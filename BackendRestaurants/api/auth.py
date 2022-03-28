
from flask import Blueprint, jsonify, current_app, request, make_response
import jwt
from BackendRestaurants.mongoDB.users import get_user_by_email, register_user
from BackendRestaurants.utils import checkPassword, isValidEmail, handleResponse
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta

# Constants
JWT_EXPIRATION_TIME=20 # minutes

auth_route_v1 = Blueprint('auth_route', "auth_route", url_prefix="/auth/")

@auth_route_v1.route('/signup', methods=["POST"])
def signup():
    #Requests must have header Content-Type=application/json
    data=request.get_json()

    if data:
        email, password = data.get("email"), data.get("password")

        if not isValidEmail(email):
            return handleResponse({"error":"Invalid Email"}, 400)
        checkPass=checkPassword(password)
        if not checkPass[0]:
            return handleResponse({"error":checkPass[1]}, 400)

        # check for existing user
        user=get_user_by_email(email)

        if not user:
            user = register_user(email, generate_password_hash(password))
            return handleResponse({"message":"Succesfully Registered"}, 201)
        else:
            return handleResponse({"message":"User already exists. Please log in"}, 200)
    else:
        return handleResponse({"message":'Sign up information not found'}, 404)

@auth_route_v1.route('/login', methods=["POST"])
def login():
    #Requests must have header Content-Type=application/json
    auth=request.get_json()
    if auth:
        email, password = auth.get("email"), auth.get("password")

        if not email or not password:
            return handleResponse({"error":'Missing information'}, 404)

        if not isValidEmail(email):
            return handleResponse({"error":"Invalid Email"}, 400)
        checkPass=checkPassword(password)
        if not checkPass[0]:
            return handleResponse({"error":checkPass[1]}, 400)

        user = get_user_by_email(email)
    
        if not user:
            # returns 401 if user does not exist
            return handleResponse(jsonify({"error":"User does not exist"}), 401)
    
        if check_password_hash(user.get("password"), password):
            # generates the JWT Token
            token = jwt.encode({
                'email': user.get("email"),
                'exp' : datetime.utcnow() + timedelta(minutes = JWT_EXPIRATION_TIME)
            }, current_app.config['SECRET_KEY'], algorithm="HS256")
    
            return handleResponse({'token' : token},200)
        # returns 403 if password is wrong
        return handleResponse({"error":"Incorrect password"}, 403)
    else:
        return handleResponse({"message":'Sign up information not found'}, 400)


def token_required(f):
    '''
    Decorator for verifying the JWT.
    
    Used for endpoints whose token is mandatory
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return handleResponse({'message' : 'Unauthorized request'},401) 
  
        current_user=None
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = get_user_by_email(data['email'])
        except Exception as e:
            print(e)
            return handleResponse({"message":"Token is invalid"},401)
        
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated


def token_verication(f):
    '''
    Decorator for verifying the JWT.
    
    Used for endpoints that might or not require token
    '''
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        # Send to endpoint with null user
        if not token:
            return  f(None, *args, **kwargs)
  
        current_user=None
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = get_user_by_email(data['email'])
        except Exception as e:
            return handleResponse({"message":"Token is invalid"},401)
        
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated

# @auth_route_v1.route('/', methods=["GET"], defaults={'userId': "0"})
# @auth_route_v1.route('/<userId>')


