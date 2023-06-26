from typing import Tuple, Dict

from flask import request
from flask_restx import Resource

from ..aad.auth_decorators import AuthDecorator
from ..custom_exceptions import *
from ..service import private_catalog_service
from ..util.dto import PrivateCatalogDto

auth_decorator = AuthDecorator()

api = PrivateCatalogDto.api
collections = PrivateCatalogDto.collection


@api.route("/collections/")
class CollectionGetCreateUpdate(Resource):
    @api.doc(description="Create a new private collection")
    @api.expect(PrivateCatalogDto.collection_dto, validate=True)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Creator"]
    )
    def post(self):
        try:
            return private_catalog_service.add_collection(request.json)
        except PrivateCollectionAlreadyExistsError:
            return {
                       "message": "Collection with this ID already exists",
                   }, 409
        except ConvertingTimestampError as e:
            return {
                       "message": f"Error converting timestamp: {e}",
                   }, 400

    @api.doc(description="Update a private collection")
    @api.expect(PrivateCatalogDto.collection_dto, validate=True)
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.response(404, "Collection not found")
    @api.response("4xx", "Stac API reported error")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Creator"]
    )
    def put(self):
        try:
            return private_catalog_service.update_collection(request.json), 200
        except PrivateCollectionDoesNotExistError:
            return {
                       "message": "Collection with this ID not found",
                   }, 404
        except ConvertingTimestampError as e:
            return {
                       "message": f"Error converting timestamp: {e}",
                   }, 400

    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self):
        return private_catalog_service.get_all_collections(), 200
