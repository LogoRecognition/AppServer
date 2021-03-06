# coding=utf-8
"""
Initialize `api` module.

Refer to http://flask-restplus.readthedocs.io/en/stable/scaling.html
"""
from flask_restplus import Api

from .image import api as image_ns
from .brand import api as brand_ns
from .brand_heat import api as brand_heat_ns
from .searching_indexes import api as searching_indexes_ns
from .user import api as user_ns
from .session import api as session_ns
from .detection import api as detection_ns

api = Api(
    title='LogoRecognition',
    version='1.0'
)

# `path` is somehow required
api.add_namespace(image_ns, path='/images')
api.add_namespace(brand_ns, path='/brand')
api.add_namespace(brand_heat_ns, path='/brand_heat')
api.add_namespace(searching_indexes_ns, path='/searching_indexes')
api.add_namespace(user_ns, path='/user')
api.add_namespace(session_ns, path='/session')
api.add_namespace(detection_ns, path='/detection')
