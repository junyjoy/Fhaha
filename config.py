"""
DB, SECRET_KEY 관련 config
Authors: jlee (junlee9834@gmail.com)
"""

import os

BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Reca1111!@mysql.cttweiazxzhe.ap-northeast-2.rds.amazonaws.com:3306/fhaa?charset=utf8'
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:0000@127.0.0.1:3306/fhaa?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "dev"