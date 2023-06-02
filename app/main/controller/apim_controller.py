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
    def get(self,oid:str, preffered_username:str, name:str):
        apim_token = f"{oid} apim_token"
        return {"apim_token": apim_token}, 200


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
