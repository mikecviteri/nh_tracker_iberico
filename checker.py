import pandas as pd
import os
import re
import sys
from date import random_date, day_checker

regex = re.compile(r'^[\d]+.wav$')
data = pd.read_csv('./prueba.csv')
day = day_checker()


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
            elif file.startswith('.'):
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


def make_csv(audios, valid_day):
    match = pd.DataFrame(
        {'Match': ['Recorded' if data['SIDE ID'].loc[i] in audios else data['Rec Status'].loc[i] for i in
                   range(data.shape[0])], 'Check': ['x' if data['SIDE ID'].loc[i] in audios else '' for i in
                                                    range(data.shape[0])]})

    match['Time'] = [random_date(valid_day) if (match['Match'].loc[i] == 'Recorded' and
                                                type(data['Rec Date'].loc[i]) == float) else data['Rec Date'].loc[i] for
                     i in range(data.shape[0])]

    match.to_csv(f'resultado_{day}.csv', index=False)
    return ''


if __name__ == "__main__":
    make_csv(match_recorded_files(), day)
    sys.exit()
