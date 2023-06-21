import json

from flask import request
from flask_restx import Resource
from typing import List, Dict
from flask import jsonify


from ..aad.auth_decorators import AuthDecorator
from ..custom_exceptions import *
from ..service import public_catalogs_service
from ..util.dto import PublicCatalogsDto

auth_decorator = AuthDecorator()

api = PublicCatalogsDto.api


@api.route("/")
class PublicCatalogs(Resource):
    @api.doc(description="""Get all public catalogs stored in the database.""")
    @api.doc("List all public catalogs in the database")
    @api.response(200, "Success")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self):
        return public_catalogs_service.get_all_stored_public_catalogs()

    @api.doc(description="Store a new public catalog in the database")
    @api.expect(PublicCatalogsDto.add_public_catalog, validate=True)
    @api.response(201, "Success")
    @api.response(400, "Validation Error - Some elements are missing")
    @api.response(409, "Conflict - Catalog already exists")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Creator"]
    )
    def post(self):
        try:
            data = request.json
            name = data["name"]
            url = data["url"]
            description = data["description"]
            return (
                public_catalogs_service.store_new_public_catalog(
                    name, url, description
                ),
                201,
            )
        except IndexError:
            return {
                "message": "Some elements in json body are not present",
            }, 400
        except CatalogAlreadyExistsError:
            return {
                "message": "Catalog with this url already exists",
            }, 409

    @api.doc(description="Delete all public catalogs from the database")
    @api.response(200, "Success")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Creator"]
    )
    def delete(self):
        public_catalogs_service.remove_all_public_catalogs()
        return {"message": "Deleted all catalogs"}, 200


@api.route("/sync/")
class PublicCatalogsUpdate(Resource):
    @api.doc(description="Get all public catalogs and update them")
    @api.response(200, "Success")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Creator"]
    )
    def get(self):
        public_catalogs_service.store_publicly_available_catalogs()
        return {"message": "Sync operation started"}, 200


@api.route("/collections/")
class PublicCatalogsCollections(Resource):
    @api.doc("Get all public collections stored in the database")
    @api.response(200, "Success")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self):
        return public_catalogs_service.get_all_stored_public_collections_as_list_of_dict()


@api.route("/collections/search/")
class PublicCatalogsCollections(Resource):
    @api.doc(description="Get all collections of all public catalogs")
    @api.response(200, "Success")
    @api.expect(PublicCatalogsDto.collection_search, validate=True)
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Creator"]
    )
    def post(self):
        spatial_extent_bbox: List[float] = request.json.get("bbox", None)
        spatial_extent_intersects: str or Dict = request.json.get("intersects", None)

        if not spatial_extent_bbox and not spatial_extent_intersects:
            return {"message": "Either bbox or intersects is required"}, 400

        if spatial_extent_bbox and spatial_extent_intersects:
            return {"message": "Only one of bbox or intersects is allowed"}, 400

        temporal_extent: str = request.json["datetime"]

        if spatial_extent_bbox:
            return (
                public_catalogs_service.search_collections(
                    temporal_extent,
                    spatial_extent_bbox=spatial_extent_bbox,
                )
            ), 200

        if spatial_extent_intersects:
            return (
                public_catalogs_service.search_collections(
                    temporal_extent,
                    spatial_extent_intersects=spatial_extent_intersects,
                )
            ), 200


@api.route("/<int:public_catalog_id>/collections/search/")
class SpecificPublicCatalogCollections(Resource):
    @api.doc(description="Get all collections for specified public catalog")
    @api.response(200, "Success")
    @api.response(404, "Not Found - Catalog does not exist")
    @api.expect(PublicCatalogsDto.collection_search, validate=True)
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Creator"]
    )
    def post(self, public_catalog_id):
        spatial_extent_bbox: List[float] = request.json["bbox"]
        temporal_extent: str = request.json["datetime"]
        try:
            return (
                public_catalogs_service.search_collections(
                    temporal_extent, public_catalog_id, spatial_extent_bbox=spatial_extent_bbox
                )
            ), 200
        except CatalogDoesNotExistError:
            return {
                "message": "Catalog with this id does not exist",
            }, 404


@api.route("/<int:public_catalog_id>/load_history/")
class PublicCatalogLoadHistory(Resource):
    @api.doc(description="Get load history for specified public catalog")
    @api.response(200, "Success")
    @api.response(404, "Not Found - Catalog does not exist")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self, public_catalog_id):
        try:
            return (
                public_catalogs_service.get_all_stored_search_parameters(
                    public_catalog_id
                ),
                200,
            )
        except PublicCatalogDoesNotExistError:
            return {
                "message": "Catalog with this id does not exist",
            }, 404


@api.route("/<int:public_catalog_id>/collections/")
class PublicCatalogCollections(Resource):
    @api.doc(description="Get all collections for specified public catalog")
    @api.response(200, "Success")
    @api.response(404, "Not Found - Catalog does not exist")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self, public_catalog_id):
        try:
            return (
                public_catalogs_service.get_collections_from_public_catalog_id(
                    public_catalog_id
                ),
                200,
            )
        except PublicCatalogDoesNotExistError:
            return {
                "message": "Catalog with this id does not exist",
            }, 404


@api.route("/<int:public_catalog_id>/collections/<string:collection_id>/")
class SpecificPublicCatalogCollection(Resource):
    @api.doc(description="Get specified collection for specified public catalog")
    @api.response(200, "Success")
    @api.response(404, "Not Found - Catalog or collection does not exist")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Creator"]
    )
    def delete(self, public_catalog_id, collection_id):
        try:
            public_catalogs_service.remove_collection_from_public_catalog(
                public_catalog_id, collection_id
            )
            return {
                "message": "Collection successfully deleted",
            }, 200
        except CatalogDoesNotExistError:
            return {
                "message": "Catalog with this id does not exist",
            }, 404
        except PublicCollectionDoesNotExistError:
            return {
                "message": "Collection with this id does not exist",
            }, 404


@api.route("/<int:public_catalog_id>/")
class PublicCatalogsViaId(Resource):
    @api.doc(description="""Get the details of a public catalog by its id.""")
    @api.response(200, "Success")
    @api.response(404, "Public catalog not found")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self, public_catalog_id):
        try:
            return public_catalogs_service.get_public_catalog_by_id_as_dict(
                public_catalog_id
            )

        except CatalogDoesNotExistError:
            return {"message": "Public catalog not found"}, 404

    @api.doc(description="Remove a public catalog via its id")
    @api.response(200, "Success")
    @api.response(404, "Public catalog not found so it cant be removed")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Creator"]
    )
    def delete(self, public_catalog_id):
        try:
            return public_catalogs_service.remove_public_catalog_via_catalog_id(
                public_catalog_id
            )
        except CatalogDoesNotExistError:
            return {"message": "No result found"}, 404


@api.route("/<int:public_catalog_id>/items/get/")
class GetStacRecordsSpecifyingPublicCatalogId(Resource):
    @api.doc(description="""Get specific collections from catalog.""")
    @api.expect(PublicCatalogsDto.start_stac_ingestion, validate=True)
    @api.response(200, "Success")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Creator"]
    )
    def post(self, public_catalog_id):
        data = request.json
        try:
            return (
                public_catalogs_service.load_specific_collections_via_catalog_id(
                    public_catalog_id, data
                ),
                200,
            )
        except CatalogDoesNotExistError:
            return {"message": "Public catalog not found"}, 404
        except ConnectionError:
            return {
                "message": "Connection Error, ingestion microservice is probably down"
            }, 500


@api.route("/items/update/")
class UpdateAllStacRecords(Resource):
    @api.doc(description="Update all stored stac records from all public catalogs")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self):
        try:
            result = public_catalogs_service.update_all_stac_records()
            response = []
            for i in result:
                response.append(
                    {
                        "operation_number": i,
                    }
                )
            return response, 200
        except ConnectionError:
            return {
                "message": "Connection Error, ingestion microservice is probably down"
            }, 500


@api.route("/<int:public_catalog_id>/items/update/")
class UpdateStacRecordsSpecifyingPublicCatalogId(Resource):
    @api.doc(description="""Get all stac records from a public catalog.""")
    @api.response(200, "Success")
    @api.response(404, "Public catalog not found")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self, public_catalog_id):
        try:
            return public_catalogs_service.update_specific_collections_via_catalog_id(
                public_catalog_id
            )
        except CatalogDoesNotExistError:
            return {"message": "Public catalog not found"}, 404
        except ConnectionError:
            return {
                "message": "Connection Error, ingestion microservice is probably down"
            }, 500

    @api.doc(description="""Update specific collections from catalog.""")
    @api.expect(
        PublicCatalogsDto.update_stac_collections_specify_collection_ids, validate=True
    )
    @api.response(200, "Success")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Creator"]
    )
    def post(self, public_catalog_id):
        collections_to_update = request.json["collections"]
        try:
            result = public_catalogs_service.update_specific_collections_via_catalog_id(
                public_catalog_id, collections_to_update
            )
            response = []
            for i in result:
                response.append(
                    {
                        "message": i,
                    }
                )
            return response, 200
        except CatalogDoesNotExistError:
            return {"message": "Public catalog with specified id not found"}, 404
        except ConnectionError:
            return {
                "message": "Connection Error, ingestion microservice is probably down"
            }, 500


@api.route("/run_search_parameters/<int:parameter_id>/")
class RunSearchParameters(Resource):
    @api.doc(description="Run search parameters for specified public catalog")
    @api.response(200, "Success")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self, parameter_id):
        try:
            return public_catalogs_service.run_search_parameters(parameter_id), 200
        except StoredSearchParametersDoesNotExistError:
            return {
                "message": "Search param with this id does not exist",
            }, 404
