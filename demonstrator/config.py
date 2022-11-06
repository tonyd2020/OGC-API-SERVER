import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('postgresql://sensorthings:ChangeMe@localhost:5432/sensorthings')
    SQLALCHEMY_TRACK_MODIFICATIONS = False