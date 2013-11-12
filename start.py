#!/usr/bin/env python

from flask import Flask, render_template, abort, jsonify
from calendar import Calendar
from datetime import date
import time
import json

import sys
# sys.path.append("../couchsurfing-python")
import couchsurfing

from functools import wraps
from flask import request, Response

app = Flask(__name__)

CALENDAR_FILE = "/static/bootstrap-calendar/events.json.php"

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    try:
    	api = couchsurfing.Api(username, password)
    except couchsurfing.AuthException:
    	return False
    return True

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

# @app.route('/', defaults={'year': None})
# @app.route('/<int:year>/')
@app.route('/',  methods=['GET', 'POST'])
@requires_auth
def index():

	return render_template("index.html")

	# cal = Calendar()
	# today = date.fromtimestamp(time.time())
	# accepted = set([date(today.year, today.month, i) for i in range(1,12)])
	# new = set([date(today.year, today.month, i) for i in range(15,17)])



	# print("ACCEPTED")
	# print(accepted)
	# print("NEW")
	# print(new)
	# try:
	# 	if not year:
	# 		year = date.today().year
	# 	cal_list = [cal.monthdatescalendar(year, i+1) for i in range(12)]
	# 	# cal_list = [cal.monthdatescalendar(year, date.today().month)]
	# 	print(cal_list)
	# except Exception as e:
	# 	abort(404)
	# else:
	# 	return render_template('cal.html', year=year, cal=cal_list, accepted=accepted, new=new)
	# abort(404)

@app.route(CALENDAR_FILE, methods=['POST', 'GET'])
def feed():
	print(request.method)
	print(request.json)
	with open(CALENDAR_FILE[1:], 'r') as f:
		data = json.load(f)

	start = request.args.get("from")
	end = request.args.get("to")

	# data["result"] = [event for event in data["result"] if (start < int(event["start"]) < int(event["end"]) < end)] 

	return jsonify(**data)

@app.route('/get', methods=['POST', 'GET'])
def get():
	print(request.method)
	# print(request.json)

	start = request.args.get("from")
	end = request.args.get("to")

	# get all couch requests
	requests = couchsurfing.Requests()

	data = {
		"success": 1,
		"result": requests.accepted + requests.new
	}

	# data["result"] = [event for event in data["result"] if (start < float(event["start"]) < float(event["end"]) < end)] 

	print("DATA")
	print(data)

	return jsonify(**data)

if __name__ == '__main__':
    app.run(debug=True)
