# coding=utf-8
"""Deal with brand-related APIs."""
from flask_restplus import Namespace, Resource
from flask_login import current_user
from http import HTTPStatus
from .utils import get_message_json, handle_internal_error
from ..model import brands, search_records, classic_goods

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
            json_res['classic_goods'] = \
                [{'name': x.name, 'image': x.image}
                 for x in classic_goods.find_list_of_classic_goods_by_brand_name(the_brand.name)]
            search_records.add_record(the_brand.name, current_user.get_id())
            return json_res, HTTPStatus.OK
        except Exception as err:
            return handle_internal_error(str(err))
