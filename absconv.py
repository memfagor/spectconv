#!/usr/bin/env python3

import os
import pandas as pd
import convbase as cb
import matplotlib.pyplot as plt

columns_list =['Wavelenght', 'Absorbance', 'Normalized', 'Max wavelenght']

plot_props = {
        'title' : 'Absorption',
        'xlabel' : 'Wavelenght [nm]',
        'ylabel' : 'Intensity [AU]',
}

def create_plot(x_val, y_val, file_name):
    fig = plt.figure()
    splot = fig.add_subplot(1, 1, 1)
    splot.plot(x_val, y_val, '-', label=cb.get_file_name(file_name))
    splot.set(**plot_props)
    splot.margins(x=0)
    splot.legend(loc='best', frameon=False)
    plot_file = cb.get_new_extension(file_name, 'png')
    fig.savefig(plot_file, dpi=600, bbox_inches='tight')


def main():
    config = cb.get_config('absconv.conf')
    data_files_list = cb.get_files_list(os.getcwd(), 'csv')
    fig_all = plt.figure()
    bx = fig_all.add_subplot(1, 1, 1)
    for data_file in data_files_list:
        try:
            print('-> Processing file: {}...'.format(data_file))
            data_sheet = pd.read_csv(data_file, names=columns_list)
            data_sheet.drop([0, 1], inplace=True)
            data_sheet.reset_index(drop=True, inplace=True)
            for column_name in columns_list[:2]:
                data_sheet[column_name] = pd.to_numeric(data_sheet[column_name])
            data_sheet['Normalized'] = cb.normalize(data_sheet['Absorbance'])
            data_sheet['Max wavelenght'][0] = data_sheet['Wavelenght'][data_sheet['Absorbance'].idxmax()]
            create_plot(data_sheet['Wavelenght'], data_sheet['Normalized'], data_file)
            bx.plot(data_sheet['Wavelenght'], data_sheet['Absorbance'], '-', label=cb.get_file_name(data_file))
            excel_file = cb.get_new_extension(data_file, 'xlsx')
            data_sheet.to_excel(excel_file)
        except Exception as e:
            print(e)
        else:
            print('   Processing sucessful, {} created.'.format(excel_file))
    bx.set(**plot_props)
    bx.margins(x=0)
    bx.legend(loc='best', frameon=False)
    fig_all.savefig('all_plots.png', dpi=600, bbox_inches='tight')

if __name__ == '__main__':
    main()
