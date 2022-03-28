import imp
from flask import Flask, request, jsonify

import os
from flask import Flask, render_template
from flask.json import JSONEncoder
from bson import json_util, ObjectId
from datetime import datetime, timedelta

from BackendRestaurants.api import api_v1

class MongoJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)

def create_app():
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    #STATIC_FOLDER = os.path.join(APP_DIR, 'build/static')
    #TEMPLATE_FOLDER = os.path.join(APP_DIR, 'build')

    app = Flask(__name__)
    app.json_encoder = MongoJsonEncoder
    
    # API
    app.register_blueprint(api_v1)

    @app.route('/')
    def serve():
       return "<p>Welcome to Backend Restaurants Service!</p>"

    return app

# app = Flask(__name__)

# # Create some test data for our catalog in the form of a list of dictionaries.
# books = [
#     {'id': 0,
#      'title': 'A Fire Upon the Deep',
#      'author': 'Vernor Vinge',
#      'first_sentence': 'The coldsleep itself was dreamless.',
#      'year_published': '1992'},
#     {'id': 1,
#      'title': 'The Ones Who Walk Away From Omelas',
#      'author': 'Ursula K. Le Guin',
#      'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
#      'published': '1973'},
#     {'id': 2,
#      'title': 'Dhalgren',
#      'author': 'Samuel R. Delany',
#      'first_sentence': 'to wound the autumnal city.',
#      'published': '1975'}
# ]

# @app.route("/", methods=["GET"])
# def init():
#     return "<p>Hello, World!</p>"
    

# # A route to return all of the available entries in our catalog.
# @app.route('/api/v1/resources/books/all', methods=['GET'])
# def api_all():
#     return jsonify(books)
