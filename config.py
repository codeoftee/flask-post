# config.py
import os
import pathlib


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(
        pathlib.Path().absolute(), 'myDb.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOADS_FOLDER = os.path.join(pathlib.Path().absolute(), 'static/uploads')