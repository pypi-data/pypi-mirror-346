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

import logging


def string_to_int(int_str: str) -> int:
    if int_str is not None:
        try:
            return int(int_str)
        except ValueError as ve:
            logging.error(
                "Conversion from string ('{}') to int failed.".format(int_str)
            )
            logging.error(ve)
            return -1
    else:
        return -1


class GeoIOServiceException(Exception):
    """Exception indicates an error within GeoIO service sdk."""


class ServiceLink:
    """
    Class holding information about generated url for published service.
    href: Url of the service can be relative or absolute.
    relation: Indicates the type of service. Either an ogc feature service (ogc-service) or a wms service (wms-service).
    mime-type: The expected mime-type
    """

    mime_type: str
    relation: str
    href: str
