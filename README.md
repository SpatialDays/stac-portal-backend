# STAC Portal Backend

Backend flask-powered API for STAC-Portal. Brings together all backend microservices, stac-fastapi, and the database, providing users a way to control the data stored on the platform.

## Deployment

### Build Jobs

Two build jobs are set up for building both prod and staging docker images.

### Environment variables

| Var name                               | Used for                                                          |
| -------------------------------------- | ----------------------------------------------------------------- |
| POSTGRES_USER                          | PostgreSQL username.                                             |
| POSTGRES_PASSWORD                      | PostgreSQL password.                                             |
| POSTGRES_HOST                          | PostgreSQL host.                                                 |
| POSTGRES_PORT                          | PostgreSQL port.                                                 |
| POSTGRES_DBNAME                        | PostgreSQL database name.                                        |
| SQLALCHEMY_DATABASE_URI                | Sqlalchemy string pointing to the PostgreSQL database.            |
| READ_STAC_API_SERVER                   | Endpoint for the stac-fastapi instance used for read operations.   |
| WRITE_STAC_API_SERVER                  | Endpoint for the stac-fastapi instance used for write operations.  |
| STAC_VALIDATOR_ENDPOINT                | Endpoint for the STAC validator microservice.                      |
| STAC_SELECTIVE_INGESTER_ENDPOINT       | Endpoint for the STAC selective ingester.                          |
| GDAL_INFO_API_ENDPOINT                 | Endpoint for the gdal info API microservice.                       |
| STAC_GENERATOR_ENDPOINT                | Endpoint for the STAC generator.                                   |
| AZURE_STORAGE_CONNECTION_STRING        | Connection string for Azure Storage Account.                       |
| AZURE_STORAGE_BLOB_NAME_FOR_STAC_ITEMS | Name of the storage blob for uploading STAC items.                 |
| REDIS_HOST                             | Redis host.                                                       |
| REDIS_PORT                             | Redis port.                                                       |
| AD_CLIENT_ID                           | Azure AD client ID.                                               |
| AD_TENANT_ID                           | Azure AD tenant ID.                                               |
| AD_ENABLE_AUTH                         | Flag to enable Azure AD authentication.                            |
| APIM_CONFIG_APIM_TENANT_ID             | Azure API Management tenant ID.                                    |
| APIM_CONFIG_APIM_SERVICE_PRINCIPAL_CLIENT_ID   | Azure API Management service principal client ID.           |
| APIM_CONFIG_APIM_SERVICE_PRINCIPAL_CLIENT_SECRET | Azure API Management service principal client secret.      |
| APIM_CONFIG_APIM_SUBSCRIPTION_ID       | Azure API Management subscription ID.                              |
| APIM_CONFIG_APIM_RESOURCE_GROUP_NAME   | Azure API Management resource group name.                          |
| APIM_CONFIG_APIM_NAME                  | Azure API Management name.                                         |

### Setting up the database

The database can be set up by running the `db.create_all()` command.

Run: 
```bash
FLASK_APP=manage.py FLASK_ENV={dev,staging,prod} python3
```

```python
>>> from manage import *
>>> db.create_all()
>>> db.session.commit()
```

## Setting up the database using migrations

``` bash
FLASK_APP=manage.py python3 manage.py db migrate
FLASK_APP=manage.py python3 manage.py db upgrade
```

## Authorization
The backend is meant to be run on Azure App Service protected by easy auth. This will provide user login, which will redirect to the Swagger UI where users can test out the API directly. To access the backend via the frontend, the authorization header can be added with the ID token from the frontend app (which can be obtained on the frontend app by visiting the /.auth/me endpoint).


