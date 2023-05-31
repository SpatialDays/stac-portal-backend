from flask import request
from flask_restx import Resource

from ..aad.auth_decorators import AuthDecorator
from ..service.validate_service import validate_json
from ..util.dto import ValidateDto

auth_decorator = AuthDecorator()

api = ValidateDto.api
validate = ValidateDto.validate


@api.route("/json/")
class ValidateJSON(Resource):
    @api.doc("validate_json")
    @api.expect(validate)
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Creator"]
    )
    def post(self):
        data = request.json
        resp, status = validate_json(data=data)
        return resp, status
