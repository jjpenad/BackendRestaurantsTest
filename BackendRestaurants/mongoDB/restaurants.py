
from BackendRestaurants.mongoDB import DB, COLLECTION_RESTAURANTS

def get_all_public_restaurants():
    '''
    Searches for PUBLIC restaurants
    '''
    cursor=DB[COLLECTION_RESTAURANTS].find({'visibility':"public"})
    return list(cursor)

def get_all_restaurants():
    '''
    Searches for PUBLIC or PRIVATE restaurants
    '''
    cursor=DB[COLLECTION_RESTAURANTS].find({})
    return list(cursor)

def get_public_restaurant_by_name(name:str):
    '''
    Searches for PUBLIC restaurant with the given name
    '''
    cursor=DB[COLLECTION_RESTAURANTS].find({'name':name,'visibility':"public"})
    try:
        restaurant=cursor[0]
    except:
        return None
    return restaurant


def get_restaurant_by_name(name:str):
    '''
    Searches for PUBLIC or PRIVATE restaurant with the given name
    '''
    cursor=DB[COLLECTION_RESTAURANTS].find({'name':name})
    try:
        restaurant=cursor[0]
    except:
        return None
    return restaurant


def get_restaurants_created_by(createdById:str):
    '''
    Get restaurants created by an user
    '''
    cursor=DB[COLLECTION_RESTAURANTS].find({"createdBy":createdById})
    return list(cursor)


def create_restaurant(name:str, description:str, createdBy:str, address:str, city:str, score:int, visibility:str="private"):
    '''
    Create a restaurant.

    It must have a creator
    '''
    restaurant_doc={"name":name, "description": description, "createdBy":createdBy, "city":city, "score":score, "visibility":visibility}
    result = DB[COLLECTION_RESTAURANTS].insert_one(restaurant_doc)
    restaurant_doc["_id"]=result.inserted_id
    return restaurant_doc
    

def update_restaurant(name: str, description:str, createdBy:str, visibility:str,address:str, city:str, score:int):
    '''
    Update a restaurant. Searched by name and creatorId

    Only the creator of the restaurant can modify it.
    '''
    
    result = DB[COLLECTION_RESTAURANTS].update_one({'name': name, 'createdBy': createdBy}, 
            {'$set': {'description': description, 'visibility':visibility, "address":address, "city":city, "score":score}})
    if result.modified_count==0:
        return False
    return True
    
def delete_restaurant(name: str, creatorId:str):
    '''
    Delete a restaurant. Searched by name and creatorId

    Only the creator of the restaurant can delete it.
    '''
    result = DB[COLLECTION_RESTAURANTS].delete_one({'name': name, 'createdBy': creatorId})
    if result.deleted_count==0:
        return False
    return True