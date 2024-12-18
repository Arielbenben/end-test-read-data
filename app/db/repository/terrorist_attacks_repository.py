from typing import List
from app.db.database import terrorist_attacks_collection



def insert_attacks(attacks: List[dict]):
    terrorist_attacks_collection.insert_many(attacks)

def get():
    return terrorist_attacks_collection.find_one()

# print(get())
# terrorist_attacks_collection.delete_many({})