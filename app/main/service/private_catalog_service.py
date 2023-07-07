import json

from .stac_service import *
from ..custom_exceptions import *
from .public_catalogs_service import get_all_available_public_collections
from .stac_service import get_all_collections as get_all_collections_from_stac_api
from .stac_service import remove_collection as remove_collection_from_stac_api


def add_collection(collection: Dict[str, any]) -> Dict[str, any]:
    try:
        collection["stac_extensions"] = [
            "https://raw.githubusercontent.com/SpatialDays/sd-stac-extensions/main/spatialdays-stac-portal-metadata/v0.0.1/schema.json"]
        collection["stac-portal-metadata"] = {
            "type-of-collection": "private",
            "is-authoritative": False,
        }
        status = create_new_collection_on_stac_api(collection)
        return status
    except CollectionAlreadyExistsError:
        raise PrivateCollectionAlreadyExistsError
    except InvalidCollectionPayloadError:
        raise InvalidCollectionPayloadError


def update_collection(collection: Dict[str, any]) -> Dict[str, any]:
    try:
        status = update_existing_collection_on_stac_api(collection)
        return status
    except CollectionDoesNotExistError:
        raise PrivateCollectionDoesNotExistError
    except InvalidCollectionPayloadError:
        raise InvalidCollectionPayloadError


def get_all_collections():
    collections = get_all_collections_from_stac_api()
    collections_to_return = []
    for i in collections["collections"]:
        try:
            if i["stac-portal-metadata"]["type-of-collection"] == "private":
                collections_to_return.append(i)
        except KeyError:
            pass
    return collections_to_return
