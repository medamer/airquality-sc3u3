"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq

APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)
api=openaq.OpenAQ()
#SQLALCHEMY_TRACK_MODIFICATIONS = False


@APP.route('/')
def root():
    return str(Record.query.filter(Record.value >= 10).all())

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to db
    for result in get_results():
        record = Record(datetime=result[0], value=result[1])
        DB.session.add(record)
    DB.session.commit()
    return 'Data refreshed!'

def get_results():
    _, body = api.measurements(city='Los Angeles', parameter='pm25')
    results=[]
    for result in body['results']:
        results.append((result['date']['utc'], result['value']))
    return results

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '< Time {} --- Value {} >'.format(self.datetime, self.value)
