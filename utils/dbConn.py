from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['spotiflop']
users_collection = db.get_collection("utilisateur")