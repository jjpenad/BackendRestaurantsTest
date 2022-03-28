from ast import Pass
import json
from turtle import update
from flask import Blueprint, jsonify, request
from BackendRestaurants.api.auth import token_required, token_verication
from BackendRestaurants.utils import handleResponse
from BackendRestaurants.mongoDB.restaurants import create_restaurant, delete_restaurant, get_all_public_restaurants, get_all_restaurants, get_public_restaurant_by_name, get_restaurant_by_name, update_restaurant
from BackendRestaurants.mongoDB.users import get_user_by_email

restaurants_route_v1 = Blueprint('restaurants_route', "restaurants_route", url_prefix="/")

@restaurants_route_v1.route('/restaurants', methods=["GET"])
@token_verication
def getAllRestaurants(current_user):
    restaurantName = request.args.get('name')
    if current_user: # Is for a logged in user
        if restaurantName!=None and restaurantName!="": # User + restaurant name = search for specific restaurant either public or if this user is the creator
            restaurant = get_restaurant_by_name(restaurantName)
            if restaurant:
                return restaurant
            else:
                return handleResponse({"message":"No restaurant found with the given name"}, 404)
        else: # User + no restaurant name = search for all public and private restaurants related to the user
            return jsonify(get_all_restaurants())
    else: # there is no user logged in = only search for public restaurants
        if restaurantName!=None and restaurantName!="": # No user + restaurant name = search for specific public restaurant
            restaurant = get_public_restaurant_by_name(restaurantName)
            if restaurant:
                return restaurant
            else:
                return handleResponse({"message":"No restaurant found with the given name"}, 404)
        else: # No user + no restaurant name = search for all public restaurants
            return jsonify(get_all_public_restaurants())


@restaurants_route_v1.route('/restaurants', methods=["POST"])
@token_required
def createRestaurant(current_user):
    #Requests must have header Content-Type=application/json
    data=request.get_json()
    if data:
        restaurantName, description, visibility = data.get("name"), data.get("description"), data.get("visibility")
        address, city, score = data.get("address"), data.get("city"), data.get("score")

        if restaurantName==None or restaurantName=="":
            return handleResponse({"error":"Restaurant name is required"}, 400)

        if visibility!= "public" and visibility!="private":
            return handleResponse({"error":"Restaurant visibility must be either public or private"}, 400)

        if score!=None:
            try:
                score=int(score)
                if score<0:
                    return handleResponse({"error":"The Score of the restaurant must be a positive integer"}, 400)
            except:
                return handleResponse({"error":"The Score of the restaurant must be a positive integer"}, 400)
        else:
            score=0

        restaurant=get_restaurant_by_name(restaurantName)
        if restaurant:
            return handleResponse({"error":"Already exists a restaurant with the given name"}, 400)

        # check for existing user
        user=get_user_by_email(current_user["email"])
        result=create_restaurant(restaurantName, description, user["_id"], address, city, score,visibility)

        if not result:
            return handleResponse({"error":"Could not create the restaurant"}, 200)

        return result # handleResponse({"message":"Restaurant succesfully created"}, 201)

    else:
        return handleResponse({"error":'No creation information found in the request'}, 400)  



@restaurants_route_v1.route('/restaurants', methods=["PUT"])
@token_required
def updateRestaurant(current_user):
    #Requests must have header Content-Type=application/json
    data=request.get_json()
    if data:
        restaurantName, description, visibility = data.get("name"), data.get("description"), data.get("visibility")
        address, city, score = data.get("address"), data.get("city"), data.get("score")

        if restaurantName==None or restaurantName=="":
            return handleResponse({"error":"Restaurant name is required"}, 400)

        if visibility!= "public" and visibility!="private":
            return handleResponse({"error":"Restaurant visibility must be either public or private"}, 400)

        if score!=None:
            try:
                score=int(score)
                if score<0:
                    return handleResponse({"error":"The Score of the restaurant must be a positive integer"}, 400)
            except:
                return handleResponse({"error":"The Score of the restaurant must be a positive integer"}, 400)
        else:
            score=0

        # check for existing user
        user=get_user_by_email(current_user["email"])
        result=update_restaurant(restaurantName, description, user["_id"], visibility, address, city, score)
        if not result:
            return handleResponse({"error":"Could not update the restaurant"}, 200)
        else:
            restaurant=get_restaurant_by_name(restaurantName)
            return restaurant

    else:
        return handleResponse({"error":'No update information found in the request'}, 400)
    

@restaurants_route_v1.route('/restaurants', methods=["DELETE"])
@token_required
def deleteRestaurant(current_user):
    #Requests must have header Content-Type=application/json
    data=request.get_json()
    if data:
        restaurantName = data.get("name")

        if restaurantName==None or restaurantName=="":
            return handleResponse({"error":"Restaurant name is required"}, 400)

        # check for existing user
        user=get_user_by_email(current_user["email"])
        result=delete_restaurant(restaurantName, user["_id"])
        
        if not result:
            return handleResponse({"error":"Could not delete the restaurant"}, 200)

        return handleResponse({"message":"Restaurant succesfully deleted"}, 200)

    else:
        return handleResponse({"error":'No delete information found in the request'}, 400)
