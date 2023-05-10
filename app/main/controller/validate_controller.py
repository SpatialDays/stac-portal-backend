from flask import request
from flask_restx import Resource

from ..service.validate_service import validate_json
from ..util.dto import ValidateDto

api = ValidateDto.api
validate = ValidateDto.validate


@api.route("/json/")
class ValidateJSON(Resource):
    @api.doc("validate_json")
    @api.expect(validate)
    def post(self):
        data = request.json
        resp, status = validate_json(data=data)
        return resp, status
