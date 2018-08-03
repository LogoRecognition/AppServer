# coding=utf-8
"""
Initialize `api` module.

Refer to http://flask-restplus.readthedocs.io/en/stable/scaling.html
"""
from flask_restplus import Api

from .image import api as image_ns
from .brand import api as brand_ns
from .brand_heat import api as brand_heat_ns

api = Api(
    title='LogoRecognition',
    version='1.0'
)

# `path` is somehow required
api.add_namespace(image_ns, path='/images')
api.add_namespace(brand_ns, path='/brand')
api.add_namespace(brand_heat_ns, path='/brand_heat')
