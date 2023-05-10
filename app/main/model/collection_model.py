import shapely
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape

from .. import db


class Collection(db.Model):
    __tablename__ = "collection_abstract"
    __abstract__ = True
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False, default="Collection")
    title = db.Column(db.Text, nullable=True, default="")
    description = db.Column(db.Text, nullable=True, default="")
    temporal_extent_start = db.Column(db.DateTime, nullable=True, default=None)
    temporal_extent_end = db.Column(db.DateTime, nullable=True, default=None)
    spatial_extent = db.Column(Geometry(geometry_type="MULTIPOLYGON"), nullable=True, default=None)

    def as_dict(self):
        data = {
            c.name: str(getattr(self, c.name))
            for c in self.__table__.columns
        }
        data.pop("_id")
        data.pop("spatial_extent")
        shape: shapely.geometry.polygon.Polygon = to_shape(self.spatial_extent)
        data["spatial_extent_wkt"] = shape.wkt

        return data
