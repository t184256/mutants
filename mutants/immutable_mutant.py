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


"""A proxy that reevaluates the proxied instance on access."""


from .on_access_mutant import OnAccessMutant


__all__ = ['ImmutableMutant']


def ImmutableMutant(callable_returning_object_to_be_proxied):
    """
    A pseudoclass that proxies everything to another object.
    But this object doesn't have to be constant:
    it's reevaluated on every access by calling the provided callable.
    It behaves like it doesn't even store the proxied object!

    It's called 'immutable' because there's no point in,
    for example, setting attributes on it,
    as they will be lost on the very next reevaluation,
    before they can be accessed again.

    Usage: ImmutableMutant(callable_returning_objects_to_be_proxied)
    """

    def mutator(_):
        return callable_returning_object_to_be_proxied()

    return OnAccessMutant(initial_object=None, mutator_callable=mutator)
