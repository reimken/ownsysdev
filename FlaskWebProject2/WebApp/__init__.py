from flask import Flask, jsonify, request, make_response
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import jwt
import datetime
from functools import wraps

basedir = os.path.abspath(os.path.dirname(__file__))   #megadja a projekt akutális elérési útját

app = Flask(__name__)
#required for web forms
app.config["SECRET_KEY"] = "rendszerfejlesztes"


#required for SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL') or \
 'sqlite:///' + os.path.join(basedir, 'sysdevdb.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class UserRoles:
    USER = 'user'
    MANAGER = 'manager'


from WebApp import routes, models

