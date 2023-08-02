import utm
import pandas as pd
import gspread
from geopy.geocoders import Nominatim
from google.oauth2.service_account import Credentials

from gspread_dataframe import set_with_dataframe

from data.config import Google


def convert_to_string_and_remove_brackets(coordinates):
    return str(coordinates).strip('[]').replace(',', '')


def convert_to_latlon(coordinates):
    coordinates = list(map(float, coordinates.split(' ')))
    easting, northing = coordinates
    zone_number = 35
    zone_letter = 'V'
    lat, lon = utm.to_latlon(easting, northing, zone_number, zone_letter)
    return f'{lat} {lon}'


def get_address(coordinates, address_format = 'fin', language = 'en'):
    lat, lon = coordinates.split(' ')
    address_format = address_format.lower()

    location = None

    try:
        geolocator = Nominatim(user_agent="geoapiExercises", timeout=10)
        location = geolocator.reverse((lat, lon), language=language)
    except Exception as ex:
        return 'error'

    if location:
        address = location.raw['address']
        full_address = location.raw['display_name']
        if address_format == 'fin':
            try:
                if address.get('house_number') and address.get('postcode'):
                    print('[i] converted address...')
                    return f"{address['road']} {address['house_number']}, {address['postcode']}, {address['city']}"
                elif address.get('postcode'):
                    print('[i] converted address...')
                    return f"{address['road']}, {address['postcode']}, {address['city']}"
                elif address.get('house_number'):
                    print('[i] converted address...')
                    return f"{address['road']} {address['house_number']}, {address['city']}"
                elif not (address.get('postcode') and address.get('house_number')):
                    print('[i] converted address...')
                    return f"{address['road']}, {address['city']}"
                else:
                    print(f'[i] converted address...')
                    return full_address
            except Exception as ex:
                # print(f'ERROR: {ex}\naddress: {address}\n')
                return full_address
        
        elif address_format == 'none':
            return address
    else:
        return 'error'


def generate_table(df: pd.DataFrame):
    try:
        credentials = Credentials.from_service_account_file(f'{Google.oauth2_file_path}{Google.oauth2_file_name}', scopes=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

        gc = gspread.authorize(credentials)
        spreadsheet = gc.open_by_key(Google.table_id)

        worksheets = spreadsheet.worksheets()

        for worksheet in worksheets[1:]:
            spreadsheet.del_worksheet_by_id(worksheet.id)

        worksheet = spreadsheet.add_worksheet(title=Google.sheet, rows=df.shape[0], cols=df.shape[1])
        set_with_dataframe(worksheet, df)
        
        print(f'Table generated!\nURL: {spreadsheet.url}')
    except Exception as ex:
        print('An error occurred:', ex)
