from flask_restx import Resource

from ..aad.auth_decorators import AuthDecorator
from ..service.file_service import *
from ..util.dto import FileDto, FilesDto

auth_decorator = AuthDecorator()