from pymongo import MongoClient
import os

client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017'))
db = client['enejistats']

users = db['users']
players = db['players']
clubs = db['clubs']
matches = db['matches']
stats = db['stats']
