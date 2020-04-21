"""
This is a simple example of a NetsBlox service in Python.
"""

import netsblox as nb
from netsblox import types

@nb.rpc('I am the simplest type of RPC')
def hello():
    return 'world'

@nb.rpc('I throw an exception...')
@nb.argument('msg', type=types.String, help='Exception message to throw')
def throws(msg):
    raise Exception(msg)

@nb.rpc('I can add numbers!')
@nb.argument('x', type=types.Number, help='The first number to sum')
@nb.argument('y', type=types.Number, help='The second number to sum')
def sum_nums(x, y):
    return x + y

