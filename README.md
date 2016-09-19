mutants, a Python library for objects that mutate on access
===========================================================


In short
--------
`mutants` allows to create Python objects that mutate on access.
It works by creating proxy objects
that change underlying objects on every access.


Demo
----
```python
import random

import mutants


n = mutants.OnAccessMutant(0, lambda n: n + 1)
print(n)                           # prints 1
print(n)                           # prints 2
print(n)                           # prints 3


class Duck:
    feathers = True

    def quack(self):
        print('quack')


class Wolf:
    teeth = 'sharp'

    def quack(self):
        print('no quack')


def random_animal():
    return random.choice([Duck(), Wolf()])

randy = mutants.ImmutableMutant(random_animal)
randy.quack()                      # prints 'quack' or 'no quack'
randy.quack()                      # prints 'quack' or 'no quack'
print(hasattr(randy, 'feathers'))  # prints 'True' or 'False'
randy.name = 'Randy'
print(hasattr(randy, 'name'))      # prints 'False', see below


def class_toggler(animal):
    if isinstance(animal, Duck):
        return Wolf
    return Duck

tracy = mutants.ClassHopperMutant(Duck(), class_toggler)
tracy.quack()                      # prints 'no quack' as it's a Wolf
tracy.quack()                      # prints 'quack' as it's a Duck
print(tracy.teeth)                 # prints 'sharp' as it's a Wolf
tracy.name = 'Tracy'
print(tracy.name)                  # prints 'Tracy'


def class_extender(animal):
    class SleepyAnimal(animal.__class__):
        def quack(self):
            super().quack()
            print('zzz')
    return SleepyAnimal

zetta = mutants.ClassHopperMutant(Duck(), class_extender)
zetta.quack()                      # prints 'quack' and 'zzz'
```


Details
-------
Depending on what you want, you can choose
one of two mutant kinds: ImmutableMutant and ClassyMutant
or make a custom OnAccessMutant.

### OnAccessMutant

`OnAccessMutant` is the core class of the library.
It wraps an object much like `wrapt.ObjectProxy` does.
But there's a callback that is called before each access
and has the ability to modify or replace the proxied object.

Usage: `OnAccessMutant(initial_object, callable_mutator)`
where: `callable_mutator(wrapped_object) -> new_wrapped_object`

### ImmutableMutant

`ImmutableMutant` can impersonate different objects.
Its constructor takes a callable.
Before each access, this callable is called to provide an object
that `ImmutableMutant` will impersonate.

Usage: `ImmutableMutant(callable_returning_objects_to_be_proxied)`

Modifying `ImmutableMutant` is probably a strange idea,
because it doesn't remember the objects that it impersonates
and the callable will probably return something else next time.

In this pure Python implementation it's implemented as:
```python
def ImmutableMutant(mutator):
    return OnAccessMutant(None, lambda _: mutator())
```
Future C extensions may implement it separately for performance benefits.

### ClassHopperMutant

`ClassHopper` reevaluates the class of the wrapped object on every access.
It's like `obj.__class__ = callable_returning_a_class()`,
but magically happening before every manipulation with the object.

Usage: `mutant.ClassHopper(initial_object, callable_returning_a_class)`

In this pure Python implementation it's implemented as:
```python
def ClassHopperMutant(initial_object, class_returning_callable, copy=True):

    from copy import copy as _copy

    def class_mutator(obj):
        obj.__class__ = class_returning_callable(obj)
        return obj

    if copy:
        initial_object = _copy(initial_object)

    return OnAccessMutant(initial_object, class_mutator)
```
Future C extensions may implement it separately for performance benefits.


More about mutants
------------------
`mutants` were born to serve the needs of another library, `hacks`,
that aids modifying object, function or class behaviour,
stacking such modifications
and switching `currently active modification stacks' easily on the fly.
Check it out on pypi: https://pypi.org/project/hacks

`mutants` is similar to `wrapt.ObjectProxy` or `lazy-object-proxy`
but with bugs and flexibility instead of laziness, caching and performance.
CPython/Python guys, please give us something cleaner to pull off our tricks!

`mutants` is currently in alpha state,
so send in pull requests if something is broken!


License
-------
`mutants` is distributed under the terms of the MIT License;
see [LICENSE.txt](LICENSE.txt).
