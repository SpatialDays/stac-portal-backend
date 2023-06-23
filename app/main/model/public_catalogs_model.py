import datetime

from .. import db


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
