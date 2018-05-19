# coding=utf-8
"""Deal with image-related APIs."""
from sqlalchemy.exc import IntegrityError
from flask import request, current_app
from flask_restplus import Namespace, Resource
from flask_login import login_required
from werkzeug.security import check_password_hash
from ..model import images
from .utils import get_message_json, handle_internal_error, DB_ERR_CODES, HTTPStatus


api = Namespace('images')

test_mode = True
""" ---------- These are for Testing ----------- """
SINGLE_IMAGE_RESPONSE = {
    'message': '',
    'id': 10,
    'filename': 'test.png',
    'state': 0,
    'ground_truth_id': 1234,
    'source': 'abcde'
}
COLLECTION_RESPONSE = {
    'message': '',
    'data':
        [
            {
                'id': 100,
                'filename': 'test1.png',
                'state': 0,
                'ground_truth_id': 1234,
                'source': 'abcde'
            },{
                'id': 101,
                'filename': 'test2.png',
                'state': 1,
                'ground_truth_id': 1244,
                'source': 'zxcvb'
            }
        ]
}
""" -------------------------------------------- """

@api.route('/<int:image_id>')
class ImageResource(Resource):
    """Deal with single image."""
    
    @login_required
    def get(self, image_id):
        if test_mode:
            SINGLE_IMAGE_RESPONSE['message'] = '图片获取成功'
            return SINGLE_IMAGE_RESPONSE, HTTPStatus.OK

        """Retrieve a single image by id."""
        try:
            image_list = images.find_image_by_id(image_id)
            if image_list:
                json_res = image_list[0].to_json()
                json_res['message'] = '图片获取成功'
                return json_res, HTTPStatus.OK
            else:
                return get_message_json('图片不存在'), HTTPStatus.NOT_FOUND
        except IntegrityError as err:
                return handle_internal_error(err.orig.args[1])
        except Exception as err:
            return handle_internal_error(str(err))
    
    @api.doc(parser=api.parser()
             .add_argument('body', type=str, required=True, help='json', location='json')
            )
    @login_required
    def put(self, image_id):
        if test_mode:
            SINGLE_IMAGE_RESPONSE['message'] = '图片更新成功'
            return SINGLE_IMAGE_RESPONSE, HTTPStatus.OK
        
        """Edit a single image by id."""
        form = request.form
        try:
            if images.find_image_by_id(image_id):
                image_list = images.update_image_by_id(
                    image_id,
                    form['filename'],
                    form['state'],
                    form['ground_truth_id'],
                    form['source']
                )
                json_res = image_list[0].to_json()
                json_res['message'] = '图片更新成功'
                return json_res, HTTPStatus.OK
            else:
                return get_message_json('图片未创建'), HTTPStatus.NOT_FOUND

        except IntegrityError as err:
            return handle_internal_error(err.orig.args[1])

        except Exception as err:
            return handle_internal_error(str(err))

    @login_required
    def delete(self, image_id):
        if test_mode:
            return {'message': '图片删除成功'}, HTTPStatus.OK

        """Delete a single image by id."""
        try:
            images.delete_image_by_id(image_id)
            return get_message_json('图片删除成功'), HTTPStatus.NO_CONTENT
        
        except IntegrityError as err:
            return handle_internal_error(err.orig.args[1])

        except Exception as err:
            return handle_internal_error(str(err))


@api.route('/')
class ImagesCollectionResource(Resource):
    """Deal with collection of images."""

    @login_required
    def get(self):
        if test_mode:
            COLLECTION_RESPONSE['message'] = '图片集合获取成功'
            return COLLECTION_RESPONSE, HTTPStatus.OK
        
        """List all images."""
        state = request.args.get('state')
        try:
            state_list = images.find_images_by_state(state)
            json_res = {}
            json_res['message'] = '图片集合获取成功'
            json_res['data'] = state_list
            return json_res, HTTPStatus.NO_CONTENT
        
        except IntegrityError as err:
            return handle_internal_error(err.orig.args[1])

        except Exception as err:
            return handle_internal_error(str(err))
    
    @login_required
    @api.doc(parser=api.parser()
             .add_argument('body', type=str, required=True, help='json', location='json')
            )
    def post(self):
        if test_mode:
            SINGLE_IMAGE_RESPONSE['message'] = '图片创建成功'
            return SINGLE_IMAGE_RESPONSE, HTTPStatus.OK
        
        """Create an image."""
        form = request.form
        try:
            image_list = images.add_image(
                form['filename'],
                form['state'],
                form['source']
            )
            json_res = image_list[0].to_json()
            json_res['message'] = '图片创建成功'

            return json_res, HTTPStatus.CREATED
        except IntegrityError as err:
            if err.orig.args[0] == DB_ERR_CODES.DUPLICATE_ENTRY:
                return get_message_json('图片已存在'), HTTPStatus.CONFLICT
            else:
                return handle_internal_error(err.orig.args[1])

        except Exception as err:
            return handle_internal_error(str(err))
        
