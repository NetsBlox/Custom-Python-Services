"""
Train custom word embeddings using gensim.

For more information about gensim, check out https://radimrehurek.com/gensim/
"""

import netsblox as nb
from netsblox import types
from gensim.models import Word2Vec
from gensim.test.utils import common_texts
import os
from os import path

models_dir = path.join(path.dirname(__file__), 'models')
os.makedirs(models_dir, exist_ok=True)

@nb.rpc(help='Train a word2vec model and save it')
@nb.argument('wordLists', type=types.List, help='List of word lists')
@nb.argument('saveName', type=types.String, help='Name for trained model')
@nb.argument('size', type=types.Integer, help='Dimensionality of the word vectors', optional=True)
@nb.argument('window', type=types.Integer, help='Max distance between current and predicted word', optional=True)
@nb.argument('minCount', type=types.Integer, help='Ignore words with fewer than this number of occurrences', optional=True)
def trainWord2Vec(wordLists, saveName, size=100, window=5, minCount=2):
    model = Word2Vec(wordLists, size=size, window=window, min_count=minCount)
    model.save(path.join(models_dir, saveName))
    return 'Model saved as ' + saveName

@nb.rpc('Get the number of words in the vocabulary')
@nb.argument('modelName', type=types.String, help='Name of trained model')
def getWord2VecVocabSize(modelName):
    model = Word2Vec.load(path.join(models_dir, modelName))
    return model.wv.vectors.shape[0]

@nb.rpc('Get the entire vocabulary of a trained model.\n\nWarning: this can be quite large.')
@nb.argument('modelName', type=types.String, help='Name of trained model')
def getWord2VecVocab(modelName):
    model = Word2Vec.load(path.join(models_dir, modelName))
    return list(model.wv.vocab.keys())

@nb.rpc('Get the top-N most similar words. Positive words contribute positively to similarity; negative words contribute negatively')
@nb.argument('modelName', type=types.String, help='Name of trained model')
@nb.argument('positive', type=types.List, help='Words that contribute positively')
@nb.argument('negative', type=types.List, help='Words that contribute negatively', optional=True)
@nb.argument('count', type=types.Integer, help='Number of words to return', optional=True)
def getMostSimilar(modelName, positive, negative=[], count=5):
    model = Word2Vec.load(path.join(models_dir, modelName))
    return model.wv.most_similar(positive, negative, count)

@nb.rpc('Get the vector representation for a given word')
@nb.argument('modelName', type=types.String, help='Name of trained model to use')
@nb.argument('word', type=types.String)
def getWordVector(modelName, word):
    model = Word2Vec.load(path.join(models_dir, modelName))
    vector = model.wv.word_vec(word)
    return [ float(n) for n in vector ]


@nb.rpc('Fetch example text (common texts from gensim)')
def exampleText():
    return common_texts

@nb.rpc('List available trained models')
def listModels():
    return os.listdir(models_dir)

@nb.rpc('Delete trained model')
@nb.argument('modelName', type=types.String, help='Name of trained model to delete')
def deleteModel(modelName):
    os.remove(path.join(models_dir, modelName))
    return os.listdir(models_dir)

