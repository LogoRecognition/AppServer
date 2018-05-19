import os
from flask import request, current_app
from flask_restplus import Namespace, Resource
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from http import HTTPStatus
from .utils import get_message_json, handle_internal_error, allowed_file


api = Namespace('images')


@api.route('/')
class ImageResource(Resource):
    """Deal with image upload and retrieval."""

    @api.doc(parser=api.parser().add_argument(
        'image_file', type=FileStorage, required=True, help='image file', location='files'))
    def post(self):
        """Create an image resource."""

        # check if the post request has the file part
        if 'image_file' not in request.files:
            return get_message_json('没有上传图片'), HTTPStatus.BAD_REQUEST

        file = request.files['image_file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return get_message_json('找不到图片'), HTTPStatus.BAD_REQUEST

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_dir = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(file_dir):
                os.mkdir(file_dir)
            file_path = os.path.join(file_dir, filename)
            # transfer to absolute path
            file_path = os.path.abspath(file_path)
            try:
                file.save(file_path)
                res_json = {
                    'message': '图片上传成功',
                    'file_path': file_path
                }
                return res_json, HTTPStatus.CREATED
            except Exception as err:
                return handle_internal_error(str(err))

