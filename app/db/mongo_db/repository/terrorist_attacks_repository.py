from typing import List
from app.db.mongo_db.database import terrorist_attacks_collection



def insert_attacks_to_mongo_db(attacks: List[dict]):
    terrorist_attacks_collection.insert_many(attacks)
    print(f"Successfully inserted {len(attacks)} records to mongo.")


# terrorist_attacks_collection.delete_many({})