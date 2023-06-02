from flask_restx import Resource
from ..aad.auth_decorators import AuthDecorator
from ..util.dto import APIMDto
from ..service.apim_service import *
from ..custom_exceptions import *

auth_decorator = AuthDecorator()

api = APIMDto.api


@api.route("/")
class GetAPIMToken(Resource):
    @api.doc(description="Get a APIM token")
    @api.response(200, "Success")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self, oid: str, preferred_username: str, name: str):
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

        return {"secrets": secrets}, 200


@api.route("/refresh/")
class RefreshAPIMToken(Resource):
    @api.doc(description="Refresh a APIM token")
    @api.response(200, "Success")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def get(self,oid:str):
        apim_token = f"{oid} apim_token"

        return {"apim_token": apim_token}, 200
