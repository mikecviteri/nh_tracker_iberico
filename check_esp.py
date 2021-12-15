import pandas as pd
import os
import re
import numpy as np
import sys
from date import random_date, day_checker
from csv_converter import convert_to_csv, check_csv_shape

# day = day_checker()
regex = re.compile(r'^[\d]+.wav$')


def match_recorded_files():
    while True:
        folder = input('Ingresa la dirección completa de la carpeta con los audiofiles')
        if os.path.isdir(folder):
            break
        else:
            print('No es una dirección válida')
            continue

    audiofiles = []
    f = open(f"no_match_{day}.txt", "w+")
    count = 1

    for root, dirs, files in os.walk(folder, topdown=False):
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


csv_1 = pd.read_csv('/Users/miguelcampero/Desktop/NH_ESP/TRACKER_DL2_ES_07dec21_Sala 1.csv', low_memory=False)
csv_2 = pd.read_csv('/Users/miguelcampero/Desktop/NH_ESP/TRACKER_DL2_ES_07dec21.csv', low_memory=False)

values = []

for i in range(csv_1.shape[0]):
    if pd.isna(csv_1['Rec Status'].loc[i]) and pd.isna(csv_2['Rec Status'].loc[i]):
        values.append(csv_1['Rec Status'].loc[i])
    elif csv_1['Rec Status'].loc[i] != csv_2['Rec Status'][i]:
        values.append(csv_1['Rec Status'].loc[i]) if pd.isna(csv_2['Rec Status'][i]) else values.append(
            csv_2['Rec Status'][i])
    else:
        values.append(csv_1['Rec Status'].loc[i])


for i in range(len(values)):
    try:
        if np.isnan([values[i], csv_1['Rec Status'].loc[i], csv_2['Rec Status'].loc[i]]).all():
            pass
    except TypeError:
        if values[i] == csv_1['Rec Status'].loc[i] or values[i] == csv_2['Rec Status'].loc[i]:
            pass
        else:
            print(f'Algo falló en la fila {i}')
