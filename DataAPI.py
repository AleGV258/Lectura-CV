import os
from dotenv import load_dotenv
from pymongo import MongoClient

def connectionDB():
    load_dotenv()
    MONGODB_URI = os.environ['MONGO_URI']
    connection = MongoClient(MONGODB_URI)
    return connection

def InsertRecord(collection, record):
    con = connectionDB()
    db = con.DataCV
    colection = db[collection]
    colection.insert_one(record)
    con.close()

def DeleteRecord(collection, recordID):
    pass

def UpdateRecord(collection, record):
    pass

# from DataAPI import FUNCTION