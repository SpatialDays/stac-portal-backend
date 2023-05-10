import requests
from flask import current_app

from ..custom_exceptions import *


def get_gdal_info(url: str) -> str:
    """
    Get gdal info from url using gdal api microservice
    """
    gdal_info_api_endpoint = current_app.config["GDAL_INFO_API_ENDPOINT"]
    try:
        response = requests.post(gdal_info_api_endpoint, json={"file_url": url})
        response_code = response.status_code
        if response_code == 404:
            raise FileNotFoundError
        return response.json()
    except ConnectionError:
        raise MicroserviceIsNotAvailableError("Gdal info microservice is not available")
