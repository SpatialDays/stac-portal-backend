from flask_restx import Resource

from ..aad.auth_decorators import AuthDecorator
from ..service.stac_service import *
from ..util.dto import StacDto
from flask import request

auth_decorator = AuthDecorator()

api = StacDto.api


@api.route("/")
class ListOfCollections(Resource):
    @api.doc(description="List all collections on the stac-api server")
    @api.response(200, "Success")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self):
        return get_all_collections(), 200


@api.route("/<collection_id>/")
class Collection(Resource):
    @api.doc(description="Get specific collection by ID")
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

    @api.doc(description="Get all items from collection")
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

    @api.doc(description="Add item to collection")
    @api.response(200, "Success")
    @api.response(404, "Collection not found")
    @api.response(409, "Item already exists")
    @api.response(400, "Invalid payload")
    @api.expect(StacDto.item_dto, validate=True)
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Creator"]
    )
    def post(self, collection_id: str):
        try:
            return add_stac_item(collection_id, request.json)
        except CollectionDoesNotExistError:
            return {
                       "message": "Collection with this ID not found",
                   }, 404
        except ItemAlreadyExistsError:
            return {
                       "message": "Item with this ID already exists",
                   }, 409
        except InvalidCollectionPayloadError:
            return {
                       "message": "Invalid payload",
                   }, 400


@api.route("/<collection_id>/items/<item_id>/")
class CollectionItem(Resource):

    @api.doc(description="Get specific item from specific collection")
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


@api.route("/collections/<collection_id>/items/<item_id>/")
class CollectionItem(Resource):

    @api.doc(description="Update specific item in a specific collection")
    @api.response(200, "Success")
    @api.response(403, "Unauthorized.")
    @api.expect(StacDto.item_dto, validate=True)
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Creator"]
    )
    def put(self, collection_id: str, item_id: str):
        try:
            return update_stac_item(collection_id, item_id, request.json), 200
        except CollectionDoesNotExistError:
            return {
                       "message": "Collection with this ID not found",
                   }, 404
        except ItemDoesNotExistError:
            return {
                       "message": "Item with this ID not found",
                   }, 404

    @api.doc(description="Remove specific item from specific collection")
    @api.response(200, "Success")
    @api.response(403, "Unauthorized.")
    @api.response("4xx", "Stac API reported error")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Creator"]
    )
    def delete(self, collection_id: str, item_id: str):
        try:
            return remove_stac_item(collection_id, item_id), 200
        except CollectionDoesNotExistError:
            return {
                       "message": "Collection with this ID not found",
                   }, 404
        except ItemDoesNotExistError:
            return {
                       "message": "Item with this ID not found",
                   }, 404
