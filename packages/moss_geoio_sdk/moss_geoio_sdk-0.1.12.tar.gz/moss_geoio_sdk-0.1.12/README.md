# MOSS GeoIO SDK

## Description

This is the Python SDK to interact with [M.O.S.S. Computer Grafik Systeme GmbH](https://www.moss.de/wega/) GeoIO

## Installation

This package kann be installed using pip

```shell
python -m pip install moss_geoio_sdk
```

## Usage

```python
import sys
from pathlib import Path
import logging
from moss.geoio_sdk.geoio_service import GeoIO
from moss.geoio_sdk.model.user import User

user_name = "username"
user_password = "password"
geoIO_url = "https://geoio.server.your.domain:8443/mcm-geoio"

my_logger = logging.getLogger("my_logger")
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
geoIO = GeoIO(
    geoIO_url, user_name, user_password, Path("c:/temp/geoio_sdk"), my_logger
)
```
