import unittest


from core.queries.querying import sort_query


class TestSortQuery(unittest.TestCase):

    def test_simple_query(self):
        query = ["gph03n1x", "<and>", "greece"]
        sorted_query = sort_query(query)
        self.assertEqual(sorted_query, ["gph03n1x", "<and>", "greece"])


suite = unittest.TestLoader().loadTestsFromTestCase(TestSortQuery)
unittest.TextTestRunner(verbosity=2).run(suite)
