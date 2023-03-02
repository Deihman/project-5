import os
from pymongo import MongoClient

client = MongoClient("mongodb://" + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.brevet
mybrevets = db.mybrevets

def store(item_dictionary:dict):
    mybrevets.insert_one(item_dictionary)
    return 1

def fetch():
    items = list(mybrevets.find())
    return items
