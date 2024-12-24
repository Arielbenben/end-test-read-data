from elasticsearch import Elasticsearch


elastic_client = Elasticsearch(
    hosts=["http://localhost:9200"],
    basic_auth=("elastic", "123456"),
    verify_certs=False
)

try:
    info = elastic_client.info()
except Exception as e:
    print(f"Failed to connect to Elasticsearch: {e}")


terrorist_attacks_history_index = 'terrorist_attack_history'