from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure

DB_NAME="BackendRestaurants"
COLLECTION_USERS="Users"
COLLECTION_RESTAURANTS="Restaurants"

def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = PyMongo(current_app).db
       
    return db

DB = LocalProxy(get_db)
