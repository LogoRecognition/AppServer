# coding=utf-8
"""Deal with detection-related APIs."""
from flask import request
from flask_restplus import Namespace, Resource
from http import HTTPStatus
from .utils import get_message_json, handle_internal_error

api = Namespace('detection')


@api.route('/logo_detection')
class PhotosCollectionResource(Resource):
    def post(self):
        """Recognize logos."""

        try:
            image_file = request.files['file']
            return get_message_json('头像上传成功'), HTTPStatus.OK
        except Exception as err:
            handle_internal_error(str(err))
            return get_message_json('文件解析失败'), HTTPStatus.BAD_REQUEST
