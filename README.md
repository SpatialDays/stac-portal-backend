# STAC Portal Backend
Backend flask-powered API for STAC-Portal. Brings all backend microservices, stac-fastapi and database togather, providing
the user a way to controll the data stored on the platform.

# Deployment

## Build Jobs

Two build jobs set up, for building both prod and dev docker image
from Dockerfile_dev and Dockerfile_prod.

## Environment variables

|Var name| Used for |
| --- | --- |
| SECRET_KEY | Secret key for flask app. |
| DEBUG | Flask debug flag. |
| SQLALCHEMY_DATABASE_URI | Sqlalchemy string pointing to Postgres database. |
| READ_STAC_API_SERVER | Endpoint for the stac-fastapi instance used for read operations. |
| WRITE_STAC_API_SERVER | Endpoint for the stac-fastapi instance used for write operations. |
| STAC_VALIDATOR_ENDPOINT | Endpoint for the stac validator microservice. |
| STAC_SELECTIVE_INGESTER_ENDPOINT | Endpoint for the stac selective ingester endpoint. |
| GDAL_INFO_API_ENDPOINT | Endpoint for the gdal info api microservice endpoint. |
| AZURE_STORAGE_CONNECTION_STRING | Connection string for Azure Storage Account. |
| AZURE_STORAGE_BLOB_NAME_FOR_STAC_ITEMS | Name of the storage blob for uploading stac items. |

## Setting up the database

Can be made from running the db.create_all() command.

Run: ```FLASK_APP=manage.py FLASK_ENV={dev,staging,prod} python3```

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

The backend is meant to be runned on Azure App Service protected by easy auth. This
will provide user login which will redirect to swagger ui where user can test out the api directly. To access the backend via frontend, the authorization header can be added with the id token from the frontend app (which can be obtained on the frontend app by
visiting /.auth/me endpoint).


