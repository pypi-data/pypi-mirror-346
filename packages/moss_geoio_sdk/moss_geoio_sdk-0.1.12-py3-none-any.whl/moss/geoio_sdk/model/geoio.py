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


import json
from typing import List
from datetime import datetime

GEOIO_TIMSTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
GEOIO_SHORT_TIMSTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"


class publish_type:
    type: str = None

    def __init__(self, type: str) -> None:
        self.type = type


class geoio_init:
    username: str = None
    publish: publish_type = None
    config = []
    keywords = []
    isolated: bool = False

    def __init__(
        self, username: int, publish: publish_type, keywords, isolated: bool = False
    ):
        self.username = username
        self.publish = publish
        self.keywords = keywords
        self.isolated = isolated

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    # {
    #     "username": "Erfassung",
    #     "publish": {
    #         "type": "SERVICE"
    #     }


class geoio_init_response:
    id: str = None
    status: str = None
    publishType: str = None
    # {
    #     "id": "9f2fefed-68ad-45af-9ad8-2c9dc6b080fa",
    #     "status": "CREATED",
    #     "publishType": "SERVICE"
    # }


class geoio_upload_file:
    id: str = None
    name: str = None
    status: str = None
    created: datetime = None

    def __init__(self, file_json: str):
        if file_json is not None:
            if "id" in file_json:
                self.id = file_json["id"]
            if "name" in file_json:
                self.name = file_json["name"]
            if "uploadFileStatus" in file_json:
                self.status = file_json["uploadFileStatus"]
            if "created" in file_json:
                self.created = self._parse_timestamp(file_json["created"])

    def _parse_timestamp(self, timestamp: str) -> datetime:
        try:
            return datetime.strptime(timestamp, GEOIO_TIMSTAMP_FORMAT)
        except Exception as exception:  # noqa E841
            return datetime.strptime(timestamp, GEOIO_SHORT_TIMSTAMP_FORMAT)


# public class UploadFileDTO {
#   private String id;
#   private String name;
#   private String created;
#   private String uploadFileStatus;
#   private String extendedMessage;
#   private String geoserverLayer;
#   private String parentFileId;
#   private String parentFileName;


class geoio_upload_info:
    id: str = None
    created: datetime = None
    created_by: str = None
    files: List[geoio_upload_file] = None
    configs: dict[str, str] = None
    last_updated: str = None
    title: str = None
    description: str = None
    target: str = None
    workspace: str = None
    publish_type: str = None

    def __init__(self, json_upload_info: str):
        if json_upload_info is not None:
            if "id" in json_upload_info:
                self.id = json_upload_info["id"]
            if "created" in json_upload_info:
                self.created = self._parse_timestamp(json_upload_info["created"])
            if "createdBy" in json_upload_info:
                self.created_by = json_upload_info["createdBy"]
            if "files" in json_upload_info:
                self.files = self._extract_files(json_upload_info["files"])
            if "configs" in json_upload_info:
                self.configs = self._extract_configs(json_upload_info["configs"])
            if "lastUpdated" in json_upload_info:
                self.last_updated = json_upload_info["lastUpdated"]
            if "title" in json_upload_info:
                self.title = json_upload_info["title"]
            if "description" in json_upload_info:
                self.description = json_upload_info["description"]
            if "target" in json_upload_info:
                self.target = json_upload_info["target"]
            if "workspace" in json_upload_info:
                self.workspace = json_upload_info["workspace"]
            if "publishType" in json_upload_info:
                self.publish_type = json_upload_info["publishType"]

    def _extract_files(self, files_json):
        ret = []
        if files_json is not None:
            for file_json in files_json:
                ret.append(geoio_upload_file(file_json))
        return ret

    def _extract_configs(self, configs_json):
        ret = {}
        if configs_json is not None:
            for config_json in configs_json:
                key = None
                value = None
                if config_json is not None:
                    if "key" in config_json:
                        key = config_json["key"]
                    if "value" in config_json:
                        value = config_json["value"]
                    if key is not None and value is not None and key not in ret:
                        ret[key] = value
        return ret

    def _parse_timestamp(self, timestamp: str) -> datetime:
        # return datetime.strptime(timestamp, GEOIO_TIMSTAMP_FORMAT)
        try:
            return datetime.strptime(timestamp, GEOIO_TIMSTAMP_FORMAT)
        except Exception as exception:  # noqa E841
            return datetime.strptime(timestamp, GEOIO_SHORT_TIMSTAMP_FORMAT)

    #   private String id;
    #   private String created;
    #   private String createdBy;
    #   private List<UploadFileDTO> files;
    #   private List<UploadConfigDTO> configs;
    #   private String lastUpdated;
    #   private String title;
    #   private String description;
    #   private String target;
    #   private String workspace;
    #   private String publishType;
