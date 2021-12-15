import openpyxl
import csv
import pandas as pd
import os

count = 1


# Listing all the Excel files within the directory

def find_excel_filenames(valid_path, suffix=".xlsm"):
    filenames = os.listdir(valid_path)
    return [os.path.join(valid_path, filename) for filename in filenames if filename.endswith(suffix)]


# Converting Excel file to csv

def convert_to_csv(path):
    excel = openpyxl.load_workbook(path)
    filename = os.path.splitext(os.path.basename(path))[0]
    sheet = excel.active

    col = csv.writer(open(f"csvs/{filename}.csv",
                          'w',
                          newline="", encoding='utf-8-sig'))

    for r in sheet.rows:
        col.writerow([cell.value for cell in r])

    return f'{os.path.join(os.getcwd(), "csvs/" + filename)}.csv'


# Comparing both csv files have the same size/data

def check_csv_shape(path_1, path_2):
    correct = 0

    csv_1 = pd.read_csv(path_1, low_memory=False)
    csv_2 = pd.read_csv(path_2, low_memory=False)

    if csv_1.shape[0] == csv_2.shape[0]:
        print('Ambos archivos tienen el mismo número de filas')
        for val in range(csv_1.shape[0]):
            if csv_1['SIDE ID'][val] != csv_2['SIDE ID'][val]:
                print(
                    f'La fila {val} tiene un problema. {csv_1["SIDE ID"][val]} y {csv_2["SIDE ID"][val]} no coinciden')
            else:
                correct += 1
        if correct == csv_1.shape[0]:
            print('OK. Todos los valores coinciden')
            return True
    else:
        print("El número de filas no es igual. Por favor revisa tus archivos")
        return False
