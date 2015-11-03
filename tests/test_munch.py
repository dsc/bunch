from munch import Munch
import unittest


class MunchTest(unittest.TestCase):

    def test_dir(self):
        m = Munch(a=1, b=2)
        self.assertEqual(dir(m), ['a', 'b'])

    def test_repr(self):
        m = Munch({'a b': 1, 'c': 5})
        self.assertEqual(dir(m), ['a b', 'c'])
        self.assertEqual('%r' % m, "Munch({'a b': 1, 'c': 5})")
        self.assertEqual(m, eval('%r' % m))


if __name__ == '__main__':
    unittest.main()