# coding=utf-8
import requests
import os
from flask import Flask
from sqlalchemy.exc import IntegrityError
from app.model import init_db


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

    logo_folder_path = os.path.join('../../', app.config['IMAGE_FOLDER'], 'logos')
    if not os.path.exists(logo_folder_path):
        os.makedirs(logo_folder_path)

    return logo_folder_path


def download_image(url, img_path):
    """Save an image by url and return the absolute path to the image."""
    img_data = requests.get(url).content
    with open(img_path, 'wb') as file:
        file.write(img_data)
    img_path = os.path.abspath(img_path)
    return img_path


def main():
    logo_folder_path = initialize()
    from app.model import brands
    with open('brands.txt') as f:
        f.readline()
        for l in f.readlines():
            items = l.split('|')
            img_path = os.path.join(logo_folder_path, items[0]+'.jpg')
            items[2] = download_image(items[2], img_path)
            try:
                brands.add_brand(*items)
            except IntegrityError:
                print('%s already exists!' % items[0])


if __name__ == '__main__':
    main()
