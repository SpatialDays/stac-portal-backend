from flask_restx import Resource

from ..aad.auth_decorators import AuthDecorator
from ..service.apim_service import *
from ..service.wmts_service import get_all_wmts_urls_for_item
from ..util.dto import WMTSDto

auth_decorator = AuthDecorator()

api = WMTSDto.api


@api.route("/<string:collection_id>/items/<string:item_id>/")
class GetWMTSUrlsForItem(Resource):
    @api.doc(description="Get a WMTS urls for a given item")
    @api.response(200, "Success")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self, collection_id: str, item_id:str, oid: str = None, preferred_username: str = None, name: str = None):
        logging.debug(f"Getting WMTS urls for item {item_id} in collection {collection_id}")
        secret = None
        if current_app.config["AD_ENABLE_AUTH"]:
            if not any([oid, preferred_username, name]):
                return {"message": "Auth is enabled, but no user info was provided"}, 401
            try:
                logging.debug("Getting subscription secrets for user")
                secrets = get_subscription_secrets_for_user(oid)
            except APIMSubscriptionNotFoundError:
                return {"message": "You need to create an API key first to access this resource"}, 401

            secret = secrets["primaryKey"]
        if not secret:
            try:
                return get_all_wmts_urls_for_item(collection_id, item_id)
            except CollectionDoesNotExistError:
                return {"message": "Collection does not exist"}, 404
            except ItemDoesNotExistError:
                return {"message": "Item does not exist"}, 404

        else:
            rewritten_urls = {}
            for key, value in get_all_wmts_urls_for_item(collection_id, item_id).items():
                rewritten_urls[key] = value + f"&subscription-key={secret}"
            return rewritten_urls



