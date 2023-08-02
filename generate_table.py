from functions import generate_table
import pandas as pd

print('Введите название файла для генерации Google Sheet (xlsx, xls, csv), пример: real_estate_fi.xlsx')
file_name = input('название: ')

result = pd.read_excel(file_name)

generate_table(result)
