# coding=utf-8
"""Deal with session-related APIs."""
from flask import request
from flask_restplus import Namespace, Resource
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from ..model import users
from .utils import get_message_json, handle_internal_error, HTTPStatus


api = Namespace('session')


@api.route('/')
class SessionResource(Resource):
    """Deal with user session."""

    @api.doc(parser=api.parser()
             .add_argument('body', type=str, required=True, help='json', location='json')
             )
    def post(self):
        """Create a session given username and password."""
        try:
            form = request.get_json()
            the_user = users.find_user_by_name(form['user_name'])

            if the_user is None:
                return get_message_json('User not found'), HTTPStatus.NOT_FOUND
            if not check_password_hash(the_user.password, form['password']):
                return get_message_json('Wrong password'), HTTPStatus.BAD_REQUEST

            login_user(the_user, remember=True)
            json_res = the_user.to_json()
            return json_res, HTTPStatus.OK
        except Exception as err:
            return handle_internal_error(str(err))
