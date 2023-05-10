from flask import request
from flask_restx import Resource

from ..service.gdal_info_service import *
from ..util.dto import GdalInfoDto

api = GdalInfoDto.api


@api.route("/")
class GdalInfo(Resource):

    @api.doc(description="Get gdal info")
    @api.expect(GdalInfoDto.get_gdal_info, validate=True)
    @api.response(200, "Success")
    @api.response(404, "File not found")
    @api.response(500, "Internal server error")
    def post(self):
        file_path = request.json["file_url"]
        try:
            return get_gdal_info(file_path), 200
        except FileNotFoundError:
            return {"message": f'File {file_path} is not found'}, 404
        except MicroserviceIsNotAvailableError:
            return {"message": "Gdal info microservice is not available"}, 500
