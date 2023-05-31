import logging

from flask import request
from flask_restx import Resource

from ..aad.auth_decorators import AuthDecorator
from ..service.stac_generator_service import create_STAC_Item
from ..util.dto import StacGeneratorDto

auth_decorator = AuthDecorator()

api = StacGeneratorDto.api


@api.route("/")
class StacGenerator(Resource):
    """
    This class represents the STAC Generator resource, which allows users to generate
    SpatioTemporal Asset Catalog (STAC) items from provided TIFF images and metadata.
    """

    @api.doc(description="Generate STAC from TIFFs and metadata")
    @api.expect(StacGeneratorDto.stac_generator, validate=False)
    @api.response(200, "Success")
    @api.response(404, "File not found")
    @api.response(500, "Internal server error")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Creator"]
    )
    def post(self):
        """
        The POST method for the STAC Generator resource.

        This method accepts JSON data with TIFF image locations and metadata,
        and uses it to create a STAC item.

        The method returns the created STAC item, or an error message if the
        creation process fails.
        """
        data = request.json
        try:
            return create_STAC_Item(data)
        except Exception as e:
            logging.error(f"STAC item creation failed with error: {e}")
            api.abort(500, str(e))
