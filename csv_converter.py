import openpyxl
import csv
import pandas as pd
import os

count = 1


def convert_to_csv():
    valid = ['.xlsx', '.xlsm', '.xltx', '.xltm']

    while True:
        path = input('Ingresa la dirección del archivo Excel a convertir')
        if any(path.endswith(extension) for extension in valid):
            excel = openpyxl.load_workbook(path)
            break
        else:
            print('No es una dirección/archivo de Excel válido')
            continue

    filename = os.path.splitext(os.path.basename(path))[0]
    sheet = excel.active

    col = csv.writer(open(f"{filename}.csv",
                          'w',
                          newline="", encoding='utf-8-sig'))

    for r in sheet.rows:
        col.writerow([cell.value for cell in r])

    df = pd.DataFrame(pd.read_csv(f"{filename}.csv", low_memory=False))

    return df


def check_names():
    while True:
        global count
        path = input(f'Ingresa el archivo csv {count}')
        if os.path.exists(os.path.dirname(path) and path.endswith('.csv')):
            count += 1
            return path
            break
        else:
            print("No es un directorio/archivo válido")
            continue


def check_csv_shape():
    correct = 0

    path_1 = check_names()
    path_2 = check_names()

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
    else:
        print("El número de filas no es igual. Por favor revisa tus archivos")
