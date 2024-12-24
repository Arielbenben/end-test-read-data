from app.db.elastic_search_db.repository.terrorist_attack_repository import create_indexes_to_mongo
from app.service.read_files_service import insert_data_to_db


if __name__ == '__main__':
    insert_data_to_db()
    create_indexes_to_mongo()





