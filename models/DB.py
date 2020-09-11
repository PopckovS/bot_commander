from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import config

two_up = os.path.abspath(os.path.join(__file__, "../.."))
sys.path.append(two_up)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.CONNECT_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
