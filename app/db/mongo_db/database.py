from pymongo import MongoClient


client = MongoClient('mongodb://172.19.191.59:27018')
terrorist_attack_db = client['terrorist_attack']

terrorist_attacks_collection = terrorist_attack_db['terrorist_attacks']

