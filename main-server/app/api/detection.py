import os
import requests
from flask import request, current_app, send_file
from flask_restplus import Namespace, Resource
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from http import HTTPStatus
from .utils import get_message_json, handle_internal_error, allowed_file


api = Namespace('detection')


@api.route('/logo')
class LogoDetectionResource(Resource):
    """Deal with logo detection."""

    @api.doc(parser=api.parser().add_argument(
        'image_file', type=FileStorage, required=True, help='image file', location='files'))
    def post(self):
        """Connect to another server to detect logo."""

        file = request.files.get('image_file')
        if file is None or file.filename == '':
            return get_message_json('No image uploaded'), HTTPStatus.BAD_REQUEST

        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                file_dir = '/home/CarLogo/Faster_RCNN_TF/data/demo/'
                if not os.path.exists(file_dir):
                    os.mkdir(file_dir)
                image_path = os.path.join(file_dir, filename)
                file.save(image_path)

                # invoke another api of model server
                url = 'http://127.0.0.1:8000/detection/' + filename
                response = requests.get(url)
                if response.status_code == HTTPStatus.OK:
                    result_path = '/home/CarLogo/detect/' + filename
                    if not os.path.exists(result_path):
                        result_path = ''
                    json_res = {
                        'result_path': result_path
                    }
                    return json_res, HTTPStatus.OK
                else:
                    return get_message_json('Something wrong with the model server'), HTTPStatus.INTERNAL_SERVER_ERROR

            except Exception as err:
                return handle_internal_error(str(err))
