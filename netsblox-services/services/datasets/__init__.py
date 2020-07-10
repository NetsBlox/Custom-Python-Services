"""
Build datasets incrementally on the server for use with Word2Vec service.

First, create a new dataset. Then add data to it and pass the name to Word2Vec.trainModel!
"""

import netsblox as nb
from netsblox import types
import os
from os import path
import pickle
import shutil

data_dir = path.join(path.dirname(__file__), 'data')

def get_dataset(name, default=None):
    try:
        data_path = path.join(data_dir, name, 'data.pkl')
        with open(data_path, 'rb') as f:
            return pickle.load(f)
    except:
        return default

def dataset_exists(name):
    return path.isdir(path.join(data_dir, name))

@nb.rpc('Initialize a new dataset')
@nb.argument('dataset', type=types.String, help='Name of dataset to create.')
def create(dataset):
    if not dataset.isalnum():
        raise Exception('Invalid dataset name. Must be alphanumeric.')
    os.makedirs(path.join(data_dir, dataset), exist_ok=True)

    return 'Dataset created!'

@nb.rpc('Add data to an existing dataset')
@nb.argument('dataset', type=types.String, help='Name of dataset.')
@nb.argument('data', type=types.List, help='Data to append to dataset.')
def addData(dataset, data):
    if not dataset_exists(dataset):
        raise Exception('Dataset not found.')

    current_data = get_dataset(dataset, [])
    current_data.extend(data)
    with open(path.join(data_dir, dataset, 'data.pkl'), 'wb') as f:
        pickle.dump(current_data, f)

@nb.rpc('Delete a dataset')
@nb.argument('dataset', type=types.String, help='Name of dataset.')
def delete(dataset):
    if not dataset_exists(dataset):
        raise Exception('Dataset not found.')

    dataset_dir = path.isdir(path.join(data_dir, name))
    shutil.rmtree(dataset_dir)

@nb.rpc('Download a dataset. This is not required for use with Word2Vec service.')
@nb.argument('dataset', type=types.String, help='Name of dataset.')
def download(dataset):
    if not dataset_exists(dataset):
        raise Exception('Dataset not found.')

    return get_dataset(dataset)
