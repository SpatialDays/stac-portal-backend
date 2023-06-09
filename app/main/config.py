import os
import ast
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious_secret_key")
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_MASK_SWAGGER = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASS")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT")
    POSTGRES_DBNAME = os.getenv("POSTGRES_DBNAME")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"
    READ_STAC_API_SERVER = os.getenv("READ_STAC_API_SERVER")
    WRITE_STAC_API_SERVER = os.getenv("WRITE_STAC_API_SERVER")
    STAC_VALIDATOR_ENDPOINT = os.getenv("STAC_VALIDATOR_ENDPOINT")
    STAC_GENERATOR_ENDPOINT = os.getenv("STAC_GENERATOR_ENDPOINT")
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    AZURE_STORAGE_BLOB_NAME_FOR_STAC_ITEMS = os.getenv("AZURE_STORAGE_BLOB_NAME_FOR_STAC_ITEMS")
    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = int(os.getenv("REDIS_PORT"))
    AD_CLIENT_ID = os.getenv("AD_CLIENT_ID")
    AD_TENANT_ID = os.getenv("AD_TENANT_ID")
    AD_ENABLE_AUTH = bool(ast.literal_eval(os.getenv("AD_ENABLE_AUTH", "True")))  # set default to true not to break
    # existing deployments
    APIM_CONFIG_APIM_TENANT_ID = os.getenv("APIM_CONFIG_APIM_TENANT_ID")
    APIM_CONFIG_APIM_SERVICE_PRINCIPAL_CLIENT_ID = os.getenv("APIM_CONFIG_APIM_SERVICE_PRINCIPAL_CLIENT_ID")
    APIM_CONFIG_APIM_SERVICE_PRINCIPAL_CLIENT_SECRET = os.getenv("APIM_CONFIG_APIM_SERVICE_PRINCIPAL_CLIENT_SECRET")
    APIM_CONFIG_APIM_SUBSCRIPTION_ID = os.getenv("APIM_CONFIG_APIM_SUBSCRIPTION_ID")
    APIM_CONFIG_APIM_RESOURCE_GROUP_NAME = os.getenv("APIM_CONFIG_APIM_RESOURCE_GROUP_NAME")
    APIM_CONFIG_APIM_NAME = os.getenv("APIM_CONFIG_APIM_NAME")


config_by_name = dict(
    prod=ProductionConfig,
    production=ProductionConfig,
)

key = Config.SECRET_KEY
