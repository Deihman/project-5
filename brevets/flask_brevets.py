"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
from pymongo import MongoClient
import pymongo_interface
import os

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
client = MongoClient("mongodb://" + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.brevet

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects three URL-encoded arguments: 
        control km: a checkpoint's distance
        brevet distance: the total distance of the brevet
        start time: the start time of the brevet
    """
    app.logger.debug("Got a JSON request: /_calc_times")
    km = request.args.get('km', 999, type=float)
    brevet_dist_km = request.args.get('brevet_dist_km', 200, type=float)
    start_time = request.args.get('start_time', '2021-01-01T00:00', type=str)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    # FIXME!
    # Right now, only the current time is passed as the start time
    # and control distance is fixed to 200
    # You should get these from the webpage!

    start_time_arrow = arrow.get(start_time, 'YYYY-MM-DDTHH:mm')

    open_time = acp_times.open_time(km, brevet_dist_km, start_time_arrow).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, brevet_dist_km, start_time_arrow).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


@app.route("/_submit")
def _submit():
    """
    adds the current inputs to a mongo database "brevet"
    Expects three URL-encoded arguments:
        control km: the checkpoint's distance
        location: the checkpoint's location name
        open time: the open time of the checkpoint
        close time: the close time of the checkpoint
    returns a jsonified true value if it reaches the end
    """
    app.logger.debug("Got a JSON request: /_submit")
    km = request.args.get("km", -1, type=float)
    location = request.args.get("location", "", type=str)
    start_time = request.args.get("start_time", "", type=str)
    brevet_dist_km = request.args.get("brevet_dist_km", -1, type=float)

    if km == -1 or start_time == "" or brevet_dist_km < 200:
        return flask.jsonify(result={"stored": "no"})

    item_doc = {
        "km": km,
        "location": location,
        "start_time": start_time,
        "brevet_distance": brevet_dist_km
    }

    pymongo_interface.store(item_doc, db)

    return flask.jsonify(result={"stored": "yes"})

@app.route("/_display")
def _display():
    app.logger.debug("Got a JSON request: /_display")

    items = pymongo_interface.fetch(db)

    return flask.jsonify(result=items)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
