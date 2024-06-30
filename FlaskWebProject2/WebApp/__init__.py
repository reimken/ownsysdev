from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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

from WebApp import routes, models

