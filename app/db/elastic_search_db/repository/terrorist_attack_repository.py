from elasticsearch.helpers import bulk
from app.db.elastic_search_db.database import terrorist_attacks_history_index, elastic_client
from app.db.mongo_db.database import terrorist_attacks_collection
from pymongo import ASCENDING



def insert_attacks_to_elastic_db(terrorist_attacks: list):
    actions = [
        {
            "_op_type": "index",
            "_index": terrorist_attacks_history_index,
            "_source": attack
        }
        for attack in terrorist_attacks
    ]

    try:
        success, failed = bulk(elastic_client, actions)
        print(f"Successfully inserted {success} records to elastic.")
        if failed > 0:
            return {'Error': f'Failed to insert {failed} records'}
        return {'Success': f'Inserted {success} records'}
    except Exception as e:
        return {'Error': f'Exception occurred: {str(e)}'}


def create_indexes_to_mongo():
    terrorist_attacks_collection.create_index([('casualties.deadly_grade', 1)])
    terrorist_attacks_collection.create_index([('location.full_date', 1)])
    terrorist_attacks_collection.create_index([('attack.attack_type', 1)])
    terrorist_attacks_collection.create_index([('attack.target', 1)])
    terrorist_attacks_collection.create_index([('location.region', 1)])
    terrorist_attacks_collection.create_index([('location.country', 1)])

    print('indexes created successfully')


def delete_all_docs_all_indexes():
    elastic_client.delete_by_query(index="_all", body={"query": {"match_all": {}}})

