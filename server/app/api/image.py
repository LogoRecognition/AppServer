import os
from flask import request, current_app, send_file
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

        file = request.files.get('image_file')
        if file is None or file.filename == '':
            return get_message_json('No image uploaded'), HTTPStatus.BAD_REQUEST

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_dir = os.path.join(current_app.config['IMAGE_FOLDER'], 'upload')
            if not os.path.exists(file_dir):
                os.mkdir(file_dir)
            image_path = os.path.join(file_dir, filename)
            # transfer to absolute path
            image_path = os.path.abspath(image_path)
            try:
                file.save(image_path)
                res_json = {
                    'message': 'Upload image successfully',
                    'image_path': image_path
                }
                return res_json, HTTPStatus.CREATED
            except Exception as err:
                return handle_internal_error(str(err))

    @api.doc(params={'image_path': 'image file path'})
    def get(self):
        """Retrieve an image resource by file path"""
        image_path = request.args.get('image_path')
        if image_path is None:
            return get_message_json('No file path'), HTTPStatus.BAD_REQUEST
        if allowed_file(image_path) and os.path.exists(image_path):
            extension = os.path.splitext(image_path)[1][1:]
            return send_file(image_path, mimetype='image/'+extension)
        return get_message_json('invalid file path'), HTTPStatus.BAD_REQUEST
