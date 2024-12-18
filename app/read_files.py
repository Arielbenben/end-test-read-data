from app.db.repository.terrorist_attacks_repository import insert_attacks
from app.utils.models_utils import convert_attack_to_models, convert_models_to_mongo_dict, \
    update_df_with_additional_columns
import pandas as pd


terrorist_attack_path = "C:\\Users\\relbh\\Downloads\\globalterrorismdb_0718dist.csv"
terrorist_attack_second_path = "C:\\Users\\relbh\\Downloads\\RAND_Database_of_Worldwide_Terrorism_Incidents.csv"


def insert_date_to_mongo_db():
    df_first_data = pd.read_csv(terrorist_attack_path, encoding='iso-8859-1')
    df_second_data = pd.read_csv(terrorist_attack_second_path, encoding='iso-8859-1')

    df_second_data = update_df_with_additional_columns(df_second_data)

    merge_df = pd.concat([df_first_data, df_second_data], axis=0, ignore_index=True)

    merge_df[['nperps', 'nkill', 'nwound']] = merge_df[['nperps', 'nkill', 'nwound']].fillna(0)
    merge_df[['nperps', 'nkill', 'nwound']] = merge_df[['nperps', 'nkill', 'nwound']].astype(int)
    merge_df[['iday', 'imonth', 'iyear']] = merge_df[['iday', 'imonth', 'iyear']].astype(int)

    list_of_dicts_data = merge_df.to_dict(orient='records')

    batch = 1000
    attacks = []

    for attack in list_of_dicts_data:
        convert_to_models = convert_attack_to_models(attack)
        convert_models_to_dict = convert_models_to_mongo_dict(convert_to_models)

        attacks.append(convert_models_to_dict)

        if len(attacks) == batch:
            insert_attacks(attacks)
            attacks = []

    if attacks:
        insert_attacks(attacks)
