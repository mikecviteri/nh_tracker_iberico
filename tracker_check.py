import re
import os
from pathlib import Path
from date import random_date
from csv_converter import convert_to_csv
import numpy as np
import pandas as pd

regex = re.compile(r'^[\d]+.wav$')


def get_files(path):
    audio_files = dict()
    alts = []
    other_files = []
    folders = []

    f = open(f"Results/report.txt", "w+")

    for root, dirs, files in os.walk(path, topdown=False):
        day = Path(root).parents[0].name[2:]
        try:
            if int(day) and day not in folders:
                folders.append(day)
                count = 1
                with open(f'Results/report.txt', 'a') as f:
                    f.write(f'{"*" * 20} {day} {"*" * 20}\n')
                f.close()
        except ValueError:
            pass

        for file in files:
            if regex.match(file) and file not in audio_files.keys():
                audio_id = int(file.replace('.wav', ''))
                audio_files.update({audio_id: random_date(int(day))})
            elif file.startswith('.') or not (file.endswith('.wav')):
                other_files.append(file)
            else:
                alts.append(file)
                with open(f'Results/report.txt', 'a') as f:
                    f.write(f'{count}. {file}\n')
                count += 1
                f.close()

    with open(f'Results/report.txt', 'a') as f:
        f.write(
            f'\nTotal de archivos de audio: {len(audio_files) + len(alts)}\nAudios alternos/mal nombrados/duplicados: '
            f'{len(alts)}\nTotal de audios a revisar: {len(audio_files)}\n\nOtros archivos no encontrados:\n\n')
        for other in other_files:
            f.write(f'* {other}\n')
        f.write('\nAudios duplicados en tomas alternas:\n')
        for i in set([x for x in alts if alts.count(x) > 1]):
            f.write(f'{i}\n')
    f.close()

    return audio_files


folder_path = '/Users/miguelcampero/Downloads/Audios/'
# virgin_xlsm = '/Users/miguelcampero/Downloads/Audios/1206/TRACKER_DL2_ES_07dec21.xlsm'
# data = convert_to_csv(virgin_xlsm)

data = pd.read_csv('/Users/miguelcampero/Desktop/NH_ESP/csvs/TRACKER_DL2_ES_07dec21.csv')

audios = get_files(folder_path)

count = 1
list_of_dict = []
for row in range(data.shape[0]):
    if data['SIDE ID'].loc[row] in audios.keys():
        list_of_dict.append({'No.': count, 'MY_SIDE_ID': data['SIDE ID'].loc[row], 'MY_REC_STATUS': 'Recorded',
                             'MY_REC_DATE': audios[data['SIDE ID'].loc[row]]})
        count += 1
    else:
        list_of_dict.append({'No.': np.nan, 'MY_SIDE_ID': np.nan, 'MY_REC_STATUS': np.nan,
                             'MY_REC_DATE': np.nan})


print(pd.DataFrame(list_of_dict))
