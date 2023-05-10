import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESTX_MASK_SWAGGER = False
    AZURE_STORAGE_BLOB_NAME_FOR_STAC_ITEMS = os.getenv('AZURE_STORAGE_BLOB_NAME_FOR_STAC_ITEMS', "stac-items")


class DevelopmentConfig(Config):
    # here are variables available only for development environment
    DEBUG = True
    ENV = "Dev"
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI",
                                        "postgresql://postgres:postgres@localhost:5432/postgres")
    READ_STAC_API_SERVER = os.getenv('READ_STAC_API_SERVER', "http://localhost:8082")
    WRITE_STAC_API_SERVER = os.getenv('WRITE_STAC_API_SERVER', "http://localhost:8082")
    STAC_VALIDATOR_ENDPOINT = os.getenv('STAC_VALIDATOR_ENDPOINT', "http://localhost:7000")
    STAC_SELECTIVE_INGESTER_ENDPOINT = os.getenv('STAC_SELECTIVE_INGESTER_ENDPOINT', "http://localhost:7001")
    GDAL_INFO_API_ENDPOINT = os.getenv('GDAL_INFO_API_ENDPOINT',
                                       "https://ctplt-pda-rg-dev-gdal-info-api.azurewebsites.net")
    AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING',
                                                "")


class StagingConfig(Config):
    DEBUG = False
    ENV = "Staging"
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI",
                                        "postgresql://postgres:postgres@ctplt-pda-rg-dev-psqlflexibleserver.postgres.database.azure.com:5432/stacportaldb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    READ_STAC_API_SERVER = os.getenv('READ_STAC_API_SERVER',
                                     "http://ctplt-pda-rg-dev-stac-api-server.azurewebsites.net/")
    WRITE_STAC_API_SERVER = os.getenv('WRITE_STAC_API_SERVER',
                                      "http://ctplt-pda-rg-dev-stac-api-server-writer.azurewebsites.net/")
    STAC_VALIDATOR_ENDPOINT = os.getenv('STAC_VALIDATOR_ENDPOINT',
                                        "http://stac-validator-api.microservices.ctplt-pda-rg-dev.azure.com")
    STAC_SELECTIVE_INGESTER_ENDPOINT = os.getenv('STAC_SELECTIVE_INGESTER_ENDPOINT',
                                                 "http://stac-api-selective-ingester.microservices.ctplt-pda-rg-dev.azure.com/")
    GDAL_INFO_API_ENDPOINT = os.getenv('GDAL_INFO_API_ENDPOINT',
                                       "http://gdal-info-api.microservices.ctplt-pda-rg-dev.azure.com")
    AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING', "")


class ProductionConfig(Config):
    DEBUG = False
    ENV = "Production"
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI",
                                        "postgresql://postgres:postgres@ctplt-pda-rg-prod-psqlflexibleserver.postgres.database.azure.com:5432/stacportaldb")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    READ_STAC_API_SERVER = os.getenv('READ_STAC_API_SERVER',
                                     "http://ctplt-pda-rg-prod-stac-api-server.azurewebsites.net/")
    WRITE_STAC_API_SERVER = os.getenv('WRITE_STAC_API_SERVER',
                                      "http://ctplt-pda-rg-prod-stac-api-server-writer.azurewebsites.net/")
    STAC_VALIDATOR_ENDPOINT = os.getenv('STAC_VALIDATOR_ENDPOINT',
                                        "http://stac-validator-api.microservices.ctplt-pda-rg-prod.azure.com")
    STAC_SELECTIVE_INGESTER_ENDPOINT = os.getenv('STAC_SELECTIVE_INGESTER_ENDPOINT',
                                                 "http://stac-api-selective-ingester.microservices.ctplt-pda-rg-prod.azure.com/")
    GDAL_INFO_API_ENDPOINT = os.getenv('GDAL_INFO_API_ENDPOINT',
                                       "http://gdal-info-api.microservices.ctplt-pda-rg-prod.azure.com")
    AZURE_STORAGE_CONNECTION_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING', "")


config_by_name = dict(
    dev=DevelopmentConfig,
    development=DevelopmentConfig,
    staging=StagingConfig,
    prod=ProductionConfig,
    production=ProductionConfig)

key = Config.SECRET_KEY
