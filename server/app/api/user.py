# coding=utf-8
"""Deal with user-related APIs."""
from flask_restplus import Namespace, Resource
from werkzeug.security import generate_password_hash
from flask import request
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from ..model import users
from .utils import *


api = Namespace('users')


@api.route('/')
class UserResource(Resource):
    """Deal with single user."""

    @api.doc(parser=api.parser()
             .add_argument('body', type=str, required=True, help='json', location='json')
             )
    def post(self):
        """Create an user."""
        try:
            form = request.get_json()
            form['password'] = generate_password_hash(form['password']),
            json_res = users.add_user(**form).to_json()
            return json_res, HTTPStatus.CREATED
        except IntegrityError:
            return get_message_json('User name already exists'), HTTPStatus.CONFLICT
        except Exception as err:
            return handle_internal_error(str(err))

    @login_required
    @api.doc(parser=api.parser()
             .add_argument('body', type=str, required=True, help='json', location='json')
             )
    def put(self):
        """Modify the info of an user."""
        try:
            form = request.get_json()
            if form.get('password'):
                form['password'] = generate_password_hash(form['password']),
            form['user_id'] = current_user.user_id
            if not users.update_user_info(**form):
                return get_message_json('User not found'), HTTPStatus.NOT_FOUND
            # TODO: update collections
            return current_user.to_json(), HTTPStatus.ACCEPTED
        except Exception as err:
            return handle_internal_error(str(err))
