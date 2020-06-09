#!/usr/bin/env python3

import os
import json
import pandas as pd


def get_config(filename):
    with open(os.path.join(os.getcwd(), filename), 'r') as config_file:
        config = json.load(config_file)
    return config

def get_files_list(dir_path, extension):
    return [f for f in os.listdir(dir_path) if extension in os.path.splitext(f)[1][1:]]

def get_files_dict(dir_path, extension):
    return {str(i).zfill(3): {'filename': f, 'label': str(i)} for i, f in enumerate(get_files_list(dir_path, extension))}

def save_files_dict(data, filename):
    with open(os.path.join(os.getcwd(), filename), 'w') as list_file:
        json.dump(data, list_file, sort_keys=True, indent=4)

def normalize(target):
    max = target.max()
    min = target.min()
    if not max == min:
        result = (target - min)/(max - min)
    else:
        result = 0
    return result

def standarize(target):
    mean = target.mean()
    std = target.std()
    if not std == 0:
        result = (target - mean)/std
    else:
        result = 0
    return result

def get_file_name(file_name):
    return os.path.splitext(file_name)[0]

def get_new_extension(file_name, extension):
    return '.'.join((get_file_name(file_name), extension))

def save_to_excel(dfs, path):
    with pd.ExcelWriter(path) as writer:
        for n, df in enumerate(dfs):
            df.to_excel(writer, 'Sheet{}'.format(n+1))
        writer.save()

def tests():
    pass

if __name__ == '__main__':
    tests()
