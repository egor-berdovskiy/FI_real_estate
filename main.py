import geojson
import json
import pandas as pd
import warnings

from functions import convert_to_latlon, convert_to_string_and_remove_brackets, get_address, generate_table

from data.config import General


warnings.filterwarnings("ignore")


def main():
    print(f'[3] Reading {General.input_file_name} file')
    with open(General.input_file_name, 'r', encoding='utf-8') as file:
        data = geojson.load(file)['features']

    df = pd.DataFrame(data)
    result = pd.DataFrame()
    
    df = pd.json_normalize(df['properties'])

    result = df[['kayttotarkoitus', 'kerrosluku']]
    result['sijainti_piste'] = pd.json_normalize(df['sijainti_piste'].apply(json.loads))['coordinates']

    result['UMT'] = result['sijainti_piste'].apply(convert_to_string_and_remove_brackets)
    result['Coordinates (Lat Lon)'] = result['UMT'].apply(convert_to_latlon)
    result = result.drop(['UMT', 'sijainti_piste'], axis=1)

    column_names = {
        'kayttotarkoitus': 'building_type',
        'kerrosluku': 'Floor'
    }

    result.rename(columns=column_names, inplace=True)

    result.to_excel(f'{General.output_file_path}{General.output_file_name}.{General.file_format}', index=False)
    print(f'[!] File "{General.output_file_path}{General.output_file_name}.{General.file_format}" saved.')
    print(f'[2] Decoding coordinates!')

    # Decoding
    result['address'] = result['Coordinates (Lat Lon)'].apply(get_address)

    result.to_excel(f'{General.output_file_path}{General.output_file_name} + addresses.{General.file_format}', index=False)
    print(f'[!] File "{General.output_file_path}{General.output_file_name} + addresses.{General.file_format}" saved.')

    # Generate google table
    print(f'[1] Generate Google table!')
    generate_table(result)


if __name__ == '__main__':
    main()
