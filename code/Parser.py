import glob
import pandas as pd
import re
import os
from functools import reduce

# Just so I don't keep multiple copies of the raw data
rectangle_dir = '/home/eduardo/PycharmProjects/dynamic-treemap-resources/rectangles'
dataset_dir = '/home/eduardo/PycharmProjects/dynamic-treemap-resources/dataset'


def parse_dataset(dataset_id):
    input_dir = dataset_dir + '/' + dataset_id
    files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
    files = natural_sort(files)
    dfs = [pd.read_csv(file) for file in files]
    df_full = reduce((lambda x, y: pd.merge(x, y, how='outer', on='id')), dfs)
    df_full.columns = ['id'] + ['t'+str(i) for i in range(df_full.shape[1]-1)]
    return df_full


def parse_rectangles(technique_id, dataset_id):
    path = rectangle_dir + '/' + technique_id + '/' + dataset_id
    files = [filename for filename in glob.iglob(path + '**/*.rect', recursive=True)]
    files = natural_sort(files)
    # Read each file into a dataframe
    dfs = [pd.read_csv(file, names=['id', 'x', 'y', 'w', 'h']) for file in files]
    return dfs


def natural_sort(l):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)


def list_datasets():
    return natural_sort(os.listdir(dataset_dir))


def list_techniques():
    return natural_sort(os.listdir(rectangle_dir))