from flask import current_app

import requests
from werkzeug.datastructures import FileStorage
from typing import Dict
from requests.models import Response


def send_file_to_transformer(file: FileStorage, output_epsg: str) -> Response:
    """
    Send a file and output EPSG to the transformer service.

    :param file: The file to be transformed.
    :param output_epsg: The output EPSG for the transformation.
    :return: The response from the transformer service.
    """
    files = {"file": file}
    data = {"output_epsg": output_epsg}

    try:
        response = requests.post(
            current_app.config["TRANSFORMER_ENDPOINT"], files=files, data=data
        )
        response.raise_for_status()
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        raise
    except Exception as err:
        print(f"Other error occurred: {err}")
        raise

    return response
