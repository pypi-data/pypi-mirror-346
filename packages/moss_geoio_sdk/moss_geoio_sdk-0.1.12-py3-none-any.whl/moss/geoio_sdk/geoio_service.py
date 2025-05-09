#
# The MIT License (MIT)
# Copyright (c) 2024 M.O.S.S. Computer Grafik Systeme GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software
# is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT,TORT OR OTHERWISE, ARISING FROM, OUT
# OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


# common imports
import logging
import requests
import json
import time
from os import path
from pathlib import Path
from typing import List

from moss.geoio_sdk.model.user import User
from moss.geoio_sdk.model.geoio import geoio_init, publish_type, geoio_upload_info
from moss.geoio_sdk.utils.util import string_to_int, GeoIOServiceException, ServiceLink

# TODOs
# Authentication !


class GeoIO:
    """Api for communication to a GeoIO service."""

    __geoio_timestamp_format = "%Y-%m-%dT%H:%M:%S.%f"
    __datetime_format = "%d.%m.%Y %H:%M:%S.%f"

    __verify_ssl: bool = True
    __logger: logging.Logger = None
    __geoio_url: str
    __username: str
    __password: str
    __base_path: Path

    def __init__(
        self,
        geoio_url: str,
        username: str,
        password: str,
        base_path: Path,
        logger: logging.Logger,
        verify_ssl: bool,
    ):
        """Creates GeoIO instance to communicate with a given GeoIO service.

        Args:
            geoio_url (str): Url to the GeoIO service
            username (str): username to authenticate with GeoIO
            password (str): password to authenticate with GeoIO
            base_path (Path): default working directory
            logger (logging.Logger): logger to log to

        """
        self.__geoio_url = geoio_url
        self.__username = username
        self.__password = password
        self.__base_path = base_path
        self.__logger = logger
        self.__verify_ssl = verify_ssl
        if geoio_url is None:
            raise GeoIOServiceException("geoio_url must not be none.")
        if username is None:
            raise GeoIOServiceException("username must not be none.")
        if base_path is None:
            raise GeoIOServiceException("base_path must not be none.")

        self.session = requests.Session()
        if self._service_is_secured():
            if not self._login_user():
                raise GeoIOServiceException("Unable to login to GeoIO.")

    def set_ssl_verification(self, verify_ssl: bool):
        """Sets whether ssl verification is used or not.

        Args:
            verify_ssl (bool):

        """
        self.__verify_ssl = verify_ssl
        self.__logger.debug("Set ssl verification to {}.".format(verify_ssl))

    def publish(
        self,
        path_to_zip: Path,
        keywords: List[str],
        target: str,
        title: str,
        isolate_workspace: bool = False,
        user: User = None,
        srs: int = -1,
    ) -> str:
        """Uploads a zip file to GeoIO to create a service for each contained file.

        Args:
            path_to_zip (Path): Path to the zip
            keywords (List[str]): List of keywords
            target (str): target name in geoio
            title (str): internaly used title of upload
            isolate_workspace (bool): if True the workspace can only be
                accessed directly, and gets not listed
            user (User): optional user,
                if none, the user provided during initiation is used
            srs (int): spatial reference id for raster files
                in case they are stingy with their srs

        Returns:
            str: upload id

        Throws GeoIOServiceException if an error occurs.
        """

        if not path_to_zip.exists():
            self.__logger.error(
                "Provided file '{}' does not exist.".format(path_to_zip.absolute)
            )
            raise GeoIOServiceException(
                "Provided file '{}' does not exist.".format(path_to_zip.absolute)
            )

        if user is not None:
            user_name = user.username
        else:
            user_name = self.__username

        init_body = geoio_init(
            user_name, publish_type("SERVICE"), keywords, isolate_workspace
        )
        success, init_resp = self._do_init_request(init_body)

        if success:
            upload_id = init_resp["id"]
            upload_status = init_resp["status"]
            upload_publish_type = init_resp["publishType"]
            if "maxFileSize" in init_resp:
                upload_max_filesize = string_to_int(init_resp["maxFileSize"])
            # if "maxUploadCount" in init_resp:
            #     upload_max_files_cnt = string_to_int(init_resp["maxUploadCount"])
            # if "maxAssetSize" in init_resp:
            #     upload_max_asset_size = string_to_int(init_resp["maxAssetSize"])
        else:
            self.__logger.error("Error during initialization of the upload process.")
            self.__logger.error(str(init_resp))
            raise GeoIOServiceException(
                "Error during initialization of the upload process. ({})".format(
                    str(init_resp)
                )
            )

        if upload_id is None and upload_status is None and upload_publish_type is None:
            self.__logger.error("Request for file upload was denied.")
            raise GeoIOServiceException("Request for file upload was denied.")

        success, workspace_uuid = self._do_target_request(upload_id, target, title)
        if not success:
            self.__logger.error("Failed to do set target.")
            raise GeoIOServiceException("Failed to do set target.")

        if upload_max_filesize > -1:
            if path.getsize(path_to_zip) > upload_max_filesize:
                self.__logger.error(
                    "File '{}' exceeds maximum file size for uploads. '{}' vs. max. '{}'".format(  # noqa E501
                        path_to_zip.name,
                        path.getsize(path_to_zip),
                        upload_max_filesize,
                    )
                )
                raise GeoIOServiceException(
                    "File '{}' exceeds maximum file size for uploads.".format(
                        path_to_zip.name
                    )
                )
        else:
            self.__logger.warn(
                "No check of maximum file size possible. No value for 'maxFileSize' received."  # noqa E501
            )

        files = [path_to_zip]
        success, uploaded_files = self._do_upload_request(upload_id, files)
        if not success:
            # uploaded_files == Fehlermeldung
            raise GeoIOServiceException(
                "Upload request was not successful. {}".format(str(uploaded_files))
            )
        else:
            pass
            # uploaded_files == dict

        # Statusabfrage

        need_to_loop = True
        uploaded_files_done = []
        # uploaded_files_wrk = uploaded_files
        while need_to_loop:

            success, uploaded_files_status = self._do_upload_status_request(
                uploaded_files, uploaded_files_done
            )
            if not success:
                # uploaded_files_status == Fehlermeldung
                self.__logger.error("Error during status request for uploaded file.")
                self.__logger.error(str(uploaded_files_status))
                raise GeoIOServiceException(
                    "Error during status request for uploaded file. {}".format(
                        str(uploaded_files_status)
                    )
                )
            else:
                # uploaded_files_status == dict
                for uploaded_file in uploaded_files_status:
                    status = uploaded_files_status[uploaded_file]
                    self.__logger.debug(
                        "Status of file '{}' = '{}'".format(uploaded_file, status)
                    )
                    if status == "UPLOAD_SUCCESS":
                        uploaded_files_done.append(uploaded_file)
                    elif status == "UPLOAD_FAILED":
                        self.__logger.error(
                            "Received fail status '{}' for file '{}'.".format(
                                status, uploaded_file
                            )
                        )
                        raise GeoIOServiceException(
                            "Received fail status '{}' for file '{}'.".format(
                                status, uploaded_file
                            )
                        )
                    elif status == "PUBLISHED_SUCCESS":
                        uploaded_files_done.append(uploaded_file)
                    elif status == "PUBLISHED_FAILED":
                        self.__logger.error(
                            "Received fail status '{}' for file '{}'.".format(
                                status, uploaded_file
                            )
                        )
                        raise GeoIOServiceException(
                            "Received fail status '{}' for file '{}'.".format(
                                status, uploaded_file
                            )
                        )
                    elif status == "SRS_RASTER_INPUT":
                        if srs > -1:
                            success, message = self._do_srs_request(
                                uploaded_files[uploaded_file],
                                srs,
                            )
                            if not success:
                                self.__logger.error("Error trying to set srs:")
                                self.__logger.error(message)
                                raise GeoIOServiceException(
                                    "Error trying to set srs '{}' for file '{}'.".format(  # noqa E501
                                        str(srs), uploaded_file
                                    )
                                )
                        else:
                            self.__logger.error(
                                "No srs set. Unable to complete upload."
                            )
                            raise GeoIOServiceException(
                                "No srs set. Unable to complete upload."
                            )
                    elif status == "VALIDATION_SUCCESS":
                        uploaded_files_done.append(uploaded_file)
                    elif status == "VALIDATION_FAILED":
                        self.__logger.error(
                            "Received fail status '{}' for file '{}'.".format(
                                status, uploaded_file
                            )
                        )
                        raise GeoIOServiceException(
                            "Received fail status '{}' for file '{}'.".format(
                                status, uploaded_file
                            )
                        )
                    elif status == "SEE_MAIN_GROUP_FILE":
                        uploaded_files_done.append(uploaded_file)
                    elif status == "UNZIPPED":
                        uploaded_files_done.append(uploaded_file)
                    elif status == "NOT_SUPPORTED":
                        self.__logger.error(
                            "Received fail status '{}' for file '{}'.".format(
                                status, uploaded_file
                            )
                        )
                        raise GeoIOServiceException(
                            "Received fail status '{}' for file '{}'.".format(
                                status, uploaded_file
                            )
                        )
                    else:
                        self.__logger.error(
                            "Received unkown status '{}' for file '{}'.".format(
                                status, uploaded_file
                            )
                        )
                        raise GeoIOServiceException(
                            "Received unkown status '{}' for file '{}'.".format(
                                status, uploaded_file
                            )
                        )
            if len(uploaded_files) == len(uploaded_files_done):
                need_to_loop = False
            else:
                time.sleep(0.25)
        return upload_id

    def get_users(self) -> List[User]:
        """Returns a list of all GeoIO users.

        Returns:
            List[User]
        """
        success, users = self._do_users_request()
        if success:
            if len(users) == 0:
                self.__logger.info(
                    "get_users request was successful, but returned no users."
                )
            return users
        else:
            # users == error msg
            self.__logger.error("Users can not be retrieved. ({})".format(users))
            raise GeoIOServiceException(
                "Users can not be retrieved. ({})".format(users)
            )

    def get_uploads_of_user(self, user: User = None) -> List[str]:
        """Returns all upload ids of a given user.

        Args:
            user (User): GeoIO user, if none the user provided during initiation is used

        Returns:
            List[str]: List of upload ids
        """
        if user is None:
            user = User(self.__username)
        uploads_of_user, msg = self._do_uploads_of_user_request(user)
        if uploads_of_user is not None:
            return uploads_of_user
        else:
            self.__logger.error(
                "An error occured trying to fetch all uploads of user '{}'. ({})".format(  # noqa E501
                    user.username, msg
                )
            )
            raise GeoIOServiceException(
                "An error occured trying to fetch all uploads of user '{}'. ({})".format(  # noqa E501
                    user.username, msg
                )
            )

    def get_file_of_upload(self, upload_id: str, target_base: Path = None) -> Path:
        """Downloads the uploaded file of a given upload id.

        Args:
            upload_id (str): upload id
            target_base (Path): optional base path to store the file, if not provided
                the init base_path value is used

        Returns:
            Path: Path to file

        Throws GeoIOServiceException if an error occurs.
        """

        upload_info, msg = self._do_upload_info_request(upload_id)
        if upload_info is not None and upload_info.files is not None:
            if len(upload_info.files) > 0:
                if len(upload_info.files) == 1:
                    candidate = upload_info.files[0]
                else:
                    # use the oldest one
                    candidate = None
                    for file in upload_info.files:
                        if candidate is None:
                            candidate = file
                        else:
                            if file.created < candidate.created:
                                candidate = file
                if candidate is not None and candidate.id is not None:
                    if target_base is None:
                        target_base = self.__base_path
                    target_file = target_base.joinpath(candidate.name)
                    success, msg = self._do_file_download_request(
                        candidate.id, target_file
                    )
                    if not success:
                        self.__logger.error(
                            "Unable to download file of upload id '{}'. ({})".format(
                                upload_id, msg
                            )
                        )
                        raise GeoIOServiceException(
                            "Unable to download file of upload id '{}'. ({})".format(
                                upload_id, msg
                            )
                        )
                    else:
                        return target_file

            else:
                self.__logger.error(
                    "No file for upload id '{}' available.".format(upload_id)
                )
                raise GeoIOServiceException(
                    "No file for upload id '{}' available.".format(upload_id)
                )
        else:
            self.__logger.error(
                "No information for upload '{}' available. ({})".format(upload_id, msg)
            )
            raise GeoIOServiceException(
                "No information for upload '{}' available. ({})".format(upload_id, msg)
            )

    def get_service_urls_of_upload(
        self, upload_id: str, base_url: str = None
    ) -> List[ServiceLink]:
        """Returns relative service urls of a given upload id.

        Args:
            upload_id (str): id of an upload
            base_url (str): optional base url for returning absolute url

        Returns:
            List[ServiceLink]: List of urls of the created services

        Throws GeoIOServiceException if an error occurs.
        """
        ret = []
        upload_info, msg = self._do_upload_info_request(upload_id)
        if upload_info is not None and upload_info.workspace is not None:
            if base_url is None:
                url_prefix = ""
            else:
                url_prefix = base_url.strip("/")

            feat_link = ServiceLink()
            feat_link.mime_type = "application/octet-stream"
            feat_link.href = "{}/{}/ogc/features/v1/?f=json".format(
                url_prefix, upload_info.workspace
            )
            feat_link.relation = "ogc-service"
            ret.append(feat_link)
            wms_link = ServiceLink()
            wms_link.mime_type = "application/octet-stream"
            wms_link.href = (
                "{}/{}/ows?service=WMS&version=1.3.0&request=GetCapabilities".format(
                    url_prefix, upload_info.workspace
                )
            )
            wms_link.relation = "wms-service"
            ret.append(wms_link)
        else:
            self.__logger.error(
                "No information for upload '{}' available. ({})".format(upload_id, msg)
            )
            raise GeoIOServiceException(
                "No information for upload '{}' available. ({})".format(upload_id, msg)
            )

        return ret

    def delete_upload(self, upload_id: str) -> bool:
        """Deletes uploaded files of given upload id.

        Args:
            upload_id (str): Upload id

        Returns:
            bool: Indicates if the request was successful
        """

        success, msg = self._do_delete_upload_request(upload_id)
        if success:
            return True
        else:
            self.__logger.error(
                "Error during deletion of upload id '{}'. ({})".format(upload_id, msg)
            )
            return False

    def delete_uploads_of_user(self, user: User = None) -> bool:
        """Deletes every upload of the given user.

        Args:
            user (User): User, if none the user provided during initiation is used

        Returns:
            bool: Indicates if the request was successful
        """
        if user is None:
            user = User(self.__username)
        success, msg = self._do_delete_uploads_of_user_request(user)
        if success:
            return True
        else:
            self.__logger.error(
                "Error during deletion of uploads for user '{}'. ({})".format(
                    user.username, msg
                )
            )
            return False

    def _do_init_request(self, init_body):
        self.__logger.debug("send init request")
        headers = {"Content-type": "application/json"}
        # self.__logger.debug("init_body: {}".format(init_body.toJson()))
        init_response = self.session.post(
            self.__geoio_url + "/init",
            data=init_body.toJson(),
            headers=headers,
            verify=self.__verify_ssl,
        )
        self.__logger.debug("status_code = {}".format(init_response.status_code))
        init_resp = None
        if init_response.status_code == 200:
            # ok Status
            # response message interpretieren
            init_resp = init_response.json()
            if init_resp is not None:
                # self.__logger.debug(init_resp)
                return True, init_resp
        elif init_response.status_code == 400:
            return False, "http 400 bad request"
            # bad request
        elif init_response.status_code == 401:
            return False, "http 401 unauthorized"
            # unauthorized
        elif init_response.status_code == 500:
            return False, "http 500 internal server error"
            # internal server error

    def _do_target_request(self, upload_id, target: str, title: str):
        self.__logger.debug("send target request")
        headers = {"Content-type": "application/json"}
        target_response = self.session.patch(
            self.__geoio_url + "/uploads/" + upload_id,
            json={
                "target": target,
                "title": title,
            },
            headers=headers,
            verify=self.__verify_ssl,
        )
        self.__logger.debug("status_code = {}".format(target_response.status_code))
        # self.__logger.debug(target_response.json())

        if target_response.status_code == 200:
            target_resp = target_response.json()
            workspace = ""
            if "workspace" in target_resp:
                workspace = target_resp["workspace"]
            return True, workspace
        elif target_response.status_code == 400:
            return False, "http 400 bad request"
            # bad request
        elif target_response.status_code == 401:
            return False, "http 401 unauthorized"
            # unauthorized
        elif target_response.status_code == 500:
            return False, "http 500 internal server error"
            # internal server error

    def _do_upload_request(self, upload_id, files):
        self.__logger.debug("send upload request")
        mime_type = "application/octet-stream"
        file_list = []
        cnt = 1
        for file in files:
            self.__logger.debug("adding file for upload: {}".format(file))
            file_list.append(
                ("{}".format(cnt), (Path(file).name, open(Path(file), "rb"), mime_type))
            )
            cnt = cnt + 1

        upload_response = self.session.post(
            self.__geoio_url + "/upload",
            params={"uploadId": str(upload_id)},
            files=file_list,
            verify=self.__verify_ssl,
        )

        uploaded_files = {}
        self.__logger.debug("status_code = {}".format(upload_response.status_code))
        if upload_response.status_code == 200:
            # ok Status
            # response message interpretieren
            upload_resp = upload_response.json()
            if upload_resp is not None:
                # self.__logger.debug(upload_resp)
                if "uploadId" in upload_resp:
                    if upload_resp["uploadId"] != upload_id:
                        self.__logger.error(
                            "Request result with uploadId '{}' does not match expected uploadId '{}'.".format(  # noqa E501
                                upload_resp["uploadId"], upload_id
                            )
                        )
                        return False, "generic error"
                if "uploadedFiles" in upload_resp:
                    uploaded_files_list = upload_resp["uploadedFiles"]
                    for uf in uploaded_files_list:
                        self.__logger.debug(
                            "add to uploaded_files {}".format(uf["fileName"])
                        )
                        uploaded_files[uf["fileName"]] = uf["fileId"]
                    return True, uploaded_files
                else:
                    self.__logger.error(
                        "Request result does not contain 'uploadedFiles'."
                    )
                    return False, "generic error"
            else:
                self.__logger.error("Received empty request result.")
                return False, "generic error"
        elif upload_response.status_code == 400:
            return False, "http 400 bad request"
            # bad request
        elif upload_response.status_code == 401:
            return False, "http 401 unauthorized"
            # unauthorized
        elif upload_response.status_code == 500:
            return False, "http 500 internal server error"
            # internal server error
        else:
            return False, "http {}".format(upload_response.status_code)
            # unexpected server error

    def _do_upload_status_request(self, uploaded_files, uploaded_files_to_skip):

        # Statusabfrage
        uploaded_files_status = {}
        error_on_status_request = False
        for uploaded_file in uploaded_files:
            if uploaded_file not in uploaded_files_to_skip:
                self.__logger.debug("send upload status request")
                uploaded_file_status_response = self.session.get(
                    self.__geoio_url + "/files/" + uploaded_files[uploaded_file],
                    verify=self.__verify_ssl,
                )
                uploaded_file_status_resp = uploaded_file_status_response.json()
                # self.__logger.debug(uploaded_file_status_resp)
                # uploadFileStatus
                if "uploadFileStatus" in uploaded_file_status_resp:
                    status = uploaded_file_status_resp["uploadFileStatus"]
                    uploaded_files_status[uploaded_file] = status
                else:
                    self.__logger.error(
                        "No 'uploadFileStatus' for file '{}' received.".format(  # noqa E501
                            uploaded_file
                        )
                    )
                    error_on_status_request = True

        if error_on_status_request:
            return False, "generic error"

        status_error = False
        for uploaded_file in uploaded_files_status:
            status = uploaded_files_status[uploaded_file]
            if status == "UPLOAD_SUCCESS":
                pass
            elif status == "UPLOAD_FAILED":
                pass
            elif status == "PUBLISHED_SUCCESS":
                pass
            elif status == "PUBLISHED_FAILED":
                pass
            elif status == "SRS_RASTER_INPUT":
                pass
            elif status == "VALIDATION_SUCCESS":
                pass
            elif status == "VALIDATION_FAILED":
                pass
            elif status == "SEE_MAIN_GROUP_FILE":
                pass
            elif status == "NOT_SUPPORTED":
                pass
            elif status == "UNZIPPED":
                pass
            else:
                self.__logger.error(
                    "Unexpected 'uploadFileStatus' = '{}', for file '{}'".format(
                        status, uploaded_file
                    )
                )
                status_error = True
        if status_error:
            return False, "generic error"

        return True, uploaded_files_status
        #   ACCEPTED,
        #   UPLOAD_SUCCESS, UPLOAD_FAILED,
        #   VALIDATION_SUCCESS, VALIDATION_FAILED, NOT_SUPPORTED,
        #   DATASTORE_CREATED_SUCCESS, DATASTORE_CREATED_FAILED,
        #   ENRICH_DATA_SUCCESS, ENRICH_DATA_FAILED, ENRICH_DATA_SKIPPED,
        #   PUBLISHED_SUCCESS, PUBLISHED_FAILED,
        #   SEE_MAIN_GROUP_FILE, ZIPPED_FOR_GEOSERVER,
        #   UNZIPPED,
        #   REMOTE_FILE_NOT_FOUND,
        #   UPLOAD_PENDING,
        #   CONVERTING_TO_GPKG, CONVERTING_TO_GPKG_FAILED,
        #   SRS_RASTER_INPUT,
        #   CONVERTING_TO_GEOTIFF, CONVERTING_TO_GEOTIFF_FAILED,
        #   EMPTY_ZIP, WITH_METADATA, INVALID_METADATA

    def _do_srs_request(self, upload_file_id, srs):
        self.__logger.debug("do srs request, srs = {}".format(srs))
        # {srs: "EPSG:2024"}
        headers = {"Content-type": "application/json"}
        srs_response = self.session.post(
            self.__geoio_url + "/files/" + upload_file_id,
            json={"srs": "EPSG:{}".format(srs)},
            headers=headers,
            verify=self.__verify_ssl,
        )

        # self.__logger.debug(srs_response.json())
        self.__logger.debug("status_code = {}".format(srs_response.status_code))
        if srs_response.status_code == 200:
            return True, "http 200"
        elif srs_response.status_code == 400:
            return False, "http 400 bad request"
            # bad request
        elif srs_response.status_code == 401:
            return False, "http 401 unauthorized"
            # unauthorized
        elif srs_response.status_code == 500:
            return False, "http 500 internal server error"
            # internal server error

    def _do_upload_delete_request(self, upload_uuid, relation):
        self.__logger.debug(
            "do upload delete request, uuid = {}, relation = {}".format(
                upload_uuid, relation
            )
        )
        # headers = {"Content-type": "application/json"}
        if relation.lower() == "asset-download":
            url = self.__geoio_url + "/files/{}".format(str(upload_uuid))
        else:
            url = self.__geoio_url + "/uploads/{}".format(str(upload_uuid))
        upload_delete_response = self.session.delete(
            url,
            verify=self.__verify_ssl,
        )

        self.__logger.debug(
            "status_code = {}".format(upload_delete_response.status_code)
        )
        if upload_delete_response.status_code == 200:
            return True, "http 200"
        elif upload_delete_response.status_code == 400:
            return False, "http 400 bad request"
            # bad request
        elif upload_delete_response.status_code == 401:
            return False, "http 401 unauthorized"
            # unauthorized
        elif upload_delete_response.status_code == 405:
            return False, "http 405 method not allowed"
            # not allowed
        elif upload_delete_response.status_code == 500:
            return False, "http 500 internal server error"
            # internal server error

    def _do_upload_info_request(self, upload_id: str):
        self.__logger.debug("do upload info request, upload_id = {}".format(upload_id))
        # GET /uploads/{uploadId}
        headers = {"Content-type": "application/json"}
        upload_info_response = self.session.get(
            self.__geoio_url + "/uploads/" + upload_id,
            headers=headers,
            verify=self.__verify_ssl,
        )

        # self.__logger.debug(upload_info_response.json())
        self.__logger.debug("status_code = {}".format(upload_info_response.status_code))
        upload_info = geoio_upload_info(upload_info_response.json())
        if upload_info_response.status_code == 200:
            return upload_info, "http 200"
        elif upload_info_response.status_code == 400:
            return None, "http 400 bad request"
            # bad request
        elif upload_info_response.status_code == 401:
            return None, "http 401 unauthorized"
            # unauthorized
        elif upload_info_response.status_code == 500:
            return None, "http 500 internal server error"
            # internal server error

    def _do_file_download_request(self, file_id: str, target_path: Path):
        self.__logger.debug("do file download request, file_id = {}".format(file_id))
        # GET /download/{fileId}"
        headers = {"Content-type": "application/json"}
        file_download_response = self.session.get(
            self.__geoio_url + "/download/" + file_id,
            headers=headers,
            verify=self.__verify_ssl,
        )

        self.__logger.debug(
            "status_code = {}".format(file_download_response.status_code)
        )
        response_headers = file_download_response.headers

        if file_download_response.status_code == 200:
            content_length = response_headers.get("content-length", None)
            if content_length and int(content_length) > 0:
                open(target_path, "wb").write(file_download_response.content)
                return True, "http 200"
            else:
                self.__logger.error("No file received.")
                return False, "http 200, no content"
        elif file_download_response.status_code == 400:
            return None, "http 400 bad request"
            # bad request
        elif file_download_response.status_code == 401:
            return None, "http 401 unauthorized"
            # unauthorized
        elif file_download_response.status_code == 404:
            return None, "http 404 file not found"
            # file not found
        elif file_download_response.status_code == 500:
            return None, "http 500 internal server error"
            # internal server error

    def _do_users_request(self):
        self.__logger.debug("do users request")
        headers = {"Content-type": "application/json"}
        users_response = self.session.get(
            self.__geoio_url + "/users",
            headers=headers,
            verify=self.__verify_ssl,
        )
        # self.__logger.debug(users_response.json())
        self.__logger.debug("status_code = {}".format(users_response.status_code))
        ret: List[User] = []
        if users_response.status_code == 200:
            for user in users_response.json():
                if "username" in user:
                    usr = User(user["username"])
                    ret.append(usr)
            return True, ret
        elif users_response.status_code == 400:
            return False, "http 400 bad request"
            # bad request
        elif users_response.status_code == 401:
            return False, "http 401 unauthorized"
            # unauthorized
        elif users_response.status_code == 404:
            return False, "http 404 not found"
            # not found
        elif users_response.status_code == 500:
            return False, "http 500 internal server error"
            # internal server error

    def _do_uploads_of_user_request(self, user: User):
        self.__logger.debug(
            "do uploads of user request, username = {}".format(user.username)
        )
        # GET /uploads/{uploadId}
        headers = {"Content-type": "application/json"}
        uploads_of_user_response = self.session.get(
            self.__geoio_url + "/uploads/user/" + user.username,
            headers=headers,
            verify=self.__verify_ssl,
        )

        # self.__logger.debug(uploads_of_user_response.json())
        self.__logger.debug(
            "status_code = {}".format(uploads_of_user_response.status_code)
        )
        ret = []

        if uploads_of_user_response.status_code == 200:
            geoio_upload_infos: List[geoio_upload_info] = []
            for user_upload_info in uploads_of_user_response.json():
                upload_info = geoio_upload_info(user_upload_info)
                geoio_upload_infos.append(upload_info)
            for upload_info in geoio_upload_infos:
                if (
                    upload_info is not None
                    and upload_info.id is not None
                    and upload_info.id not in ret
                ):
                    ret.append(upload_info.id)
            return ret, "http 200"
        elif uploads_of_user_response.status_code == 400:
            return None, "http 400 bad request"
            # bad request
        elif uploads_of_user_response.status_code == 401:
            return None, "http 401 unauthorized"
            # unauthorized
        elif uploads_of_user_response.status_code == 404:
            return None, "http 404 not found"
            # bad request
        elif uploads_of_user_response.status_code == 500:
            return None, "http 500 internal server error"
            # internal server error

    # /uploads/user/{username}
    def _do_delete_uploads_of_user_request(self, user: User):
        self.__logger.debug(
            "do delete uploads of user request, username = {}".format(user.username)
        )
        # headers = {"Content-type": "application/json"}
        url = self.__geoio_url + "/uploads/user/{}".format(str(user.username))
        delete_uploads_of_user_response = self.session.delete(
            url,
            verify=self.__verify_ssl,
        )

        self.__logger.debug(
            "status_code = {}".format(delete_uploads_of_user_response.status_code)
        )
        if delete_uploads_of_user_response.status_code == 200:
            return True, "http 200"
        elif delete_uploads_of_user_response.status_code == 400:
            return False, "http 400 bad request"
            # bad request
        elif delete_uploads_of_user_response.status_code == 401:
            return False, "http 401 unauthorized"
            # unauthorized
        elif delete_uploads_of_user_response.status_code == 404:
            return False, "http 404 not found"
            # not found
        elif delete_uploads_of_user_response.status_code == 405:
            return False, "http 405 method not allowed"
            # not allowed
        elif delete_uploads_of_user_response.status_code == 500:
            return False, "http 500 internal server error"
            # internal server error

    def _do_delete_upload_request(self, upload_id: str):
        self.__logger.debug(
            "do delete upload request, upload_id = {}".format(upload_id)
        )
        # headers = {"Content-type": "application/json"}
        url = self.__geoio_url + "/uploads/{}".format(str(upload_id))
        delete_uploads_of_user_response = self.session.delete(
            url,
            verify=self.__verify_ssl,
        )

        self.__logger.debug(
            "status_code = {}".format(delete_uploads_of_user_response.status_code)
        )
        if delete_uploads_of_user_response.status_code == 200:
            return True, "http 200"
        elif delete_uploads_of_user_response.status_code == 400:
            return False, "http 400 bad request"
            # bad request
        elif delete_uploads_of_user_response.status_code == 401:
            return False, "http 401 unauthorized"
            # unauthorized
        elif delete_uploads_of_user_response.status_code == 404:
            return False, "http 404 not found"
            # not found
        elif delete_uploads_of_user_response.status_code == 405:
            return False, "http 405 method not allowed"
            # not allowed
        elif delete_uploads_of_user_response.status_code == 500:
            return False, "http 500 internal server error"
            # internal server error

    def _service_is_secured(self):
        """
        This one wil return false if the service can be used
        without token or username/password
        """

        logging.debug("Checking if service at %s is secured", self.__geoio_url)

        response = self.session.get(
            self.__geoio_url + "/users/", verify=self.__verify_ssl
        )
        logging.debug(" Status code: %s", response.status_code)

        if "application/json" in response.headers["Content-Type"]:
            logging.info("The service needs no authentication.")
            return False

        return True

    def _login_user(self):
        """
        This is the internal function to log in.
        """

        url = self.__geoio_url + "/login"

        self.__logger.info("Logging on user using the address %s", url)
        payload = {"username": self.__username, "password": self.__password}
        self.session.post(url, data=payload, verify=self.__verify_ssl)

        # Test if we can read the projects. Just to see if the log is ok.
        # If the password is wrong, the code is always 200.

        response = self.session.get(self.__geoio_url + "/users/")
        # Expecting a json response, otherwise the login was not successful
        # always returns 200!
        if response.status_code == 200:
            try:
                response_dict = json.loads(response.text)
            except ValueError as exception:
                logging.error(
                    "Login error. Please check username and password: %s", exception
                )
                return False
            else:
                self.information = response_dict
                return True

            return True
        else:
            raise GeoIOServiceException("Error logging in")


# das Publizieren von Daten in GeoIO

#  - das Generieren von Dienst-URLS zu einem Upload

#  - das Abfragen von Usern, Uploads und Files

# /* Publish's a given file to GeoServer as service. */
#   publish(file: string): Promise<string>;

#   /* Returns all users */
#   users(): Promise<User>;

#   /* Returns all uploads for a given user. */
#   uploads(user: string): Promise<Upload>;

#   /* Returns the uploaded files for a given upload id.*/
#   files(uploadId: string): Promise<File>;

#   /* Generates service URLS for a given upload. */
#   urls(uploadId: string): Promise<Link>;
# }

# const service = new GeoIO({ url: '...' });

# service.publish(pathToZip);
# service.publish(pathToFolder);
