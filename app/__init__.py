from flask import Blueprint
from flask_restx import Api

from .main.controller.file_controller import api as file_ns
from .main.controller.private_catalog_controller import api as collection_ns
from .main.controller.public_catalogs_contoller import api as public_catalogs_ns
from .main.controller.stac_controller import api as stac_ns
from .main.controller.stac_generator_controller import api as stac_generator_ns
from .main.controller.status_reporting_controller import api as status_controller_ns
from .main.controller.validate_controller import api as validate_ns
from .main.controller.apim_controller import api as apim_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='STAC Portal',
          version='1.0',
          description='A simple STAC Portal API')

api.add_namespace(collection_ns, path='/private_catalog')
api.add_namespace(validate_ns, path='/validate')
api.add_namespace(public_catalogs_ns, path='/public_catalogs')
api.add_namespace(status_controller_ns, path='/status_reporting')
api.add_namespace(file_ns, path='/file')
api.add_namespace(stac_generator_ns, path='/stac_generator')
api.add_namespace(stac_ns, path='/stac')
api.add_namespace(apim_ns, path='/apim')
