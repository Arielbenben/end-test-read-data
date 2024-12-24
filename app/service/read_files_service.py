from app.db.elastic_search_db.repository.terrorist_attack_repository import insert_attacks_to_elastic_db
from app.db.mongo_db.repository.terrorist_attacks_repository import insert_attacks_to_mongo_db
from app.utils.models_utils import convert_attack_to_models, convert_models_to_mongo_dict, \
    update_df_with_additional_columns, calculate_deadly_grade
import pandas as pd
import os
from dotenv import load_dotenv


load_dotenv(verbose=True)


def read_csv_files():

    terrorist_attack_path = os.getenv('TERRORIST_ATTACK_PATH')
    terrorist_attack_second_path = os.getenv('TERRORIST_ATTACK_SECOND_PATH')

    df_first_data = pd.read_csv(terrorist_attack_path, encoding='iso-8859-1')
    df_second_data = pd.read_csv(terrorist_attack_second_path, encoding='iso-8859-1')

    return df_first_data, df_second_data


def prepare_and_merge_data(df_first_data, df_second_data):

    df_second_data = update_df_with_additional_columns(df_second_data)

    merge_df = pd.concat([df_first_data, df_second_data], axis=0, ignore_index=True)
    merge_df = merge_df.drop_duplicates()

    merge_df[['nperps', 'nkill', 'nwound']] = merge_df[['nperps', 'nkill', 'nwound']].apply(pd.to_numeric, errors='coerce')
    merge_df['nperps'] = merge_df['nperps'].apply(lambda x: x if x >= 0 else None)

    merge_df[['iday', 'imonth', 'iyear']] = merge_df[['iday', 'imonth', 'iyear']].apply(pd.to_numeric, errors='coerce')

    merge_df = calculate_deadly_grade(merge_df)

    return merge_df


def insert_data_in_batches(df, batch_size=1000):
    list_of_dicts_data = df.to_dict(orient='records')
    batch = []

    for attack in list_of_dicts_data:
        convert_to_models = convert_attack_to_models(attack)
        convert_models_to_dict = convert_models_to_mongo_dict(convert_to_models)

        batch.append(convert_models_to_dict)

        if len(batch) == batch_size:
            insert_attacks_to_elastic_db(batch)
            insert_attacks_to_mongo_db(batch)
            batch = []

    if batch:
        insert_attacks_to_elastic_db(batch)
        insert_attacks_to_mongo_db(batch)



def insert_data_to_db():
    df_first_data, df_second_data = read_csv_files()
    merge_data = prepare_and_merge_data(df_first_data, df_second_data)
    insert_data_in_batches(merge_data, 1000)
