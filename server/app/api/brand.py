# coding=utf-8
"""Deal with brand-related APIs."""
from flask_restplus import Namespace, Resource
from http import HTTPStatus
from .utils import get_message_json, handle_internal_error
from ..model import brands, search_records

api = Namespace('brand')


@api.route('/<string:name>')
class BrandResource(Resource):
    def get(self, name):
        """Retrieve basic info of a brand by name."""

        try:
            the_brand = brands.find_brand_by_name(name)
            if the_brand is None:
                return get_message_json('Brand not found'), HTTPStatus.NOT_FOUND
            json_res = the_brand.to_json()
            json_res['classic_goods'] = []
            search_records.add_record(the_brand.name)
            return json_res, HTTPStatus.OK
        except Exception as err:
            return handle_internal_error(str(err))
