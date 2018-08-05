# coding=utf-8
"""Deal with brand-heat-related APIs."""
from flask import request
from flask_login import current_user
from flask_restplus import Namespace, Resource
from http import HTTPStatus
from .utils import get_message_json, handle_internal_error
from ..model import brands, search_records

api = Namespace('brand_heat')


@api.route('/')
class BrandHeatResource(Resource):
    @api.doc(params={
        'num': 'max number of brands',
        'current_user': 'a flag indicating that only records of current user will be taken into account'
    })
    def get(self):
        """Get some heat brands."""

        try:
            num = request.args.get('num')
            if num:
                num = int(num)
            user_id = current_user.get_id() if request.args.get('current_user') == '1' else None
            result = search_records.get_heat_brands(num, user_id)
            json_res = {
                'brands': [x.to_json() for x in result]
            }
            return json_res, HTTPStatus.OK
        except Exception as err:
            return handle_internal_error(str(err))
