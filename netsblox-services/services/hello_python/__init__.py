"""
This is a simple example of a NetsBlox service in Python.
"""

import netsblox
from netsblox import types

@netsblox.rpc(help='I am the simplest type of RPC')
def hello():
    return 'world'

@netsblox.rpc(help='I can add numbers!')
@netsblox.argument('x', type=types.Number, help='The first number to sum')
@netsblox.argument('y', type=types.Number, help='The second number to sum')
def sum_nums(x, y):
    return x + y

