import datetime
import json

from .. import db
from ..model.collection_model import Collection


class PublicCatalog(db.Model):
    __tablename__ = "public_catalogs"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.Text, nullable=False)
    url: str = db.Column(db.Text, nullable=False, unique=True)
    description: str = db.Column(db.Text, nullable=True)
    added_on: datetime.datetime = db.Column(db.DateTime,
                                            nullable=False,
                                            default=datetime.datetime.utcnow)
    stored_search_parameters = db.relationship("StoredSearchParameters", backref="public_catalogs", lazy="dynamic",
                                               cascade="all, delete-orphan")
    stored_ingestion_statuses = db.relationship("StacIngestionStatus", backref="public_catalogs", lazy="dynamic",
                                                cascade="all, delete-orphan")
    collections = db.relationship("PublicCollection", backref="public_catalogs", lazy="dynamic",
                                  cascade="all, delete-orphan")

    def get_number_of_stored_search_parameters(self):
        return StoredSearchParameters.query.filter_by(
            associated_catalog_id=self.id).count()

    def as_dict(self):
        data = {
            c.name: str(getattr(self, c.name))
            for c in self.__table__.columns
        }

        data[
            "number_of_stored_search_parameters_associated"] = self.get_number_of_stored_search_parameters(
        )
        return data


class PublicCollection(Collection):
    __tablename__ = "public_collections"
    __mapper_args__ = {
        'polymorphic_identity': 'PublicCollection',
    }
    parent_catalog = db.Column(db.Integer, db.ForeignKey("public_catalogs.id", ondelete='CASCADE'), nullable=False)
    __table_args__ = (db.UniqueConstraint('id', 'parent_catalog', name='_id_parent_catalog_uc'),)

    def as_dict(self):
        data = super().as_dict()
        data["parent_catalog"] = self.parent_catalog
        return data


class StoredSearchParameters(db.Model):
    __tablename__ = "stored_search_parameters"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bbox = db.Column(db.Text, nullable=True, default="[]")
    datetime = db.Column(db.Text, nullable=True, default="")
    collection = db.Column(db.Text, nullable=True, default="")
    used_search_parameters: str = db.Column(db.Text,
                                            nullable=False,
                                            unique=True)
    associated_catalog_id: int = db.Column(db.Integer,
                                           db.ForeignKey('public_catalogs.id',
                                                         ondelete='CASCADE'),
                                           nullable=False,
                                           index=True)

    def as_dict(self):
        data = {}
        data["collection"] = self.collection
        try:
            data["bbox"] = json.loads(self.bbox)
        except json.decoder.JSONDecodeError:
            data["bbox"] = []
        try:
            data["datetime"] = json.loads(self.datetime)
        except json.decoder.JSONDecodeError:
            data["datetime"] = ""
        try:
            data["used_search_parameters"] = json.loads(self.used_search_parameters)
        except json.decoder.JSONDecodeError:
            data["used_search_parameters"] = ""
        data["associated_catalog_id"] = self.associated_catalog_id
        data["id"] = self.id
        return data
