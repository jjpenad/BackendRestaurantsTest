from BackendRestaurants.mongoDB import DB, COLLECTION_USERS
from BackendRestaurants.utils import isValidEmail



def register_user(email:str, password:str):
    '''
    This function directly creates the user with the given password to Mongo.
    Before using it, check if email and password are valid.

    Also, because you should pass the encrypted password here, only the email pattern is checked.
    '''
    if not isValidEmail(email) or password==None or password=="":
        return False
    
    user_doc={"email":email, "password": password}
    result = DB[COLLECTION_USERS].insert_one(user_doc)
    return {"_id":result.inserted_id, "email":user_doc["email"]}


def get_user_by_email(email=str):
    ''' Checks if the user already exists in the database by email.
        If True return the User else None 
    '''
    cursor=DB[COLLECTION_USERS].find({"email":email})
    user=None
    try:
        user=cursor[0]
    except:
        return None
    return user
