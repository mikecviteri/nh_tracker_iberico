import pandas as pd
import os
import re
import numpy as np
from date import random_date, day_checker

day = day_checker()
regex = re.compile(r'^[\d]+.wav$')


# Check if a given path exists in local

def get_path():
    while True:
        folder = input('Ingresa la dirección completa de la carpeta con los audiofiles')
        if os.path.isdir(folder):
            break
        else:
            print('No es una dirección válida')
            continue
    return folder


# Getting a list of all the .wav recorded audiofiles

def list_audiofiles(path):
    audiofiles = []
    f = open(f"Results/no_match_{day}.txt", "w+")
    count = 1

    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            if regex.match(file):
                audiofiles.append(int(file.replace('.wav', '')))
            elif file.startswith('.') or not (file.endswith('.wav')):
                pass
            else:
                with open(f'Results/no_match_{day}.txt', 'a') as f:
                    f.write(f"{count}. {file if not file[0] == '.' else ''}\n")
                    count += 1
            f.close()

    if os.stat(f"{os.getcwd()}/Results/no_match_{day}.txt").st_size == 0:
        os.remove(f"Results/no_match_{day}.txt")
    else:
        print(
            f'Algunos audios no se encontraron en el Excel. Revisa el archivo \"no_match_{day}.txt\" '
            f'en la carpeta Results')

    return audiofiles


# Merging the 2 csv files

def merge_csvs(path, first_file, second_file):
    files = list_audiofiles(path)

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
                with open(f'Results/no_match_{day}.txt', 'a') as f:
                    f.write(error)
                date_filter.append('ERROR! NOT FOUND')
        else:
            rec.append(csv_1['Rec Status'].loc[i])
            date_rec.append(csv_1['Rec Date'].loc[i])
            date_filter.append('')

    # Double checking the merge was done correctly
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

        match.to_csv(f'Results/resultado_{day}.csv', index=False)
