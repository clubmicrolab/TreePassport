from pymongo.mongo_client import MongoClient 

from dotenv import dotenv_values

config = dotenv_values(".env")


client = MongoClient(f'mongodb+srv://{config["USER_DB"]}:{config["USER_DB_PW"]}@cluster0.pvwuovh.mongodb.net/?retryWrites=true&w=majority')

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)