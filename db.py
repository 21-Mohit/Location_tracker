from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv('DB')

client = MongoClient(db_url)


tracker = client.get_database('Tracker')
coordinate_db = tracker.get_collection("coordinates") #get_collection

def save_coordinates(deviceId, longitude,latitude):
    #if coordinate_db.find_one({'_id':deviceId,'longitude':longitude,'latitude':latitude})
    coordinate_db.insert_one({'_id':deviceId,'longitude':longitude,'latitude':latitude})
    
def update_coordinates(deviceId, longitude,latitude):
    if coordinate_db.find_one({'_id': deviceId}):
        coordinate_db.update_one({'_id':deviceId},{'$set':{'longitude':longitude,'latitude':latitude}})
    else:
        save_coordinates(deviceId, longitude,latitude)
        