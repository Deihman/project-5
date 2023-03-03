from pymongo import MongoClient

def store(item_dictionary:dict, database):
    '''
    stores a dictionary in the specified database
    '''
    database.insert_one(item_dictionary)

    return

def fetch(database):
    '''
    returns an object from the specified database in dictionary form
    '''
    items = database.find_one()

    return items
