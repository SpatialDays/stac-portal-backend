from typing import Dict, Tuple
from urllib.parse import urljoin

import requests
from flask import Response
from flask import current_app

from . import public_catalogs_service
from ..custom_exceptions import *


def get_all_collections() -> Dict[str, any]:
    response = requests.get(urljoin(current_app.config["READ_STAC_API_SERVER"], "collections/"))
    if response.status_code in range(200, 203):
        collection_json = response.json()
        return collection_json
    else:
        resp = response.json()
        resp["error_code"] = response.status_code
        return resp


def get_collection_by_id(
        collection_id: str) -> Dict[str, any]:
    response = requests.get(urljoin(current_app.config["READ_STAC_API_SERVER"], "collections/") + collection_id)
    if response.status_code in range(200, 203):
        collection_json = response.json()
        return collection_json
    elif response.status_code == 404:
        raise CollectionDoesNotExistError
    elif response.status_code == 424:
        raise CollectionDoesNotExistError
    else:
        resp = response.json()
        resp["error_code"] = response.status_code
        return resp


def get_items_by_collection_id(
        collection_id: str) -> Dict[str, any]:
    response = requests.get(
        urljoin(current_app.config["READ_STAC_API_SERVER"], "collections/") + collection_id + "/items")

    if response.status_code in range(200, 203):
        collection_json = response.json()
        return collection_json
    elif response.status_code == 404:
        raise CollectionDoesNotExistError
    elif response.status_code == 424:
        raise CollectionDoesNotExistError
    else:
        resp = response.json()
        resp["error_code"] = response.status_code
        return resp


def get_item_from_collection(
        collection_id: str,
        item_id: str) -> Dict[str, any]:
    response = requests.get(
        urljoin(current_app.config["READ_STAC_API_SERVER"], "collections/") + collection_id + "/items/" + item_id)

    if response.status_code in range(200, 203):
        collection_json = response.json()
        return collection_json
    elif response.status_code == 404:
        if "collection" in response.json()["description"].lower() and \
                "does not exist" in response.json()["description"].lower():
            raise CollectionDoesNotExistError
        elif "item" in response.json()["description"].lower() and \
                "does not exist" in response.json()["description"].lower():
            raise ItemDoesNotExistError
    elif response.status_code == 424:
        raise CollectionDoesNotExistError
    else:
        resp = response.json()
        resp["error_code"] = response.status_code
        return resp


def create_new_collection_on_stac_api(
        collection_data: Dict[str,
                              any]) -> Dict[str, any]:
    response = requests.post(urljoin(current_app.config["WRITE_STAC_API_SERVER"], "collections/"),
                             json=collection_data)

    if response.status_code in range(200, 203):
        collection_json = response.json()
        return collection_json
    elif response.status_code == 400:
        raise InvalidCollectionPayloadError
    elif response.status_code == 409:
        raise CollectionAlreadyExistsError
    else:
        resp = response.json()
        resp["error_code"] = response.status_code
        return resp


def update_existing_collection_on_stac_api(
        collection_data: Dict[str,
                              any]) -> Dict[str, any]:
    response = requests.put(urljoin(current_app.config["WRITE_STAC_API_SERVER"], "collections/"), json=collection_data)

    if response.status_code in range(200, 203):
        collection_json = response.json()
        return collection_json
    elif response.status_code == 400:
        raise InvalidCollectionPayloadError
    elif response.status_code == 404:
        if "collection" in response.json()["description"].lower() \
                and "does not exist" in response.json()["description"].lower():
            raise CollectionDoesNotExistError
    else:
        resp = response.json()
        resp["error_code"] = response.status_code
        return resp


def remove_collection(collection_id: str) -> Dict[str, any]:
    response = requests.delete(urljoin(current_app.config["WRITE_STAC_API_SERVER"], "collections/") + collection_id)
    if response.status_code in range(200, 203):
        collection_json = response.json()
        return collection_json
    elif response.status_code == 400:
        raise InvalidCollectionPayloadError
    elif response.status_code == 404:
        raise PrivateCollectionDoesNotExistError
    else:
        resp = response.json()
        resp["error_code"] = response.status_code
        return resp


def add_stac_item(
        collection_id: str,
        item_data: Dict[str, any]) -> Dict[str, any]:
    response = requests.post(
        urljoin(current_app.config["WRITE_STAC_API_SERVER"], "collections/") + collection_id + "/items",
        json=item_data, headers={"Content-Type": "application/json"})

    if response.status_code in range(200, 203):
        collection_json = response.json()
        return collection_json
    elif response.status_code == 400:
        raise InvalidCollectionPayloadError
    elif response.status_code == 404:
        raise CollectionDoesNotExistError
    elif response.status_code == 409:
        raise ItemAlreadyExistsError
    elif response.status_code == 424:
        raise CollectionDoesNotExistError
    else:
        resp = response.json()
        resp["error_code"] = response.status_code
        return resp


def update_stac_item(
        collection_id: str, item_id: str,
        item_data: Dict[str, any]):
    response = requests.put(
        urljoin(current_app.config["WRITE_STAC_API_SERVER"], "collections/") + collection_id + "/items/" +
        item_id,
        json=item_data)

    if response.status_code in range(200, 203):
        collection_json = response.json()
        return collection_json
    elif response.status_code == 400:
        raise InvalidCollectionPayloadError
    elif response.status_code == 404:
        raise CollectionDoesNotExistError
    elif response.status_code == 424:
        raise CollectionDoesNotExistError
    else:
        resp = response.json()
        resp["error_code"] = response.status_code
        return resp


def remove_stac_item(
        collection_id: str,
        item_id: str):
    response = requests.delete(
        urljoin(current_app.config["WRITE_STAC_API_SERVER"], "collections/") + collection_id + "/items/" + item_id)

    if response.status_code in range(200, 203):
        collection_json = response.json()
        return collection_json
    elif response.status_code == 400:
        raise InvalidCollectionPayloadError
    elif response.status_code == 404:
        raise CollectionDoesNotExistError
    elif response.status_code == 424:
        raise CollectionDoesNotExistError
    else:
        resp = response.json()
        resp["error_code"] = response.status_code
        return resp


