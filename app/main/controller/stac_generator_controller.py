import logging

from flask import request
from flask_restx import Resource

from ..service.stac_generator_service import create_STAC_Item
from ..util.dto import StacGeneratorDto

api = StacGeneratorDto.api


@api.route("/")
class StacGenerator(Resource):
    @api.doc(description="Generate STAC from tiffs and metadata")
    @api.expect(StacGeneratorDto.stac_generator, validate=False)
    @api.response(200, "Success")
    @api.response(404, "File not found")
    @api.response(500, "Internal server error")
    def post(self):
        data = request.json
        try:
            return create_STAC_Item(data["metadata"])
        except Exception as e:
            logging.error(e)

        return None
