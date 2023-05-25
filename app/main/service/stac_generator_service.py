from flask import current_app
import requests


def create_STAC_Item(data):
    """
    Create a STAC (SpatioTemporal Asset Catalog) item using the provided data.

    This function sends a POST request to a local server running a STAC service
    and returns the JSON response.

    Returns:
        dict: The STAC item, in JSON format.

    Raises:
        Exception: If the API request fails for any reason.
    """
    try:
        response = requests.post(current_app.config["STAC_GENERATOR_ENDPOINT"], json=data)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print(f"Request failed: {err}")
        raise

    try:
        return response.json()
    except ValueError:
        raise Exception("Received non-JSON response from STAC API")

    return None
