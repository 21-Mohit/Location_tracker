from pymongo import MongoClient, errors  
from dotenv import load_dotenv  
import os  

load_dotenv()  
db_url = os.getenv('DB')  

client = MongoClient(db_url)  

tracker = client.get_database('Tracker')  
coordinate_db = tracker.get_collection("coordinates") # Collection for coordinates  
user_db = tracker.get_collection("users")  # New collection for users  

def save_coordinates(deviceId, longitude, latitude):  
    # Save the coordinates for the given deviceId  
    coordinate_db.insert_one({  
        '_id': deviceId,  
        'longitude': longitude,  
        'latitude': latitude  
    })  
    
def update_coordinates(deviceId, longitude, latitude):  
    # Update the coordinates or save them if they do not exist  
    if coordinate_db.find_one({'_id': deviceId}):  
        coordinate_db.update_one({'_id': deviceId}, {'$set': {'longitude': longitude, 'latitude': latitude}})  
    else:  
        save_coordinates(deviceId, longitude, latitude)  

def create_user(username, userId):  
    # Check if the user already exists  
    if user_db.find_one({'username': username}):  
        return False  # User already exists  

    # Insert the new user into the users collection  
    user_db.insert_one({  
        'username': username,  
        'password': userId  
    })  
    return True  # User created successfully  

def find_user_by_name(username):  
    # Find and return a user by their username  
    user = user_db.find_one({'username': username})  
    if user:  
        return user  # Return the user document  
    return None  # No user found

