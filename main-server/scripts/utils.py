# coding=utf-8
import os
import requests
from flask import Flask
import sys
sys.path.append(os.path.abspath('./'))
from app.model import init_db


def initialize():
    """Initialize a simple app to establish DB connection"""
    app = Flask(__name__)
    # Load private config at instance/config.py
    config_path = 'instance/config.py'
    if os.path.exists(config_path):
        app.config.from_pyfile(os.path.abspath(config_path))

    # Initialize database
    init_db(
        app.config['DB_USERNAME'],
        app.config['DB_PASSWORD'],
        app.config['DB_NAME']
    )

    return app


def download_image(url, img_path):
    """Save an image by url and return the absolute path to the image."""
    img_data = requests.get(url).content
    with open(img_path, 'wb') as file:
        file.write(img_data)
    img_path = os.path.abspath(img_path)
    return img_path
