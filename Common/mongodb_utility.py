# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas as pd


def connect_db(dbhost="localhost", dbport=27017, db_name=None):
    client = MongoClient(dbhost, dbport)
    db = client[db_name]
    return db

def insert_db(db=None, collection_name=None, data=None):
    if data is None:
        print("No data to be inserted!")
        return None
    try:
        result = db[collection_name].insert_many(data)
        return result
    except Exception as e:
        print(e.details)
        return None

def export2df(database = None, conditions={}, collection=""):
    """
    Export data from mongo db in dataframe with conditions
    :param conditions: 
    :param database: 
    :param collection: 
    :return: DataFrame
    """
    results = database[collection].find(conditions)
    frame = pd.DataFrame(list(results))
    return frame
