from pymongo.mongo_client import MongoClient 

from dotenv import dotenv_values


def send_to_cloud(data):
    config = dotenv_values(".env")
    client = MongoClient(f'mongodb+srv://{config["USER_DB"]}:{config["USER_DB_PW"]}@cluster0.pvwuovh.mongodb.net/?retryWrites=true&w=majority')  
    db = client["TreeInfo"]
    collection = db["trees"] 
    collection.insert_one(data)



