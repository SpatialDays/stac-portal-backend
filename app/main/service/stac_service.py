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
        public_collections: [] = public_catalogs_service.get_public_collections()
        public_collections_ids = [collection["id"] for collection in public_collections]
        for collection in collection_json["collections"]:
            collection["management_metadata"] = {}
            if collection["id"] in public_collections_ids:
                index = public_collections_ids.index(collection["id"])
                collection["management_metadata"]["parent_catalog_id"] = public_collections[index]["parent_catalog"]
                collection["management_metadata"]["is_public"] = True
            else:
                collection["management_metadata"]["is_public"] = False
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
            raise CollectionAlreadyExistsError
        elif "item" in response.json()["description"].lower() \
                and "does not exist" in response.json()["description"].lower():
            raise ItemDoesNotExistError
    else:
        resp = response.json()
        resp["error_code"] = response.status_code
        return resp


def remove_public_collection_by_id_on_stac_api(
        collection_id: str) -> Dict[any, any]:
    """Remove a collection by ID from the STAC API server.

    Additionally, removes all stored search parameters associated with the collection.


    :param collection_id: Collection ID to remove.
    :return: Either a tuple containing stac server response and status code, or a Response object.
    """
    response = requests.delete(urljoin(current_app.config["WRITE_STAC_API_SERVER"], "collections/") + collection_id)

    public_catalogs_service.remove_search_params_for_collection_id(
        collection_id)
    if response.status_code in range(200, 203):
        collection_json = response.json()
        return collection_json
    elif response.status_code == 400:
        raise InvalidCollectionPayloadError
    elif response.status_code == 404:
        raise CollectionDoesNotExistError
    else:
        resp = response.json()
        resp["error_code"] = response.status_code
        return resp


def remove_private_collection_by_id_on_stac_api(collection_id: str) -> Dict[str, any]:
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


def add_item_to_collection_on_stac_api(
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


def update_item_in_collection_on_stac_api(
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


def remove_item_from_collection_on_stac_api(
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
