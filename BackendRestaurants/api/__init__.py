from BackendRestaurants.api.auth import auth_route_v1
from BackendRestaurants.api.restaurants import restaurants_route_v1
from flask import Blueprint

api_v1 = Blueprint('api', "api", url_prefix="/api/v1/")

api_v1.register_blueprint(auth_route_v1)
api_v1.register_blueprint(restaurants_route_v1)