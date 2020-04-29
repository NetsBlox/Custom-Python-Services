"""
Preprocessing utilities using gensim.

For more information about gensim, check out https://radimrehurek.com/gensim/
"""

import netsblox as nb
from netsblox import types
from gensim.summarization.textcleaner import replace_abbreviations, get_sentences, clean_text_by_sentences
import os
from os import path

@nb.rpc('Convert text into sentences')
@nb.argument('text', type=types.String)
@nb.argument('replaceAbbreviations', type=types.Boolean, help='Replace abbreviations to ensure they are not mistaken as sentence boundaries.')
def getSentences(text, replaceAbbreviations=False):
    if replaceAbbreviations:
        text = replace_abbreviations(text)
    return list(get_sentences(text))

@nb.rpc('Clean and convert text into sentences')
@nb.argument('text', type=types.String)
def getCleanSentences(text):
    return [t.token for t in clean_text_by_sentences(text)]
