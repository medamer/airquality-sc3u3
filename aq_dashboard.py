"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import openaq

APP = Flask(__name__)


@APP.route('/')
def root():
    utc_datetime = request.form['datetime']
    value= request.form['value']
    return utc_datetime


APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)
SQLALCHEMY_TRACK_MODIFICATIONS = False



class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'DATABASE CREATED'


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    api=openaq.OpenAQ()
    status, resp = api.measurements()
    record=DB.resp['results']
    DB.session.commit()
    return 'Data refreshed!'