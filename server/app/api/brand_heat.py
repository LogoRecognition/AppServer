# coding=utf-8
"""Deal with brand-heat-related APIs."""
from flask import request
from flask_restplus import Namespace, Resource
from http import HTTPStatus
from .utils import get_message_json, handle_internal_error
from ..model import brands, search_records

api = Namespace('brand_heat')


@api.route('/')
class BrandHEATResource(Resource):
    @api.doc(params={'num': 'max number of brands'})
    def get(self):
        """Get some heat brands."""

        try:
            num = request.args.get('num')
            if num:
                num = int(num)
            result = search_records.get_heat_brands(num)
            json_res = {
                'brands': [x.to_json() for x in result]
            }
            return json_res, HTTPStatus.OK
        except Exception as err:
            return handle_internal_error(str(err))
