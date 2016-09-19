import mutants


class Duck:
    def quack(self):
        return 'quack'


class Wolf:
    def quack(self):
        return 'no quack'


def test_basic_duckwolf():
    def duckwolf_generator():
        yield Duck()
        yield Duck()
        while True:
            yield Wolf()
    duckwolf_iter = iter(duckwolf_generator())

    duckwolf = mutants.ImmutableMutant(duckwolf_iter.__next__)
    assert duckwolf.quack() == 'quack'
    assert duckwolf.quack() == 'quack'
    assert duckwolf.quack() == 'no quack'
    assert duckwolf.quack() == 'no quack'


def test_basic_restoration():
    dee = mutants.ImmutableMutant(lambda: Duck())

    dee.name = 'Misnamed'  # Will not get applied
    assert not hasattr(dee, 'name')

    dee.quack = NotImplemented  # Will get restored on next access
    assert dee.quack() == 'quack'

    l = mutants.ImmutableMutant(lambda: [1, 2, 3])
    assert l == [1, 2, 3]
    assert [1, 2, 3] == l

    l.append(4)
    assert l == [1, 2, 3]

    assert l + [4] == [1, 2, 3, 4]

    l.extend([4])
    assert l == [1, 2, 3]

    l += [4]                  # The assignment breaks the proxy,
    assert l == [1, 2, 3, 4]  # as lists do not implement __iadd__.
    # TODO: Should that be hacked around with safeguard __i???__s?
    # Probably not.


def test_completeness_str():
    test = mutants.ImmutableMutant(lambda: 'test')
    assert type(test) != str  # !!!
    assert test.__class__ == str
    assert str(test) == 'test'

    assert test.__eq__('test')
    assert test == 'test'
    assert 'test' == test
    assert test != 'tset'

    assert isinstance(test, str)
    assert str(test) == 'test'
    assert test + 'X' == 'testX'
    # assert 'X' + test == 'Xtest'  # FIXME
    assert test + 'test' == 'test' + 'test'
    # assert 'test' + test == 'test' + 'test'  # FIXME
    # assert test + test == 'test' + 'test'  # FIXME
    assert test * 3 == 'test' * 3
    assert 3 * test == 3 * 'test'

    assert 'test' in test
    # assert test in 'test'  # FIXME
    # assert test in test  # FIXME

    assert dir(test) == dir('test')
    for attrname in dir(test):
        original_attr = getattr('test', attrname)
        immutant_attr = getattr(test, attrname)
        assert original_attr == immutant_attr


def test_everyone_is_a_mutant():
    s = mutants.ImmutableMutant(lambda: 6)
    t = mutants.ImmutableMutant(lambda: ([1, 2, 3], [4, 5, s]))
    mzip = mutants.ImmutableMutant(lambda: zip)

    l = list(mzip(*t))
    assert l == [(1, 4), (2, 5), (3, 6)]


def test_generator_breaks():
    range_2 = (x for x in range(2))
    assert range_2.__next__() == 0
    assert range_2.__next__() == 1

    broken_range_2 = mutants.ImmutableMutant(lambda: (x for x in range(2)))
    assert broken_range_2.__next__() == 0
    assert broken_range_2.__next__() == 0  # broken_range_2 is reset on access
    assert broken_range_2.__next__() == 0

    # But
    assert list(broken_range_2) == [0, 1]
