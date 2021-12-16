import sys
import pandas as pd
import re
import os
from pathlib import Path

file_no = re.compile(r'.*?([0-9]+)\..*')


def join_csv_tracker(path1, path2):
    f1, f2 = map(lambda x: file_no.match(os.path.basename(x)).group(1), [path1, path2])

    file_1 = pd.read_csv(path1)
    file_2 = pd.read_csv(path2)

    rec_status = []
    rec_date = []
    date_filter = []

    if file_1.shape == file_2.shape:
        for i in range(file_1.shape[0]):
            if pd.isna(file_1['Rec Status'].loc[i]) or pd.isna(file_2['Rec Status'].loc[i]):
                rec_status.append(file_2['Rec Status'].loc[i]) if pd.isna(
                    file_1['Rec Status'][i]) else rec_status.append(
                    file_1['Rec Status'][i])
                rec_date.append(file_2['Rec Date'].loc[i]) if pd.isna(file_1['Rec Date'][i]) else rec_status.append(
                    file_1['Rec Date'][i])
                date_filter.append(file_2['Filter'].loc[i]) if pd.isna(file_1['Filter'][i]) else rec_status.append(
                    file_1['Filter'][i])
            elif pd.isna(file_1['Filter'].loc[i]) or pd.isna(file_2['Filter'].loc[i]):
                rec_status.append(file_2['Rec Status'].loc[i])
                rec_date.append(file_2['Rec Date'].loc[i])
                date_filter.append(file_2['Filter'].loc[i]) if pd.isna(
                    file_1['Filter'][i]) else date_filter.append(
                    file_1['Filter'][i])
            else:
                rec_status.append(file_2['Rec Status'].loc[i])
                rec_date.append(file_2['Rec Date'].loc[i])
                date_filter.append(file_2['Filter'].loc[i])

    else:
        print('Hay un error con los tamaños de los csvs. Revisa los archivos')

    merged = pd.DataFrame(
        {'Rec Status': rec_status, 'Rec Date': rec_date, 'Filter': date_filter})

    merged.to_csv(f'Results/resultado_{f1}_{f2}.csv', index=False)


def valid_csv():
    while True:
        csv = input('Ingresa la dirección del archivo csv')
        my_file = Path(csv)
        if my_file.is_file():
            return my_file
            break
        else:
            print('No es una dirección válida')
            continue


if __name__ == '__main__':
    print('Primer archivo csv')
    csv1 = valid_csv()
    print('Segundo archivo archivo csv')
    csv2 = valid_csv()
    join_csv_tracker(csv1, csv2)
