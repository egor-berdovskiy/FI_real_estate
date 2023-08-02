from configparser import ConfigParser


parser = ConfigParser()
parser.read(r'config.ini')


def set_value(section, key, value):
    parser.set(section, key, value)
    with open('config.ini', 'w') as configfile:
        parser.write(configfile)


class General:
    section = 'General'
    input_file_name = parser.get(section, 'input_file_name')
    output_file_name = parser.get(section, 'output_file_name')
    file_format = parser.get(section, 'file_format')
    output_file_path = parser.get(section, 'output_file_path')


class GeocoderSettings:
    section = 'GeocoderSettings'
    address_format = parser.get(section, 'address_format')
    language = parser.get(section, 'language')


class Coordinates:
    section = 'Coordinates'
    zone_number = parser.getint(section, 'zone_number')
    zone_letter = parser.get(section, 'zone_letter')


class Google:
    section = 'Google'
    oauth2_file_name = parser.get(section, 'oauth2_file_name')
    oauth2_file_path = parser.get(section, 'oauth2_file_path')
    table_id = parser.get(section, 'table_id')
    table = parser.get(section, 'table')
    sheet = parser.get(section, 'sheet')
