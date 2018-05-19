# coding=utf-8
"""The entrance of the whole project."""

from app import create_app


app = create_app('development')

if __name__ == '__main__':
    app.run(host=app.config.get('HOST'), port=app.config.get('PORT'))
