#!/usr/bin/env python

from datetime import date
import time
import sys
import os
from functools import wraps

from flask import Flask, render_template, jsonify, request, Response, make_response
from pymongo import MongoClient
from requests.utils import dict_from_cookiejar

import couchsurfing

MONGO_URI = os.getenv("MONGOHQ_URL")
db = MongoClient(MONGO_URI)['app19566517']

app = Flask(__name__)

def get_home():
    return 'http://' + request.host + '/'

def check_login(uid):
    return db.data.find_one({"uid": uid})

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid.
    """
    try:
    	api = couchsurfing.Api(username, password)
    except couchsurfing.AuthException:
    	return False
    return api

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
        if not auth:
            return authenticate()
        api = check_auth(auth.username, auth.password)
        if not api:
            return authenticate()
        return f(api, *args, **kwargs)
    return decorated

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/get')
@requires_auth
def get(api):
    """ Query user's data from API """
    start = int(request.args.get("from")[:-3])
    end = int(request.args.get("to")[:-3])

    requests = couchsurfing.Requests(api, start, end)

    all_requests = requests.accepted + requests.new
    for req in all_requests:
        req["start"] *= 1000
        req["end"] *= 1000

    data = {
    	"success": 1,
    	"result": all_requests
    }

    return jsonify(**data)

@app.route('/save')
@requires_auth
def save(api):
    """ Save calendar data to db """
    requests = couchsurfing.Requests(api)

    all_requests = requests.accepted
    for req in all_requests:
        req["start"] *= 1000
        req["end"] *= 1000

    print(request.args)

    data = {"uid": api.uid, "requests": all_requests}
    # check if we want to store a cookie as well
    if request.args.get("cookie") == "true":
            data["cookie"] = dict_from_cookiejar(api.cookies)

    db.data.update({"uid": api.uid}, data, upsert=True)

    # return link to user's calendar
    return get_home() + api.uid

@app.route('/check')
@requires_auth
def check_cookie(api):
    """ Check if a cookie exists for a given uid """
    find = db.data.find_one({"uid": api.uid})
    response = make_response()

    if find and "cookie" in find:
        response.status_code = 200
    else:
        response.status_code = 204

    response.data = response.status
    return response

@app.route('/get_user')
def get_user():
    """ Get user's calendar """
    username = request.args.get("uid")

    find = db.data.find_one({"uid": username})
    data = {
        "success": 1,
        "result": find['requests']
    }

    return jsonify(**data)

@app.route('/<path:uid>')
def index_user(uid):
    """ User's calendar view """
    return render_template("index_user.html", uid=uid)

if __name__ == '__main__':
    app.run(debug=True)
