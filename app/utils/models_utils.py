from datetime import datetime
from pandas import DataFrame
import pandas as pd
from app.db.mongo_models.attack import Attack
from app.db.mongo_models.casualties import Casualties
from app.db.mongo_models.date import Date
from app.db.mongo_models.location import Location
from app.db.mongo_models.terrorist_group import TerroristGroup


def create_datetime(day: int, month: int, year: int):
    if day == '0' or month == '0' or year == '0':
        return None
    if not day or not month or not year:
        return None
    return datetime(year, month, day)


def validate_perps(perps: int):
    return perps if perps >= 0 else 0


def convert_data_to_terrorist_group_model(attack_data: dict):
    return TerroristGroup(
        name=attack_data['gname'],
        perps=validate_perps(int(attack_data['nperps']))
    )


def convert_data_to_attack_model(attack_data: dict):
    return Attack(
        attack_type=attack_data['attacktype1_txt'],
        attack_type_2=attack_data['attacktype2_txt'],
        attack_type_3=attack_data['attacktype3_txt'],
        weapon=attack_data['weapdetail'],
        target=attack_data['target1'],
        target_type=attack_data['targtype1_txt'],
        target_sub_type=attack_data['targsubtype1_txt'],
        summary=attack_data['summary']
    )


def convert_data_to_casualties_model(attack_data: dict):
    return Casualties(
        killed=attack_data['nkill'],
        wound=attack_data['nwound']
    )


def convert_data_to_date_model(attack_data: dict):
    return Date(
        day=attack_data['iday'],
        month=attack_data['imonth'],
        year=attack_data['iyear'],
        full_date=create_datetime(attack_data['iday'], attack_data['imonth'], attack_data['iyear'])
    )


def convert_data_to_location_model(attack_data: dict):
    return Location(
        country=attack_data['country_txt'],
        region=attack_data['region_txt'],
        city=attack_data['city'],
        latitude=attack_data['latitude'],
        longitude=attack_data['longitude'],
        province=attack_data['provstate'],
        exact_location=attack_data['location']
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
    df['iday'] = df['Date'].dt.day
    df['imonth'] = df['Date'].dt.month
    df['iyear'] = df['Date'].dt.year
    return df


def rename_columns(df):
    df.rename(columns={'Fatalities': 'nkill', 'Injuries': 'nwound', 'City': 'city', 'Country': 'country_txt',
                       'Perpetrator': 'gname', 'Weapon': 'weapdetail', 'Description': 'summary'}, inplace=True)
    return df


def add_default_columns(df):
    df['nperps'] = 0
    df['attacktype1_txt'] = None
    df['attacktype2_txt'] = None
    df['attacktype3_txt'] = None
    df['target1'] = None
    df['targtype1_txt'] = None
    df['targsubtype1_txt'] = None
    df['region_txt'] = None
    df['latitude'] = None
    df['longitude'] = None
    df['provstate'] = None
    df['location'] = None
    return df


def update_df_with_additional_columns(df: DataFrame):
    df = process_date_columns(df)
    df = rename_columns(df)
    df = add_default_columns(df)

    return df

