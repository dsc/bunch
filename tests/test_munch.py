from munch import Munch


def test_dir():
    m = Munch(a=1, b=2)
    assert dir(m) == ['a', 'b']
