import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-change-later')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///insureworth.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False