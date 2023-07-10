from flask_restx import Resource

from ..aad.auth_decorators import AuthDecorator
from ..service.apim_service import *
from ..service.wmts_service import get_all_wmts_urls_for_item
from ..util.dto import WMTSDto

auth_decorator = AuthDecorator()

api = WMTSDto.api


@api.route("/")
class GetWMTSUrlsForItem(Resource):
    @api.doc(description="Get a WMTS urls for a given item")
    @api.response(200, "Success")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self, oid: str, preferred_username: str, name: str):
        logging.info("Getting WMTS urls for item")
        collection_id = "landsat-c2-l2"
        item_id = "LC09_L2SP_203024_20230703_02_T1"
        secret = None
        if current_app.config["AD_ENABLE_AUTH"]:
            try:
                secrets = get_subscription_secrets_for_user(oid)
            except APIMSubscriptionNotFoundError:
                try:
                    get_user_from_apim(oid)
                except APIMUserNotFoundError:
                    first_name = name.split(" ")[0]
                    last_name = "".join(name.split(" ")[1:])
                    try:
                        create_user_on_apim(oid, preferred_username, first_name, last_name)
                    except APIMUserCreationError:
                        return {"message": "Error creating user on APIM"}, 500

                try:
                    make_subscription_for_user_on_all_apis(oid)
                    secrets = get_subscription_secrets_for_user(oid)
                except APIMSubscriptionCreationError:
                    return {"message": "Error creating subscription on APIM"}, 500

            secret = secrets["secrets"]["primaryKey"]
        if not secret:
            return get_all_wmts_urls_for_item(collection_id, item_id)
        else:
            rewriten_urls = {}
            for key, value in get_all_wmts_urls_for_item(collection_id, item_id).items():
                rewriten_urls[key] = value + f"&subscription-key={secret}"
            return rewriten_urls



