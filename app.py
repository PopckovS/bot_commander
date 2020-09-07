from flask import Flask, url_for, request, render_template, \
    redirect, abort, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
# app = Flask('wb')
app.config['SQLALCHEMY_DATABASE_URI'] = config.CONNECT_DB
sslify = SSLify(app)
db = SQLAlchemy(app)
