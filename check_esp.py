import sys
import pandas as pd
import os
import re
import numpy as np
from date import random_date, day_checker
from csv_converter import convert_to_csv

day = day_checker()
regex = re.compile(r'^[\d]+.wav$')


def get_path():
    while True:
        folder = input('Ingresa la dirección completa de la carpeta con los audiofiles')
        if os.path.isdir(folder):
            break
        else:
            print('No es una dirección válida')
            continue
    return folder


def find_excel_filenames(suffix=".xlsm"):
    global valid_path
    filenames = os.listdir(valid_path)
    return [os.path.join(valid_path, filename) for filename in filenames if filename.endswith(suffix)]


valid_path = get_path()


def match_recorded_files():
    global valid_path

    audiofiles = []
    f = open(f"no_match_{day}.txt", "w+")
    count = 1

    for root, dirs, files in os.walk(valid_path, topdown=False):
        for file in files:
            if regex.match(file):
                audiofiles.append(int(file.replace('.wav', '')))
            elif file.startswith('.') or not (file.endswith('.wav')):
                pass
            else:
                with open(f'no_match_{day}.txt', 'a') as f:
                    f.write(f"{count}. {file if not file[0] == '.' else ''}\n")
                    count += 1
            f.close()

    if os.stat(f"{os.getcwd()}/no_match_{day}.txt").st_size == 0:
        os.remove(f"no_match_{day}.txt")
    else:
        print(f'Algunos audios no se encontraron en el Excel. Revisa el archivo \"no_match_{day}.txt\"')

    return audiofiles


# MERGE

def generate_csv(first_file, second_file):
    files = match_recorded_files()

    csv_1 = pd.read_csv(first_file, low_memory=False)
    csv_2 = pd.read_csv(second_file, low_memory=False)

    rec = []
    date_rec = []
    date_filter = []

    for i in range(csv_1.shape[0]):
        if pd.isna(csv_1['Rec Status'].loc[i]) and pd.isna(csv_2['Rec Status'].loc[i]):
            rec.append(csv_1['Rec Status'].loc[i])
            date_rec.append(csv_1['Rec Date'].loc[i])
            date_filter.append('')
        elif csv_1['Rec Status'].loc[i] != csv_2['Rec Status'][i]:
            rec.append(csv_1['Rec Status'].loc[i]) if pd.isna(csv_2['Rec Status'][i]) else rec.append(
                csv_2['Rec Status'][i])
            date_rec.append(csv_1['Rec Date'].loc[i]) if pd.isna(csv_2['Rec Date'][i]) else date_rec.append(
                csv_2['Rec Date'][i])
            if csv_1['SIDE ID'].loc[i] in files:
                date_filter.append(random_date(day))
            else:
                error = f'Al parecer SIDE ID: {csv_1["SIDE ID"].loc[i]} no está grabado'
                print(error)
                with open(f'no_match_{day}.txt', 'a') as f:
                    f.write(error)
                date_filter.append('ERROR! NOT FOUND')
        else:
            rec.append(csv_1['Rec Status'].loc[i])
            date_rec.append(csv_1['Rec Date'].loc[i])
            date_filter.append('')

    # DOUBLE CHECK
    errors = 0
    for i in range(len(rec)):
        try:
            if np.isnan([rec[i], csv_1['Rec Status'].loc[i], csv_2['Rec Status'].loc[i]]).all():
                pass
        except TypeError:
            if rec[i] == csv_1['Rec Status'].loc[i] or rec[i] == csv_2['Rec Status'].loc[i]:
                pass
            else:
                errors += 1
                print(f'Algo falló en la fila {i}')

    if errors != 0:
        print('Revisa el código, hay errores al juntar los dos Exceles')
    else:
        match = pd.DataFrame(
            {'Rec Status': rec, 'Rec Date': date_rec, 'Filter': date_filter})

        match.to_csv(f'resultado_{day}.csv', index=False)


if __name__ == '__main__':
    file_1, file_2 = map(lambda x: convert_to_csv(x), find_excel_filenames())
    generate_csv(file_1, file_2)
