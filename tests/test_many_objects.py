import gc
import random
import sys

from nose.plugins.skip import SkipTest

import mutants


def LazyMutant(obj):
    return mutants.OnAccessMutant(obj, lambda x: x)


def find_difference(obj, mutant, func):
    try:
        o1 = func(obj)
        o2 = func(obj)
        assert o1 == o2
        if not o1 == o2 or not o1.__eq__(o2):
            return  # inconsistent equality
    except:
        return  # TODO: extend

    om = func(mutant)

    if not om == o1:
        return True


def inspect_for_differences(obj, func):
    mutant = LazyMutant(obj)
    if find_difference(obj, mutant, func):
        return True


def inspect_all_with(func):
    for obj in gc.get_objects():
        assert not inspect_for_differences(obj, func)


# Has been seen working with Python 3.5-3.6
def test_many_objects_ident():
    if sys.version_info < (3, 5):
        raise SkipTest("Skipped on Py<3.5")
    inspect_all_with(lambda x: x)


def test_many_objects_dir():
    inspect_all_with(lambda x: dir(x))


def test_many_objects_class():
    inspect_all_with(lambda x: x.__class__)


def test_many_objects_int():
    inspect_all_with(lambda x: int(x))


def test_many_objects_getattr_first():
    inspect_all_with(lambda x: getattr(x, dir(x)[0]))


# Is broken for now
#def test_many_objects_getattr_random():
#    inspect_all_with(lambda x: getattr(x, random.choice(dir(x))))


def test_many_objects_bool():
    inspect_all_with(lambda x: getattr(x, bool(x)))


def test_many_objects_str():
    inspect_all_with(lambda x: str(x))


# Breaks because of type() output in str in some classes.
# Like '<collections._Link object at 0x7fda883731b0>' vs
# '<weakproxy at 0x7fda880fdbd8 to _Link at 0x7fda883731b0>'
# Has been seen working with Python 3.5-3.6
def test_many_objects_repr():
    if sys.version_info < (3, 5):
        raise SkipTest("Skipped on Py<3.5")
    inspect_all_with(lambda x: repr(x))


# Doesn't work because of explicit type() checks
#def test_many_objects_add():
#    inspect_all_with(lambda x: x + x)
