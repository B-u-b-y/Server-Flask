from pymongo import MongoClient


def get_db_connection():
    # Replace with your MongoDB connection string
    mongo_uri = "mongodb://localhost:27017/Football"
    client = MongoClient(mongo_uri)

    # Choose your database
    db = client['Football']
    return db
