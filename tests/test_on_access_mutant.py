import mutants


def test_on_access_mutant_basic():
    n = mutants.OnAccessMutant(0, lambda n: n + 1)
    assert n == 1
    assert n == 2
    assert n == 3
