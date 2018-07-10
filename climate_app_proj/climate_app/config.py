import os
basedir = os.path.abspath(os.path.dirname(__file__))
previous_dir = basedir[:-len('climate//app')]


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(previous_dir, 'hawaii.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False