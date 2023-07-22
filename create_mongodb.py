from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
import os


def get_database():
   uri = os.environ.get('MONGO_URL')
   # Create a new client and connect to the server
   client = MongoClient(uri, tlsCAFile=certifi.where())
   return client['biasbusters_db']

if __name__ == "__main__":   
   biasbusters_db = get_database()