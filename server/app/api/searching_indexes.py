# coding=utf-8
"""Deal with searching-indexes-related APIs."""
from flask_restplus import Namespace, Resource
from flask import request
from http import HTTPStatus
import datetime
from .utils import get_message_json, handle_internal_error
from ..model import brands, search_records

api = Namespace('searching_indexes')


@api.route('/')
class SearchingIndexesResource(Resource):
    @api.doc(params={
        'brand_name': 'a single brand name',
        'month_start': 'starting month',
        'month_end': 'ending month',
    })
    def get(self):
        """Get searching champions of each recent month."""

        try:
            brand_name = request.args.get('brand_name')
            month_start = request.args.get('month_start')
            month_end = request.args.get('month_end')
            json_res = search_records.get_recent_search_champions(brand_name, month_start, month_end)
            return json_res, HTTPStatus.OK
        except Exception as err:
            return handle_internal_error(str(err))
