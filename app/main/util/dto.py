#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_restx import Namespace, fields
from werkzeug.datastructures import FileStorage


class PrivateCatalogDto:
    api = Namespace("private_catalog", description="private catalog related operations")
    collection = api.model(
        "collections",
        {
            "collection_id": fields.String(
                required=True, description="collection status_id"
            ),
            "item_id": fields.String(required=True, description="item status_id"),
        },
    )

    collection_search = api.model(
        "collection_search_private",
        {
            "bbox": fields.List(
                fields.Float,
                required=True,
                description="bounding box of the area to be ingested",
                example=[-1, 50, 1, 51],
            ),
            "datetime": fields.String(
                required=True,
                description="datetime of the area to be ingested",
                example="2021-05-05T00:00:00Z/2022-05-05T00:00:00Z",
            )},
    )
    collection_dto = api.model(
        "collection_dto",
        {  # TODO: Check: Follow collection spec fully, recurse it all the way down
            # Must follow https://github.com/radiantearth/stac-spec/blob/master/collection-spec/collection-spec.md
            "type": fields.String(
                required=True, description="Collection type", example="Collection"
            ),
            "stac_version": fields.String(
                required=True, description="stac version", example="1.0.0"
            ),
            "id": fields.String(
                required=True,
                description="collection id",
                example="custom-landsat-c2-l2",
            ),
            "description": fields.String(
                required=True,
                description="collection description",
                example="Custom Landsat Collection 2 Level 2",
            ),
            "license": fields.String(
                required=True, description="collection license", example="proprietary"
            ),
            # "extent": fields.Nested(
            #     api.model(
            #         "extent",
            #         {
            #             "spatial": fields.Nested(
            #                 api.model(
            #                     "spatial",
            #                     {
            #                         "bbox": fields.List(
            #                             fields.List(fields.Float),
            #                             required=True,
            #                             description="bbox",
            #                             example=[[-180, -90, 180, 90]],
            #                         )
            #                     },
            #                 ),
            #                 required=True,
            #                 description="spatial",
            #             ),
            #             "temporal": fields.Nested(
            #                 api.model(
            #                     "temporal",
            #                     {
            #                         "interval": fields.List(
            #                             fields.List(any),
            #                             required=True,
            #                             description="interval",
            #                             example=[
            #                                 [
            #                                     "2021-05-05T00:00:00Z",
            #                                     "2022-05-05T00:00:00Z",
            #                                 ]
            #                             ],
            #                         ),
            #                     },
            #                 )
            #             ),
            #         },
            #     ),
            #     required=True,
            #     description="spatial and temporal extent",
            # ),
        },
    )
    item_dto = api.model(
        "item_dto",
        {  # TODO: Check: Follow collection spec fully, recurse it all the way down
            # Must follow https://github.com/radiantearth/stac-spec/blob/master/item-spec/item-spec.md
            "type": fields.String(
                required=True, description="Item type", example="Feature"
            ),
            "stac_version": fields.String(
                required=True, description="stac version", example="1.0.0"
            ),
            "id": fields.String(
                required=True,
                description="item id",
                example="LC08_L2SP_20210505_20210505_02_RT",
            ),
            "bbox": fields.List(
                fields.Float,
                required=False,
                description="bbox",
                example=[-180, -90, 180, 90],
            ),
            "geometry": fields.Nested(
                api.model(
                    "geometry",
                    {
                        "type": fields.String(
                            required=True,
                            description="geometry type",
                            example="Polygon",
                        ),
                        "coordinates": fields.List(
                            fields.List(fields.List(fields.Float)),
                            required=True,
                            description="geometry coordinates",
                            example=[
                                [
                                    [-180, -90],
                                    [-180, 90],
                                    [180, 90],
                                    [180, -90],
                                    [-180, -90],
                                ]
                            ],
                        ),
                    },
                ),
                required=False,
                description="geometry",
            ),
            "properties": fields.Nested(
                api.model(
                    "properties",
                    {
                        "datetime": fields.String(
                            required=True,
                            description="datetime",
                            example="2021-05-05T00:00:00Z",
                        )
                    },
                ),
                required=True,
            ),
        },
    )


class ValidateDto:
    api = Namespace("validate", description="validate related operations")
    validate = api.model(
        "validate",
        {"json": fields.Raw(required=True, description="JSON object to validate")},
    )  # takes a JSON object


class PublicCatalogsDto:
    api = Namespace("public_catalogs", description="public catalogs related operations")
    add_public_catalog = api.model(
        "add_public_catalog",
        {
            "name": fields.String(
                required=True,
                description="name of the public catalog",
                example="Microsoft Planetary Computer",
            ),
            "url": fields.String(
                required=True,
                description="url of the public catalog",
                example="https://planetarycomputer.microsoft.com/api/stac/v1",
            ),
            "description": fields.String(
                required=True,
                description="description of the public catalog",
                example="The Planetary Computer is a cloud-based platform for planetary-scale geospatial data processing and analysis.",
            ),
            "stac_version": fields.String(
                required=True,
                description="STAC version of the public catalog",
                example="1.0.0",
            ),
        },
    )
    start_stac_ingestion = api.model(
        "start_stac_ingestion",
        {
            "update": fields.Boolean(
                required=True, description="update the destination catalog"
            ),
            "bbox": fields.List(
                fields.Float,
                required=False,
                description="bounding box of the area to be ingested",
                example=[-1, 50, 1, 51],
            ),
            "datetime": fields.String(
                required=False,
                description="datetime of the area to be ingested",
                example="2021-05-05T00:00:00Z/2022-05-05T00:00:00Z",
            ),
            "collections": fields.List(
                fields.String,
                required=False,
                description="collections to be ingested",
                example=["landsat-8-l1-c1", "sentinel-2-l1c", "landsat-c2-l2"],
            ),
            # 'intersects': fields.String(required=False,
            #                             description='geojson of the area to be ingested'
            #                             , example='{}'),
            # 'ids': fields.List(fields.String, required=False,
            #                    description='ids of the items to be ingested'
            #                    , example=[]),
        },
    )
    update_stac_collections_specify_collection_ids = api.model(
        "update_stac_collections_specify_collection_ids",
        {
            "collections": fields.List(
                fields.String,
                required=True,
                default=[],
                example=["landsat-8-l1-c1", "sentinel-2-l1c", "landsat-c2-l2"],
            )
        },
    )
    update_stac_collections_via_catalog_url = api.model(
        "update_stac_collections_via_catalog_url",
        {
            "source_catalog_url": fields.String(
                required=True,
                description="Url of the source catalog in the database",
                example="https://planetarycomputer.microsoft.com/api/stac/v1",
            ),
            "collections": fields.List(
                fields.String,
                required=False,
                default=[],
                example=["landsat-8-l1-c1", "sentinel-2-l1c", "landsat-c2-l2"],
            ),
        },
    )
    collection_search = api.model(
        "collection_search",
        {
            "bbox": fields.List(
                fields.Float,
                required=False,
                description="bounding box of the area to be ingested",
                example=[-1, 50, 1, 51],
            ),
            "datetime": fields.String(
                required=False,
                description="datetime of the area to be ingested",
                example="2021-05-05T00:00:00Z/2022-05-05T00:00:00Z",
            )},
    )


class StatusReportingDto:
    api = Namespace(
        "status_reporting", description="Status reporting related operations"
    )
    stac_ingestion_status_post = api.model(
        "stac_ingestion_status_post",
        {
            "newly_stored_collections_count": fields.Integer(
                required=True, description="number of newly stored collections"
            ),
            "newly_stored_collections": fields.List(
                fields.String, required=True, description="newly stored collections"
            ),
            "updated_collections_count": fields.Integer(
                required=True, description="updated collections count"
            ),
            "updated_collections": fields.List(
                fields.String, required=True, description="updated collections"
            ),
            "newly_stored_items_count": fields.Integer(
                required=True, description="newly stored items count"
            ),
            "updated_items_count": fields.Integer(
                required=True, description="updated items count"
            ),
            "already_stored_items_count": fields.Integer(
                required=True, description="already stored items count"
            ),
        },
    )


class FileDto:
    api = Namespace("files", description="File upload related operations")
    file_upload = api.parser()
    file_upload.add_argument("file", location="files", type=FileStorage, required=True)


class FilesDto:
    files_api = Namespace('files', description='File upload related operations')
    files_upload = files_api.parser()
    files_upload.add_argument('files', location='files', type=FileStorage, required=True, action='append')


class GdalInfoDto:
    api = Namespace("gdal_info", description="gdalinfo related operations")
    get_gdal_info = api.model(
        "gdalinfo",
        {
            "file_url": fields.String(
                required=True,
                description="url of the file to get the stac info for",
                example="https://ctpltstacstrgdev.blob.core.windows.net/stac-items/LC09_L2SP_202024_20220810_20220812_02_T1_SR_B4.tiff",
            ),
        },
    )


class StacDto:
    api = Namespace("stac", description="stac related operations")


class StacGeneratorDto:
    api = Namespace('stac_generator', description='stac generator related operations')
    # Takes an array of metadata JSON
    stac_generator = api.model('stac_generator', {
        'metadata': fields.List(fields.String, required=True, description='metadata json'),
        'stac_version': fields.String(required=False, description='stac version', example='1.0.0'),
        'stac_extensions': fields.List(fields.String, required=False, description='stac extensions', example=['eo']),
        'stac_collection': fields.String(required=False, description='stac collection', example='landsat-8-l1-c1'),
    })
    item_search = api.model(
        "item_search",
        {
            "collections": fields.List(
                fields.String,
                required=False,
                default=[],
                example=["landsat-8-l1-c1", "sentinel-2-l1c", "landsat-c2-l2"],
            ),
            "bbox": fields.List(
                fields.Float,

                required=False,
                description="bounding box of the area to be ingested",
                example=[-1, 50, 1, 51],
            ),
            "datetime": fields.String(
                required=False,
                description="datetime of the area to be ingested",
                example="2021-05-05T00:00:00Z/2022-05-05T00:00:00Z",
            ),
            "ids": fields.List(
                fields.String,
                required=False,
                default=[],
                example=["LC08_L2SP_202024_20220810_20220812_02_T1_SR_B4"],
            ),
            "limit": fields.Integer(
                required=False,
                default=10,
                description="maximum number of items to return",
                example=10,
            ),
            "intersects": fields.String(
                required=False,
                description="geojson of the area to be ingested",
                example="{}",
            )},
    )
    collection_search = api.model(
        "collection_search_2",
        {
            "collections": fields.List(
                fields.String,
                required=False,
                default=[],
                example=["landsat-8-l1-c1", "sentinel-2-l1c", "landsat-c2-l2"],
            ),
            "bbox": fields.List(
                fields.Float,
                required=False,
                description="bounding box of the area to be ingested",
                example=[-1, 50, 1, 51],
            ),
            "datetime": fields.String(
                required=False,
                description="datetime of the area to be ingested",
                example="2021-05-05T00:00:00Z/2022-05-05T00:00:00Z",
            )},
    )
