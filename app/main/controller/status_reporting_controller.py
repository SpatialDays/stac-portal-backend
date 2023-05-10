import sqlalchemy
from flask_restx import Resource

from ..service import status_reporting_service
from ..util.dto import StatusReportingDto

api = StatusReportingDto.api


@api.route('/loading_public_stac_records/')
class StacIngestionStatus(Resource):
    @api.doc(description='Get all statuses of stac ingestion statuses')
    def get(self):
        return status_reporting_service.get_all_stac_ingestion_statuses()


@api.route('/loading_public_stac_records/<string:status_id>/')
class StacIngestionStatusViaId(Resource):
    @api.doc(description='get a stac ingestion status via status_id')
    def get(self, status_id):
        try:
            return status_reporting_service.get_stac_ingestion_status_by_id(
                status_id), 200
        except AttributeError:
            return {'message': 'No result found'}, 404

    @api.doc(
        description='Delete a stac ingestion status with specified status_id')
    def delete(self, status_id):
        try:
            return status_reporting_service.remove_stac_ingestion_status_entry(
                status_id), 200
        except sqlalchemy.orm.exc.UnmappedInstanceError:
            return {'message': 'No result found to delete'}, 404
