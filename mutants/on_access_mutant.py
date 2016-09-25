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


"""A wrapper that reevaluates the wrapped instance on access."""


from .special_methods import SPECIAL_METHODS


__all__ = ['OnAccessMutant']


def _delegate_or(smethname, func):
    """
    Produce a method that calls either the existing method of the wrapped
    object with the same name or a special invocation if it's missing
    (see SPECIAL_METHODS in special_methods.py).

    Usage: OnAccessMutant(initial_object, callable_mutator)
    where: callable_mutator(wrapped_object) -> new_wrapped_object
    """
    def delegated(self, *a, **kwa):
        # Mutate the object before access
        wrapped = object.__getattribute__(self, '__wrapped_object__')
        mutator = object.__getattribute__(self, '__wrapped_mutator__')
        wrapped = mutator(wrapped)
        object.__setattr__(self, '__wrapped_object__', wrapped)

        # Proxy access or use a fallback function
        try:
            meth = getattr(wrapped, smethname)
        except AttributeError:
            return func(wrapped, *a, **kwa)
        if not isinstance(wrapped, type):
            return meth(*a, **kwa)
        else:
            meth = getattr(type(wrapped), smethname)
            return meth(wrapped, *a, **kwa)

    return delegated


class _MetaImmutableMutant(type):
    """
    We don't want to override __new__ for OnAccessMutant,
    so let's hack into the instantiation with a metaclass:
    """
    def __call__(cls, initial_object, mutator_callable, *a, **kwa):
        immutant = cls.__new__(cls, *a, **kwa)
        object.__setattr__(immutant, '__wrapped_object__', initial_object)
        object.__setattr__(immutant, '__wrapped_mutator__', mutator_callable)
        return immutant


class OnAccessMutant(metaclass=_MetaImmutableMutant):
    """
    A class that proxies everything to another object.
    The quirk that it can change the proxied object on every access
    witha mutator function.
    But this object doesn't have to be constant:
    it's reevaluated on every access by calling the provided callable.

    Usage: OnAccessMutant(initial_object, callable_mutator)
    where: callable_mutator(wrapped_object) -> new_wrapped_object
    """

    __slots__ = ('__wrapped_object__', '__wrapped_mutator__')


def _extend_on_access_mutant():  # let's not pollute namespace
    for special_method_name, func_if_missing in SPECIAL_METHODS.items():
        delegated = _delegate_or(special_method_name, func_if_missing)
        setattr(OnAccessMutant, special_method_name, delegated)
_extend_on_access_mutant()
del _extend_on_access_mutant
