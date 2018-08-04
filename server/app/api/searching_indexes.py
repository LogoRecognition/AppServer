# coding=utf-8
"""Deal with searching-indexes-related APIs."""
from flask_restplus import Namespace, Resource
from http import HTTPStatus
import datetime
from .utils import get_message_json, handle_internal_error
from ..model import brands, search_records

api = Namespace('searching_indexes')


@api.route('/')
class SearchingIndexesResource(Resource):
    def get(self):
        """Get searching champions of each recent month."""

        try:
            json_res = search_records.get_recent_search_champions_by_month()
            return json_res, HTTPStatus.OK
        except Exception as err:
            return handle_internal_error(str(err))
