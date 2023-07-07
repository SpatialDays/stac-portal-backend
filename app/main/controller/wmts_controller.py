from flask_restx import Resource
from ..util.dto import WMTSDto
from ..aad.auth_decorators import AuthDecorator

auth_decorator = AuthDecorator()

api = WMTSDto.api


@api.route("/<string:collection_id>/items/<string:item_id>/")
class GetWMTSUrlsForItem(Resource):
    def get(self, collection_id: str, item_id: str):
        pass
