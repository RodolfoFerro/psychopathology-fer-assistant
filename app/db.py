from datetime import datetime
from random import random
from time import sleep

from pymongo import MongoClient


MONGO_URI = ''


def db_connect_collection(MONGO_URI, database_name, collection_name):
    client = MongoClient(MONGO_URI)
    database = client[database_name]
    collection = database[collection_name]
    return collection


def db_fetch_all(collection, query={}):
    cursor = collection.find(query)
    return cursor


def db_fetch_last(collection, patient, n=20):
    cursor = collection.find({'patient': patient}).sort([('_id', -1)]).limit(20)
    return cursor


def db_insert_record(collection, record):
    return collection.insert_one(record)


def db_clean(collection, conditions={}):
    collection.delete_many(conditions)
    return


if __name__ == "__main__":
	fer = db_connect_collection(MONGO_URI, 'psychofer', 'fer')
	db_clean(fer)
	