from flask_restx import Resource

from ..aad.auth_decorators import AuthDecorator
from ..service.stac_service import *
from ..util.dto import StacDto

auth_decorator = AuthDecorator()

api = StacDto.api


@api.route("/")
class CollectionsList(Resource):
    @api.doc(description="List all collections on the stac-api server")
    @api.response(200, "Success")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self):
        return get_all_collections(), 200


@api.route("/<collection_id>/")
class Collection(Resource):
    @api.doc(description="get_collection")
    @api.response(200, "Success")
    @api.response(404, "Collection not found")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self, collection_id: str):
        try:
            return get_collection_by_id(collection_id), 200
        except CollectionDoesNotExistError:
            return {
                       "message": "Collection with this ID not found",
                   }, 404


@api.route("/<collection_id>/items/")
class CollectionItems(Resource):

    @api.doc(description="get_collection_items")
    @api.response(200, "Success")
    @api.response(404, "Collection not found")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self, collection_id: str) -> Tuple[Dict[str, str], int]:
        try:
            return get_items_by_collection_id(collection_id), 200
        except CollectionDoesNotExistError:
            return {
                       "message": "Collection with this ID not found",
                   }, 404


@api.route("/<collection_id>/items/<item_id>/")
class CollectionItem(Resource):

    @api.doc(description="get_collection_item")
    @api.response(200, "Success")
    @api.response(404, "Collection not found")
    @api.response(404, "Item not found")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self, collection_id: str,
            item_id: str) -> Tuple[Dict[str, str], int]:
        try:
            return get_item_from_collection(collection_id, item_id), 200
        except ItemDoesNotExistError:
            return {
                       "message": "Item with this ID not found",
                   }, 404
        except CollectionDoesNotExistError:
            return {
                       "message": "Collection with this ID not found",
                   }, 404
