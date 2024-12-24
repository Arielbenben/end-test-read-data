from datetime import datetime
from pandas import DataFrame
import pandas as pd
from app.db.mongo_db.mongo_models.attack import Attack
from app.db.mongo_db.mongo_models.casualties import Casualties
from app.db.mongo_db.mongo_models.date import Date
from app.db.mongo_db.mongo_models.location import Location
from app.db.mongo_db.mongo_models.terrorist_group import TerroristGroup


def check_nan_or_unknown(value):
    if isinstance(value, str) and value in ['Unknown', 'Other']:
        return None
    return None if pd.isna(value) else value


def calculate_deadly_grade(merge_df):
    merge_df['deadly_grade'] = merge_df['nwound'] + (merge_df['nkill'] * 2)
    return merge_df


def create_datetime(day: int, month: int, year: int):
    if day == '0' or month == '0' or year == '0':
        return None
    if not day or not month or not year:
        return None
    return datetime(year, month, day)


def validate_perps(perps):
    return None if perps is None or perps < 0 else perps


def correct_years(date):
    if pd.isna(date):
        return date
    if date.year >= 2068:
        return date.replace(year=date.year - 100)
    return date


def convert_data_to_terrorist_group_model(attack_data: dict):
    return TerroristGroup(
        name=check_nan_or_unknown(attack_data['gname']),
        perps=check_nan_or_unknown(attack_data['nperps'])
    )


def convert_data_to_attack_model(attack_data: dict):
    return Attack(
        attack_type=check_nan_or_unknown(attack_data['attacktype1_txt']),
        weapon=check_nan_or_unknown(attack_data['weapdetail']),
        target=check_nan_or_unknown(attack_data['target1']),
        target_type=check_nan_or_unknown(attack_data['targtype1_txt']),
        target_sub_type=check_nan_or_unknown(attack_data['targsubtype1_txt']),
        summary=check_nan_or_unknown(attack_data['summary'])
    )


def convert_data_to_casualties_model(attack_data: dict):
    return Casualties(
        killed=check_nan_or_unknown(attack_data['nkill']),
        wound=check_nan_or_unknown(attack_data['nwound']),
        deadly_grade=check_nan_or_unknown(attack_data['deadly_grade'])
    )


def convert_data_to_date_model(attack_data: dict):
    return Date(
        day=check_nan_or_unknown(attack_data['iday']),
        month=check_nan_or_unknown(attack_data['imonth']),
        year=check_nan_or_unknown(attack_data['iyear']),
        full_date=create_datetime(attack_data['iday'], attack_data['imonth'], attack_data['iyear'])
    )


def convert_data_to_location_model(attack_data: dict):
    return Location(
        country=check_nan_or_unknown(attack_data['country_txt']),
        region=check_nan_or_unknown(attack_data['region_txt']),
        city=check_nan_or_unknown(attack_data['city']),
        latitude=check_nan_or_unknown(attack_data['latitude']),
        longitude=check_nan_or_unknown(attack_data['longitude']),
        province=check_nan_or_unknown(attack_data['provstate']),
        exact_location=check_nan_or_unknown(attack_data['location'])
    )


def convert_attack_to_models(attack_data: dict):
    terrorist_group = convert_data_to_terrorist_group_model(attack_data)
    attack = convert_data_to_attack_model(attack_data)
    casualties = convert_data_to_casualties_model(attack_data)
    date = convert_data_to_date_model(attack_data)
    location = convert_data_to_location_model(attack_data)

    return {'terrorist_group': terrorist_group, 'attack': attack, 'casualties': casualties,
            'date': date, 'location': location}


def convert_models_to_mongo_dict(models: dict) -> dict:
    return {
        'terrorist_group': models['terrorist_group'].to_dict(),
        'attack': models['attack'].to_dict(),
        'casualties': models['casualties'].to_dict(),
        'date': models['date'].to_dict(),
        'location': models['location'].to_dict(),
    }


def process_date_columns(df):
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Date'] = df['Date'].apply(correct_years)

    df['iday'] = df['Date'].dt.day
    df['imonth'] = df['Date'].dt.month
    df['iyear'] = df['Date'].dt.year
    return df


def rename_columns(df):
    df.rename(columns={'Fatalities': 'nkill', 'Injuries': 'nwound', 'City': 'city', 'Country': 'country_txt',
                       'Perpetrator': 'gname', 'Weapon': 'weapdetail', 'Description': 'summary'}, inplace=True)
    return df


# def add_default_columns(df):
#     df['nperps'] = 0
#     df['attacktype1_txt'] = None
#     df['attacktype2_txt'] = None
#     df['attacktype3_txt'] = None
#     df['target1'] = None
#     df['targtype1_txt'] = None
#     df['targsubtype1_txt'] = None
#     df['region_txt'] = None
#     df['latitude'] = None
#     df['longitude'] = None
#     df['provstate'] = None
#     df['location'] = None
#     return df


def update_df_with_additional_columns(df: DataFrame):
    df = process_date_columns(df)
    df = rename_columns(df)
    # df = add_default_columns(df)

    return df

