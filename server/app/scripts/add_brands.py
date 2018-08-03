# coding=utf-8
import requests
import os
from flask import Flask
from sqlalchemy.exc import IntegrityError
from app.model import init_db

logo_folder_path = '../../../images/logos'


def initialize():
    """Initialize a simple app to establish DB connection"""
    app = Flask(__name__)
    # Load private config at instance/config.py
    config_path = '../../instance/config.py'
    if os.path.exists(config_path):
        app.config.from_pyfile(config_path)

    # Initialize database
    init_db(
        app.config['DB_USERNAME'],
        app.config['DB_PASSWORD'],
        app.config['DB_NAME']
    )

    if not os.path.exists(logo_folder_path):
        os.makedirs(logo_folder_path)


def download_image(url, name):
    """Save an image by url and return the absolute path to the image."""
    img_data = requests.get(url).content
    img_path = os.path.join(logo_folder_path, name+'.jpg')
    with open(img_path, 'wb') as file:
        file.write(img_data)
    img_path = os.path.abspath(img_path)
    return img_path


if __name__ == '__main__':
    initialize()
    from app.model import brands
    with open('brands.txt') as f:
        f.readline()
        for l in f.readlines():
            items = l.split('|')
            items[2] = download_image(items[2], items[0])
            try:
                brands.add_brand(*items)
            except IntegrityError:
                print('%s already exists!' % items[0])
