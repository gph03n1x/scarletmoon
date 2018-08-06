import unittest

from moon.ngrams import get_n_grams


class TestNGrams(unittest.TestCase):

    def test_get_n_grams(self):
        token = "results"
        token_n_grams = get_n_grams(token, 2)
        self.assertEqual(token_n_grams, ['$r', 're', 'es', 'su', 'ul', 'lt', 'ts', 's$'])


suite = unittest.TestLoader().loadTestsFromTestCase(TestNGrams)
unittest.TextTestRunner(verbosity=2).run(suite)
