#!/usr/bin/env python3

import os
import specio
import pandas as pd
import convbase as cb
import matplotlib.pyplot as plt

columns_list =['Wavelength', 'Emission', 'Max wavelength', 'Normalized',
        'Standarized', 'Parameters', 'Values']


def get_data(obj):
    data = {}
    data[columns_list[0]] = obj.wavelength
    data[columns_list[1]] = obj.amplitudes
    return pd.DataFrame(data)


def get_params(obj):
    data = {}
    data[columns_list[5]] = list(obj.meta.keys())
    data[columns_list[6]] = list(obj.meta.values())
    return pd.DataFrame(data)


def sp_to_dataframes(file_name):
    spectra = specio.specread(file_name)
    return get_data(spectra), get_params(spectra)


def main():
    config = cb.get_config('emiconv.conf')
    data_files_list = cb.get_files_list(os.getcwd(), 'sp')
    for data_file in data_files_list:
        try:
            print('-> Processing file: {}...'.format(data_file))
            data_sheet, parameters = sp_to_dataframes(data_file)
            data_sheet  = data_sheet.reindex(columns = columns_list[:-2])
            if config['normalization']:
                data_sheet[columns_list[3]] = cb.normalize(data_sheet[columns_list[1]])
            if config['standarization']:
                data_sheet[columns_list[4]] = cb.standarize(data_sheet[columns_list[1]])
            data_sheet[columns_list[2]][0] = data_sheet[columns_list[0]][data_sheet[columns_list[1]].idxmax()]
            parameters[columns_list[6]][1] = '2D constant interval dataset file'
            excel_file = cb.get_new_extension(data_file, 'xlsx')
            cb.save_to_excel([data_sheet, parameters], excel_file)
        except Exception as e:
            print(e)
        else:
            print('   Processing sucessful, {} created.'.format(excel_file))

if __name__ == '__main__':
    main()
