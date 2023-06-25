from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi

def get_database():
   uri = "mongodb+srv://biasbuster:vicksANDbl123@biasbuster.fp2dd9w.mongodb.net/?retryWrites=true&w=majority"
   # Create a new client and connect to the server
   client = MongoClient(uri, tlsCAFile=certifi.where())
   return client['biasbusters_db']

if __name__ == "__main__":   
   biasbusters_db = get_database()




