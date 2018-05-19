# coding=utf-8
"""Provide common utilities for API processing."""
from flask import current_app

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


def get_message_json(message):
    """Return a json with message."""
    return {'message': message}


def handle_internal_error(message):
    """
    Log unknown error and return tuple of json and status code.
    :param message: error message
    :return: tuple of json and status code
    """
    current_app.logger.exception(message)
    return get_message_json('服务器内部错误'), HTTPStatus.INTERNAL_SERVER_ERROR


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
