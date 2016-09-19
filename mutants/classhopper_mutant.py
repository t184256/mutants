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


"""A wrapper that reevaluates the class of the wrapped instance on access."""


from .on_access_mutant import OnAccessMutant


__all__ = ['ClassHopperMutant']


def ClassHopperMutant(initial_object, class_returning_callable, copy=True):
    """
    ClassHopper: a wrapper that reevaluates the class of the wrapped instance
    on every access attempt.
    It's like obj.__class__ = callable_returning_a_class(),
    but magically happening before every manipulation with the object.

    Usage: mutant.ClassHopper(initial_object, callable_returning_a_class)
    """

    from copy import copy as _copy

    def class_mutator(obj):
        obj.__class__ = class_returning_callable(obj)
        return obj

    if copy:
        initial_object = _copy(initial_object)

    return OnAccessMutant(initial_object, class_mutator)
