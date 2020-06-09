#!/usr/bin/env python3

import os
import pandas as pd
import convbase as cb
import matplotlib.pyplot as plt

columns_list =['Wavelenght', 'Absorbance', 'Normalized', 'Max wavelenght']

plot_props = {
        'title' : 'Absorption',
        'xlabel' :  r'$\lambda$ [nm]',
        'ylabel' : 'A',
}

def create_plot(x_val, y_val, file_desc):
    fig = plt.figure()
    splot = fig.add_subplot(1, 1, 1)
    splot.plot(x_val, y_val, '-', label=file_desc['label'])
    splot.set(**plot_props)
    splot.margins(x=0)
    splot.legend(loc='best', frameon=False)
    plot_file = cb.get_new_extension(file_desc['filename'], 'png')
    fig.savefig(plot_file, dpi=600, bbox_inches='tight')

def main():
    config = cb.get_config('absplot.conf')
    try:
        data_files_list = cb.get_config('files_list.txt')
        data_files_list = dict(sorted(data_files_list.items()))
    except Exception as e:
        print(e)
        data_files_list = cb.get_files_dict(os.getcwd(), 'csv')
    fig_all = plt.figure()
    bx = fig_all.add_subplot(1, 1, 1)
    if config['set_x_lim']:
        bx.set_xlim(config['x_lim_min'], config['x_lim_max'])
    for data_file in data_files_list.values():
        try:
            print('-> Processing file: {}...'.format(data_file['filename']))
            data_sheet = pd.read_csv(data_file['filename'], names=columns_list)
            data_sheet.drop([0, 1], inplace=True)
            data_sheet.reset_index(drop=True, inplace=True)
            for column_name in columns_list[:2]:
                data_sheet[column_name] = pd.to_numeric(data_sheet[column_name])
            data_sheet['Normalized'] = cb.normalize(data_sheet['Absorbance'])
            data_sheet['Max wavelenght'][0] = data_sheet['Wavelenght'][data_sheet['Absorbance'].idxmax()]
            if config['data_type']:
                spec_value = data_sheet['Normalized']
            else:
                spec_value = data_sheet['Absorbance']
            bx.plot(data_sheet['Wavelenght'], spec_value, '-', label=data_file['label'])
            if config['create_single_plots']:
                create_plot(data_sheet['Wavelenght'], spec_value, data_file)
        except Exception as e:
            print(e)
        else:
            print('    Processing of {} sucessful.'.format(data_file['filename']))
    bx.set(**plot_props)
    bx.margins(x=0)
    bx.legend(loc='best', frameon=False)
    fig_all.savefig('all_plots.png', dpi=600, bbox_inches='tight')
    cb.save_files_dict(data_files_list, 'files_list.txt')

if __name__ == '__main__':
    main()