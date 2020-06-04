"""
Fetch word embeddings from pretrained language models using spacy.

For more information, check out https://spacy.io/models
"""

import netsblox as nb
from netsblox import types
import spacy

model_names = {}
model_names['en'] = 'en_core_web_md'
# model_names['de'] = 'de_core_news_md'
model_names['es'] = 'es_core_news_md'
# model_names['fr'] = 'fr_core_news_md'
# model_names['el'] = 'el_core_news_md'

models = {}
for (lang, name) in model_names.items():
    models[lang] = spacy.load(name)

def to_list(vec):
    return [ float(n) for n in vec ]

@nb.rpc('Get supported languages with word vectors available')
def getSupportedLanguages():
    return list(model_names.keys())

@nb.rpc('Retrieve word vectors using the given language model')
@nb.argument('words', type=types.List, help='Word vectors to retrieve')
@nb.argument('language', type=types.String, help='Language model to use', optional=True)
def getWordVectors(words, language='en'):
    if language not in model_names:
        raise Exception(f'Unrecognized language: {language}')

    #nlp = spacy.load(model_names[language])
    nlp = models[lang]
    return [to_list(nlp(word).vector) for word in words]

@nb.rpc('Retrieve word vectors using the given language model')
@nb.argument('word', type=types.String, help='Word vector to retrieve')
@nb.argument('language', type=types.String, help='Language model to use', optional=True)
def getWordVector(word, language='en'):
    return next(getWordVectors([word], language))
