from flask_restx import Resource
from ..aad.auth_decorators import AuthDecorator
auth_decorator = AuthDecorator()