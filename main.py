import sys
from datetime import datetime

from flask import Flask, abort, request
from flask_restful import Api, Resource, reqparse, inputs
from flask_sqlalchemy import SQLAlchemy

# Configuring application and setting up Flask-SQLalchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Creating DB
db.create_all()
api = Api(app)  # Creating API for HTTP
parser = reqparse.RequestParser()  # Creating argument parser for proper GET requests

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


class Calendar(db.Model):  # This is the DB table Calendar
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)


class apiResource(Resource):  # This is at .../event 
    def get(self):
        if len(request.args) > 0:  # IF there are url parameters, only put the range of dates between start and end time
            start = request.args.get("start_time")
            end = request.args.get("end_time")
            dates = Calendar.query.filter(Calendar.date.between(start, end)).all()
        else:  # Else, query all events
            dates = Calendar.query.all()
        list_of_dates = list()
        for date in dates:
            list_of_dates.append({"id": date.id, "event": date.event, "date": str(date.date)})
        return list_of_dates

    def post(self):  # You can only add events on this url
        args = parser.parse_args()  # First, make sure everything is formatted properly
        args["message"] = "The event has been added!"  # If it is, then this success message will pop up
        db_date = Calendar(event=args["event"], date=args["date"])  # Add it to database
        db.session.add(db_date)
        db.session.commit()
        return {"message": args["message"], "event": args["event"], "date": str(args["date"].date())}


class apiTodayResource(Resource):  # This is for event/today
    def get(self):
        dates = Calendar.query.all()  # Query all events in database
        list_of_dates = list()
        for date in dates:
            if str(date.date) == str(datetime.today().date()):  # If there is an event today, display it!
                list_of_dates.append({"id": date.id, "event": date.event, "date": str(date.date)})
        return list_of_dates


class EventByID(Resource):  # This is for event/# where # is the ID of the event (GET /event shows all ids)
    def get(self, event_id):  # You can retrieve events by ID
        dates = Calendar.query.filter_by(id=event_id).first()
        if dates is None:
            abort(404, "The event doesn't exist!")
        return {"id": dates.id, "event": dates.event, "date": str(dates.date)}

    def delete(self, event_id):  # You can delete events
        dates = Calendar.query.filter_by(id=event_id).first()
        if dates is None:
            abort(404, "The event doesn't exist!")
        db.session.delete(dates)  # Delete from DB
        db.session.commit()
        return {"message": "The event has been deleted!"}


# These add to the API so that we can do proper HTTP commands
api.add_resource(apiResource, '/event')
api.add_resource(apiTodayResource, '/event/today')
api.add_resource(EventByID, '/event/<int:event_id>')  # <int:event_id> = any integer thrown into event_id

# This is here to run the URL on your own computer
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
