from elasticsearch.helpers import bulk
from app.db.elastic_search_db.database import terrorist_attacks_history_index, elastic_client



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


def delete_all_docs_all_indexes():
    elastic_client.delete_by_query(index="_all", body={"query": {"match_all": {}}})

# delete_all_docs_all_indexes()
