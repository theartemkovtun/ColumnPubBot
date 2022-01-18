from pymongo import MongoClient
import configuration

def get_database():
    return MongoClient(configuration.MONGO_CONNECTION_STRING)[configuration.MONGO_DB_NAME]
