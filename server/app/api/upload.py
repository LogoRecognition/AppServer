import os
from flask import request, current_app
from flask_restplus import Namespace, Resource
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from ..model import accounts
from .utils import get_message_json, handle_internal_error, HTTPStatus

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

api = Namespace('uploads')


@login_required
@api.route('/photos')
class PhotosCollectionResource(Resource):
    """Deal with collection of accounts' photos."""
    
    # @api.doc(parser=api.parser()
    #          .add_argument('body', type=str, required=True, help='json', location='json')
    #         )
    def post(self):
        """Create an account."""

        try:
            photo_file = request.files['file']
            photo_filename = secure_filename(photo_file.filename)

        except Exception as err:
            return get_message_json('文件解析失败'), HTTPStatus.BAD_REQUEST

        
        try:
            photo_location = os.path.join(os.environ['HOME'], current_app.config['PHOTOS_FOLDER'])
            photo_file.save(os.path.join(photo_location, photo_filename))

            return get_message_json('头像上传成功'), HTTPStatus.OK

        except Exception as err:
            return handle_internal_error(str(err))


@login_required
@api.route('/medical-images')
class MedicalImagesCollectionResource(Resource):
    """Deal with collection of accounts' photos."""
    
    # @api.doc(parser=api.parser()
    #          .add_argument('body', type=str, required=True, help='json', location='json')
    #         )
    def post(self):
        """Create an account."""

        try:
            photo_file = request.files['file']
            photo_filename = secure_filename(photo_file.filename)

        except Exception as err:
            return get_message_json('文件解析失败'), HTTPStatus.BAD_REQUEST

        
        try:
            photo_location = os.path.join(os.environ['HOME'], current_app.config['MEDICAL_IMAGES_FOLDER'])
            photo_file.save(os.path.join(photo_location, photo_filename))

            return get_message_json('医学影像上传成功'), HTTPStatus.OK

        except Exception as err:
            return handle_internal_error(str(err))