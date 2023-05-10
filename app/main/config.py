import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "my_precious_secret_key")
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_MASK_SWAGGER = False
    AZURE_STORAGE_BLOB_NAME_FOR_STAC_ITEMS = os.getenv(
        "AZURE_STORAGE_BLOB_NAME_FOR_STAC_ITEMS", "stac-items"
    )


class ProductionConfig(Config):
    DEBUG = False
    POSTGRES_USER = os.getenv("POSTGRES_USER", "")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASS", "")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DBNAME = os.getenv("POSTGRES_DBNAME", "")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DBNAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    READ_STAC_API_SERVER = os.getenv("READ_STAC_API_SERVER", "")
    WRITE_STAC_API_SERVER = os.getenv("WRITE_STAC_API_SERVER", "")
    STAC_VALIDATOR_ENDPOINT = os.getenv("STAC_VALIDATOR_ENDPOINT", "")
    STAC_SELECTIVE_INGESTER_ENDPOINT = os.getenv("STAC_SELECTIVE_INGESTER_ENDPOINT", "")
    GDAL_INFO_API_ENDPOINT = os.getenv("GDAL_INFO_API_ENDPOINT", "")
    AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "")


config_by_name = dict(
    prod=ProductionConfig,
    production=ProductionConfig,
)

key = Config.SECRET_KEY
