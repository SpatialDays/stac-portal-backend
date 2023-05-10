from typing import Dict, List

import geoalchemy2
import shapely
from shapely.geometry import box, MultiPolygon
from sqlalchemy import or_

from .stac_service import update_existing_collection_on_stac_api, create_new_collection_on_stac_api, \
    remove_private_collection_by_id_on_stac_api
from .. import db
from ..custom_exceptions import *
from ..model.private_catalog_model import PrivateCollection
from ..util import process_timestamp
from ..util.process_timestamp import *


def _does_collection_exist_in_database(collection_id: str) -> bool:
    """Check if a collection exists in the database.

    :param: collection_id: Collection ID to check.
    :return: True if collection exists, False otherwise.
    """
    return PrivateCollection.query.filter_by(id=collection_id).first() is not None


def add_collection(collection: Dict[str, any]) -> Dict[str, any]:
    collection_id = collection["id"]
    if _does_collection_exist_in_database(collection_id):
        raise PrivateCollectionAlreadyExistsError

    if True:
        private_collection = PrivateCollection()
        private_collection.id = collection_id
        try:
            private_collection.type = collection['type']
        except KeyError:
            private_collection.type = "Collection"
        try:
            private_collection.title = collection['title']
        except KeyError:
            private_collection.title = None
        try:
            private_collection.description = collection['description']
        except KeyError:
            private_collection.description = None

        bboxes = collection['extent']['spatial']['bbox']
        shapely_boxes = []
        for i in range(0, len(bboxes)):
            shapely_box = box(*(collection['extent']['spatial']['bbox'][i]))
            shapely_boxes.append(shapely_box)
        shapely_multi_polygon = geoalchemy2.shape.from_shape(MultiPolygon(shapely_boxes), srid=4326)
        private_collection.spatial_extent = shapely_multi_polygon
        temporal_extent_start = collection['extent']['temporal']['interval'][0][0]
        temporal_extent_end = collection['extent']['temporal']['interval'][0][1]
        private_collection.temporal_extent_start = process_timestamp_single_string(temporal_extent_start)
        private_collection.temporal_extent_end = process_timestamp_single_string(temporal_extent_end)
        db.session.add(private_collection)
        try:
            status = create_new_collection_on_stac_api(collection)
            db.session.commit()
            return status
        except CollectionAlreadyExistsError:
            status = update_existing_collection_on_stac_api(collection)
            db.session.commit()
            return status
        except InvalidCollectionPayloadError:
            db.session.rollback()
            raise InvalidCollectionPayloadError


def update_collection(collection: Dict[str, any]) -> Dict[str, any]:
    collection_id = collection["id"]
    if not _does_collection_exist_in_database(collection_id):
        raise PrivateCollectionDoesNotExistError
    private_collection = PrivateCollection.query.filter_by(id=collection_id).first()
    try:
        private_collection.title = collection['title']
    except KeyError:
        pass
    private_collection.description = collection['description']
    bboxes = collection['extent']['spatial']['bbox']
    shapely_boxes = []
    for i in range(0, len(bboxes)):
        shapely_box = box(*(collection['extent']['spatial']['bbox'][i]))
        shapely_boxes.append(shapely_box)
    shapely_multi_polygon = geoalchemy2.shape.from_shape(MultiPolygon(shapely_boxes), srid=4326)
    private_collection.spatial_extent = shapely_multi_polygon
    temporal_extent_start = collection['extent']['temporal']['interval'][0][0]
    temporal_extent_end = collection['extent']['temporal']['interval'][0][1]
    private_collection.temporal_extent_start = process_timestamp_single_string(temporal_extent_start)
    private_collection.temporal_extent_end = process_timestamp_single_string(temporal_extent_end)
    try:
        status = update_existing_collection_on_stac_api(collection)
        db.session.commit()
        return status
    except PrivateCollectionDoesNotExistError:
        status = create_new_collection_on_stac_api(collection)
        db.session.commit()
        return status
    except InvalidCollectionPayloadError:
        db.session.rollback()
        raise InvalidCollectionPayloadError


def remove_collection(collection_id: str) -> Dict[str, any]:
    if not _does_collection_exist_in_database(collection_id):
        raise PrivateCollectionDoesNotExistError
    private_collection = PrivateCollection.query.filter_by(id=collection_id).first()
    db.session.delete(private_collection)
    db.session.commit()
    remove_private_collection_by_id_on_stac_api(collection_id)
    return {"status": "success"}


def search_collections(bbox: shapely.geometry.polygon.Polygon or List[float], time_interval_timestamp: str,
                       ) -> Dict[str, any] or List[any]:
    if isinstance(bbox, list):
        bbox = shapely.geometry.box(*bbox)
    a = db.session.query(PrivateCollection).filter(PrivateCollection.spatial_extent.ST_Intersects(
        f"SRID=4326;{bbox.wkt}"))

    time_start, time_end = process_timestamp.process_timestamp_dual_string(time_interval_timestamp)
    if time_start:
        a = a.filter(
            or_(PrivateCollection.temporal_extent_start == None, PrivateCollection.temporal_extent_start <= time_start))
    if time_end:
        a = a.filter(
            or_(PrivateCollection.temporal_extent_end == None, PrivateCollection.temporal_extent_end >= time_end
                ))
    data = a.all()
    grouped_data = []
    for item in data:
        item: PrivateCollection
        grouped_data.append(item.as_dict())
    return grouped_data


def get_all_collections():
    data = db.session.query(PrivateCollection).all()
    grouped_data = []
    for item in data:
        item: PrivateCollection
        grouped_data.append(item.as_dict())
    return grouped_data
