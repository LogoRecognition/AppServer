# coding=utf-8
"""
Initialize `api` module.

Refer to http://flask-restplus.readthedocs.io/en/stable/scaling.html
"""
from flask_restplus import Api

from .image import api as image_ns

api = Api(
    title='LogoRecognition',
    version='1.0'
)

# `path` is somehow required
api.add_namespace(image_ns, path='/images')
