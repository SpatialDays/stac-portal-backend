from flask import request
from flask_restx import Resource
from werkzeug.utils import secure_filename
from typing import Tuple

from ..aad.auth_decorators import AuthDecorator
from ..service.transformer_service import send_file_to_transformer
from ..util.dto import TransformerDto

ALLOWED_EXTENSIONS = {"zip"}
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_UNPROCESSABLE_ENTITY = 422

auth_decorator = AuthDecorator()
api = TransformerDto.api


def allowed_file(filename: str) -> bool:
    """Check if the file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@api.route("/")
class Transformer(Resource):
    @api.doc(description="Transforms a shapefile zip to a new EPSG")
    @api.response(200, "Success")
    @auth_decorator.header_decorator(
        allowed_roles=["StacPortal.Viewer", "StacPortal.Creator"]
    )
    def post(self) -> Tuple[dict, int]:
        """Handle POST request for transforming shapefiles."""
        if "file" not in request.files:
            return {"message": "No file part in the request"}, HTTP_STATUS_BAD_REQUEST
        shapefile = request.files["file"]

        if shapefile.filename == "":
            return {
                "message": "No file selected for uploading"
            }, HTTP_STATUS_BAD_REQUEST

        if not allowed_file(shapefile.filename):
            return {
                "message": "Invalid file type. Only .zip files are allowed."
            }, HTTP_STATUS_UNPROCESSABLE_ENTITY

        output_epsg = request.form.get("output_epsg")
        if not output_epsg:
            return {
                "message": "Missing 'output_epsg' in form data."
            }, HTTP_STATUS_UNPROCESSABLE_ENTITY

        res = send_file_to_transformer(shapefile, output_epsg)

        return res.json(), res.status_code
