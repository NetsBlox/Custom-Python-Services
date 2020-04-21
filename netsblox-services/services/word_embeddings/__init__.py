"""
Train custom word embeddings from a corpus
"""

import netsblox
from netsblox import types
#from gensim.models import Word2Vec

# @netsblox.rpc(help='Train a word2vec model and save it')
# @netsblox.argument('text', type=types.String, help='The first number to sum')
# @netsblox.argument('name', type=types.String, help='The second number to sum')
# def trainWord2Vec(text, save_name):
    # return 'world'

@netsblox.rpc(help='List available trained models')
def listModels():
    return []

# @netsblox.rpc(help='I can add numbers!')
# @netsblox.argument('x', type=types.String, help='The first number to sum')
# @netsblox.argument('y', type=types.String, help='The second number to sum')
# def sum_nums(x, y):
    # return x + y

