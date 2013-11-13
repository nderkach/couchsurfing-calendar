#!/usr/bin/env python

from datetime import date
import time
import sys
from functools import wraps

from flask import Flask, render_template, abort, jsonify, request, Response

import couchsurfing

#import imp
#couchsurfing = imp.load_source('couchsurfing', '../couchsurfing-python/couchsurfing/__init__.py')


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
    {'WWW-Authenticate': 'Basic realm="Enter your couchsurfing.org login and password"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(auth.username, auth.password, *args, **kwargs)
    return decorated

@app.route('/',  methods=['GET', 'POST'])
def index():
	return render_template("index.html")

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
@requires_auth
def get(username, password):
	print(request.method)
	# print(request.json)

	# start = request.args.get("from")
	# end = request.args.get("to")

	# get all couch requests
	api = couchsurfing.Api(username, password)
	requests = couchsurfing.Requests(api)

	data = {
		"success": 1,
		"result": requests.accepted + requests.new
	}

	# data["result"] = [event for event in data["result"] if (start < float(event["start"]) < float(event["end"]) < end)] 

	# print("DATA")
	# print(data)

	return jsonify(**data)

if __name__ == '__main__':
    app.run(debug=True)
