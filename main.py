import sys
from datetime import datetime

from flask import Flask
from flask_restful import Api, Resource, reqparse, inputs
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)
api = Api(app)
parser = reqparse.RequestParser()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

parser.add_argument(
    "message",
    type=str,
    help="",
    required=False
)
parser.add_argument(
    "event",
    type=str,
    help="The event name is required!",
    required=True
)
parser.add_argument(
    "date",
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)


class Calendar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)


class apiResource(Resource):  # This is at .../event 
    def get(self):
        dates = Calendar.query.all()
        list_of_dates = list()
        info = dict()
        for date in dates:
            info["id"] = date.id
            info["event"] = date.event
            info["date"] = str(date.date)
            list_of_dates.append(info)
            info = dict()
        return list_of_dates

    def post(self):
        args = parser.parse_args()
        args["date"] = str(args["date"].date())
        args["message"] = "The event has been added!"
        db_date = Calendar(event=args["event"], date=datetime.strptime(args["date"], "%Y-%m-%d"))
        db.session.add(db_date)
        db.session.commit()
        return args


class apiTodayResource(Resource):
    def get(self):
        dates = Calendar.query.all()
        list_of_dates = list()
        info = dict()
        for date in dates:
            if str(date.date) == str(datetime.today().date()):
                info["id"] = date.id
                info["event"] = date.event
                info["date"] = str(date.date)
                list_of_dates.append(info)
            info = dict()
        return list_of_dates


db.create_all()

api.add_resource(apiResource, '/event')
api.add_resource(apiTodayResource, '/event/today')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
