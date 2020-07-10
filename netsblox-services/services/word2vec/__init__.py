"""
Train custom word2vec models using gensim.

For more information about gensim, check out https://radimrehurek.com/gensim/
"""

import netsblox as nb
from netsblox import types
from gensim.models import Word2Vec, KeyedVectors
from gensim.test.utils import common_texts
import os
from os import path
from flask import request
import services.datasets as datasets

service_name = 'Word2Vec'

def read_list(filepath):
    if path.isfile(filepath):
        with open(filepath, 'r') as f:
            return [ line.strip() for line in f.readlines() ]
    else:
        return []

models_dir = path.join(path.dirname(__file__), 'models')
public_models_file = path.join(models_dir, 'public-models.txt')
public_models = read_list(public_models_file)
public_vectors_file = path.join(models_dir, 'public-wv.txt')
public_vectors = read_list(public_vectors_file)

for wv_name in public_vectors:
    public_models.append(wv_name)

def resolve_model_name(model_name):
    if not path.sep in model_name:
        model_name = username() + path.sep + model_name
    return model_name

def set_model_public(model_name):
    if model_name not in public_models:
        public_models.append(model_name)
        with open(public_models_file, 'w') as f:
            f.write('\n'.join(public_models))

def set_model_private(model_name):
    if model_name in public_models:
        public_models.remove(model_name)
        with open(public_models_file, 'w') as f:
            f.write('\n'.join(public_models))


def ensure_exists(modelName):
    model_path = path.join(models_dir, modelName)
    exists = path.isfile(model_path)
    if not exists:
        raise Exception('Model not found')

def ensure_logged_in():
    if not username():
        raise Exception('Please log in to use this feature')

def ensure_valid_name(model_name):
    user_prefix = username() + path.sep
    if model_name.startswith(user_prefix):
        model_name = model_name[len(user_prefix):]

    if not model_name.isalnum():
        raise Exception('Invalid model name. Must be alphanumeric.')

def username():
    return request.args.get('username')

def is_own_model(modelName):
    return modelName.startswith(username() + path.sep)

def load_model(model_name):
    model_name = resolve_model_name(model_name)
    err_msg = 'Model not found (or is not public!)'
    ensure_exists(model_name)

    is_public = model_name in public_models
    if not (is_own_model(model_name) or is_public):
        raise Exception('Cannot access model another user\'s private model')

    model_path = path.join(models_dir, model_name)
    model = Word2Vec.load(model_path)
    return model

def load_wv(model_name):
    if model_name in public_vectors:
        return KeyedVectors.load(path.join(models_dir, model_name))
    else:
        return load_model(model_name).wv

@nb.rpc('Train a word2vec model and save it')
@nb.argument('sentences', type=types.List, help='List of word lists or dataset name (from Datasets service)')
@nb.argument('saveName', type=types.String, help='Name for trained model')
@nb.argument('size', type=types.Integer, help='Dimensionality of the word vectors (default: 100)', optional=True)
@nb.argument('window', type=types.Integer, help='Max distance between current and predicted word (default: 5)', optional=True)
@nb.argument('minCount', type=types.Integer, help='Ignore words with fewer than this number of occurrences (default: 2)', optional=True)
def trainModel(sentences, saveName, size=100, window=5, minCount=2):
    sentences = datasets.get_dataset(sentences, sentences)
    ensure_logged_in()
    ensure_valid_name(saveName)
    model = Word2Vec(sentences, size=size, window=window, min_count=minCount)
    saveName = resolve_model_name(saveName)
    saveFile = path.join(models_dir, saveName)
    os.makedirs(path.dirname(saveFile), exist_ok=True)
    model.save(saveFile)
    return 'Model saved as ' + saveName

@nb.rpc('Get the number of words in the vocabulary')
@nb.argument('modelName', type=types.String, help='Name of trained model')
def getVocabSize(modelName):
    wv = load_wv(modelName)
    return wv.vectors.shape[0]

@nb.rpc('Get the entire vocabulary of a trained model.\n\nWarning: this can be quite large.')
@nb.argument('modelName', type=types.String, help='Name of trained model')
def getVocab(modelName):
    wv = load_wv(modelName)
    return list(wv.vocab.keys())

@nb.rpc('Get the top-N most similar words. Positive words contribute positively to similarity; negative words contribute negatively')
@nb.argument('modelName', type=types.String, help='Name of trained model')
@nb.argument('positive', type=types.List, help='Words that contribute positively', optional=True)
@nb.argument('negative', type=types.List, help='Words that contribute negatively', optional=True)
@nb.argument('count', type=types.Integer, help='Number of words to return (default: 5)', optional=True)
def getMostSimilarWords(modelName, positive=[], negative=[], count=5):
    num_examples = len(positive) + len(negative)
    if num_examples == 0:
        raise Exception('Positive and/or negative examples required.')

    wv = load_wv(modelName)
    return wv.most_similar(positive, negative, count)

@nb.rpc('Get the vector representation for a given word')
@nb.argument('modelName', type=types.String, help='Name of trained model to use')
@nb.argument('word', type=types.String)
def getWordVector(modelName, word):
    wv = load_wv(modelName)
    vector = wv.word_vec(word)
    return [ float(n) for n in vector ]

@nb.rpc('Get the vector representation for a given word')
@nb.argument('modelName', type=types.String, help='Name of trained model to use')
@nb.argument('words', type=types.List)
def getWordVectors(modelName, words):
    wv = load_wv(modelName)
    vectors = ( wv.word_vec(word) for word in words )
    return [[ float(n) for n in vector ] for vector in vectors ]


@nb.rpc('Fetch example text (common texts from gensim)')
def exampleText():
    first_sentence = ['these', 'are', 'example', 'sentences']
    sentences = [first_sentence];
    sentences.extend(common_texts)
    return sentences

@nb.rpc('List available trained models')
def listModels():
    ensure_logged_in()
    user_models_dir = path.join(models_dir, username())
    models = os.listdir(user_models_dir) if path.isdir(user_models_dir) else []
    return models

@nb.rpc('List public trained models')
def listPublicModels():
    return public_models

@nb.rpc('Make model available to other users')
@nb.argument('modelName', type=types.String, help='Name of trained model to publish')
def publish(modelName):
    ensure_logged_in()
    modelName = resolve_model_name(modelName)
    if not is_own_model(modelName):
        owner = modelName.split(path.sep)[0]
        raise Exception(f'Cannot publish model belonging to {owner}')
    ensure_exists(modelName)
    set_model_public(modelName)

@nb.rpc('Make model private and only available to yourself')
@nb.argument('modelName', type=types.String, help='Name of trained model to publish')
def unpublish(modelName):
    ensure_logged_in()
    modelName = resolve_model_name(modelName)
    if not is_own_model(modelName):
        owner = modelName.split(path.sep)[0]
        raise Exception(f'Cannot unpublish model belonging to {owner}')
    ensure_exists(modelName)
    set_model_private(modelName)

@nb.rpc('Delete trained model')
@nb.argument('modelName', type=types.String, help='Name of trained model to delete')
def deleteModel(modelName):
    ensure_logged_in()
    modelName = resolve_model_name(modelName)
    if not is_own_model(modelName):
        owner = modelName.split(path.sep)[0]
        raise Exception(f'Cannot delete model belonging to {owner}')

    set_model_private(modelName)
    os.remove(path.join(models_dir, modelName))

