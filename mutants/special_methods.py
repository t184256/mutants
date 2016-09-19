# Copyright (c) 2016 Alexander Sosedkin <monk@unboiled.info>
# Distributed under the terms of the MIT License, see below:
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


"""
This module defines a collection of special methods
and their fallback functions / canonical invocations.
Fallback function invocations will be tried
if the special method is missing.
At least they should fail like the real deal, right?

Taken from https://docs.python.org/3.5/reference/datamodel.html
"""


__all__ = ['SPECIAL_METHODS']


def _raise(exception_cls, *a, **kwa):
    raise exception_cls(*a, **kwa)


def _will_give_up(msg):
    return lambda *a, **kwa: RuntimeError(msg)


def _setitem(w, k, v):
    w[k] = v


def _delitem(w, k):
    del w[k]


SPECIAL_METHODS = {
    #'__new__': _will_give_up('no __new__'),
    #'__init__': _will_give_up('no __init__'),
    '__del__': lambda _: None,
    '__repr__': repr,
    '__str__': str,
    '__bytes__': bytes,
    '__format__': format,
    '__lt__': object.__lt__,
    '__le__': object.__le__,
    '__eq__': object.__eq__,
    '__ne__': object.__ne__,
    '__gt__': object.__gt__,
    '__ge__': object.__ge__,
    '__hash__': hash,
    '__bool__': bool,
    '__getattr__': getattr,
    '__getattribute__': object.__getattribute__,
    '__setattr__': setattr,
    '__delattr__': delattr,
    '__dir__': dir,
    '__get__': lambda w, i, o: w.__get__(i, o),
    '__set__': lambda w, i, o: w.__set__(i, o),
    '__delete__': lambda w, i, o: w.__delete__(i, o),
    '__prepare__': lambda w, n, b, **kwa: w.__prepare__(n, b, **kwa),
    '__instancecheck__': isinstance,
    '__subclasscheck__': issubclass,
    '__call__': lambda w, *a, **kwa: w(*a, **kwa),
    '__len__': len,
    '__length_hint__': len,  # FIXME
    '__getitem__': lambda w, k: w[k],
    '__setitem__': _setitem,
    #'__missing__',
    '__delitem__': _delitem,
    '__iter__': iter,
    '__reversed__': reversed,
    '__contains__': lambda w, i: i in w,
    '__neg__': lambda w: -w,
    '__pos__': lambda w: +w,
    '__abs__': abs,
    '__invert__': lambda w: ~w,
    '__complex__': complex,
    '__int__': int,
    '__float__': float,
    '__round__': round,
    '__index__': lambda w: w.__index__(),  # FIXME
    '__enter__': lambda w: w.__enter__(),  # FIXME
    '__exit__': lambda w, et, ev, tb: w.__exit__(et, ev, tb),  # FIXME
    '__await__': lambda w: w.__await__(),  # FIXME
    '__aiter__': lambda w: w.__aiter__(),  # FIXME
    '__anext__': lambda w: w.__anext__(),  # FIXME
    '__aenter__': lambda w: w.__aenter__(),  # FIXME
    '__aexit__': lambda w, et, ev, tb: w.__aexit__(et, ev, tb),  # FIXME
    # # And...
    # '__next__',
}


# Also add numerical operators to that dict:
_NUMERIC_SPECIAL_METHODS = set((
    'add', 'sub', 'mul', 'matmul', 'truediv', 'floordiv', 'mod', 'divmod',
    'pow', 'lshift', 'rshift', 'and', 'xor', 'or',
))


# All of these have three forms (__???__, __r???__ and __i???__)
# and should not require a fallback if missing
def _add_numeric_operators():  # let's not pollute namespace
    for numeric_name in _NUMERIC_SPECIAL_METHODS:
        for tmpl in ('__%s__', '__r%s__', '__i%s__'):
            name = tmpl % numeric_name
            try:
                SPECIAL_METHODS[name] = getattr(object, name)
            except AttributeError:
                SPECIAL_METHODS[name] = lambda w, o: NotImplemented
_add_numeric_operators()
del _add_numeric_operators
