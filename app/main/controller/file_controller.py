from flask import request
from flask_restx import Resource
from werkzeug.utils import secure_filename

from ..service.file_service import *
from ..util.dto import FileDto, FilesDto

api = FileDto.api
files_api = FilesDto.files_api


@api.route("/sas_token/<filename>/")
class GetSasToken(Resource):
    @api.doc(description="Get a SAS token for the blob")
    @api.response(200, "Success")
    def get(self, filename):
        sas_token, endpoint, endpoint_without_sas_token = get_write_sas_token(filename)

        return {"sas_token": sas_token,
                "endpoint": endpoint,
                "endpoint_without_sas_token": endpoint_without_sas_token
                }, 200


@api.route("/sas_token_read/<filename>/")
class GetReadSasToken(Resource):
    @api.doc(description="Get a SAS token for the blob")
    @api.response(200, "Success")
    def get(self, filename):
        sas_token, endpoint, endpoint_without_sas_token = get_read_sas_token(filename)

        return {"sas_token": sas_token,
                "endpoint": endpoint,
                "endpoint_without_sas_token": endpoint_without_sas_token
                }, 200