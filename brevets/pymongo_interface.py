import os
from pymongo import MongoClient

client = MongoClient("mongodb://" + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.brevet

def store(item_dictionary:dict):
    db.insert_one(item_dictionary)
    return 1

def fetch():
    items = list(db.find_one())
    return items
