from csv_converter import convert_to_csv, check_csv_shape, find_excel_filenames
from check_esp import merge_csvs, get_path

valid_path = get_path()

if __name__ == '__main__':
    file_1, file_2 = map(lambda x: convert_to_csv(x), find_excel_filenames(valid_path))
    if check_csv_shape(file_1, file_2):
        merge_csvs(valid_path, file_1, file_2)
    else:
        pass
