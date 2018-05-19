# coding=utf-8
"""Provide common utilities for API processing."""
from flask import current_app


class DBErrorCodes(object):
    """
    Collect MySQL error codes that are used in this project.

    Refer to
    https://dev.mysql.com/doc/refman/8.0/en/error-messages-server.html
    """
    # Duplicate entry for unique key
    DUPLICATE_ENTRY = 1062


DB_ERR_CODES = DBErrorCodes()


class HttpCodes(object):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500


HTTPStatus = HttpCodes()


class ConstantCodes(object):
    # Authority 1XX
    Empty = 100
    Admin = 101
    Doctor = 102
    Guest = 103
    # Job State 2XX
    Unlabeled = 200
    Labeling = 201
    Finished = 202
    # Image State 3XX
    Unassigned = 300
    Running = 301
    Different = 302
    Done = 303


ConstCodes = ConstantCodes()


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
