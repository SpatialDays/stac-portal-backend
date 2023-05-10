from .. import db
from ..model.collection_model import Collection


class PrivateCollection(Collection):
    __tablename__ = "private_collections"
    __mapper_args__ = {
        'polymorphic_identity': 'PrivateCollection',
    }
    id: str = db.Column(db.Text, nullable=False)
