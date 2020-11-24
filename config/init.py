import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

basedir = os.path.abspath(os.path.dirname(__file__))

sqlite_url = "sqlite:////" + os.path.join(basedir, "customer.db")

app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = sqlite_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

marsh = Marshmallow(app)
