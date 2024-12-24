from typing import List
from app.db.mongo_db.database import terrorist_attacks_collection



def insert_attacks(attacks: List[dict]):
    terrorist_attacks_collection.insert_many(attacks)


# terrorist_attacks_collection.delete_many({})