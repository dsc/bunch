from munch import Munch

def test_dir():
    m = Munch(a=1, b=2)
    assert dir(m) == ['a', 'b']

def test_repr():
    m = Munch({'a b': 1, 'c': 5})
    assert dir(m) == ['a b', 'c']
    assert ('%r' % m) == "Munch({'a b': 1, 'c': 5})"
    assert m == eval(('%r' % m))
