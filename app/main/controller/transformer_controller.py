from flask import request
from flask_restx import Resource
from werkzeug.utils import secure_filename

from ..aad.auth_decorators import AuthDecorator
from ..service.file_service import *
from ..util.dto import TransformerDto

auth_decorator = AuthDecorator()

api = TransformerDto.api


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() == "zip"


@api.route("/transform")
class Transformer(Resource):
    @api.doc(description="Transforms a shapefile zip to a new EPSG")
    @api.response(200, "Success")
    @api.expect(TransformerDto.transformer_dto, validate=True)
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def post(self):
        # get file from the request
        if "file" not in request.files:
            return {"message": "No file part in the request"}, 400
        file = request.files["file"]

        if file.filename == "":
            return {"message": "No file selected for uploading"}, 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            return {"message": "File successfully uploaded"}, 201
        else:
            return {"message": "Allowed file types are .zip"}, 400
