import unittest
from representation import Variable, OrCollection, AndCollection, Collection

class MyTestCase(unittest.TestCase):
    def test_variable_parsing(self):
        a = Variable(name="a", negated=False)
        self.assertEqual(str(a), "a")
        a_from_str = Variable.from_str("a")
        self.assertEqual(a_from_str.name, "a")
        self.assertEqual(a_from_str.negated, False)

        b = Variable(name="b", negated=True)
        self.assertEqual(str(b), "~b")
        b_from_str = Variable.from_str("~b")
        self.assertEqual(b_from_str.name, "b")
        self.assertEqual(b_from_str.negated, True)

    def test_parse_or_collection(self):
        or_collection_str_1 = "(a | b | c)"
        or_collection_str_2 = "a | b | c"

        or_collection_1 = OrCollection.from_str(or_collection_str_1)
        self.assertEqual(len(or_collection_1.variables), 3)
        self.assertEqual(or_collection_str_1, str(or_collection_1))
        self.assertFalse(or_collection_1.negated)

        or_collection_2 = OrCollection.from_str(or_collection_str_2)
        self.assertEqual(len(or_collection_2.variables), 3)
        self.assertEqual("(" + or_collection_str_2 + ")", str(or_collection_2))
        self.assertFalse(or_collection_2.negated)

    def test_parse_and_collection(self):
        and_collection_str_1 = "(a & b & c)"
        and_collection_str_2 = "a & b & c"

        and_collection_1 = AndCollection.from_str(and_collection_str_1)
        self.assertEqual(len(and_collection_1.variables), 3)
        self.assertEqual(and_collection_str_1, str(and_collection_1))
        self.assertFalse(and_collection_1.negated)

        and_collection_2 = AndCollection.from_str(and_collection_str_2)
        self.assertEqual(len(and_collection_2.variables), 3)
        self.assertEqual("(" + and_collection_str_2 + ")", str(and_collection_2))
        self.assertFalse(and_collection_2.negated)

    def test_nested_collection(self):
        test_str = "(a & (b | c))"

        collection = Collection.from_str(test_str)
        self.assertEqual(str(collection), test_str)

        test_str = "((a | b) & c)"

        collection = Collection.from_str(test_str)
        self.assertEqual(str(collection), test_str)

        test_str = "(a | (b & c))"

        collection = Collection.from_str(test_str)
        self.assertEqual(str(collection), test_str)

        test_str = "((a & b) | c)"

        collection = Collection.from_str(test_str)
        self.assertEqual(str(collection), test_str)

    def test_double_nested_collection(self):
        test_str = "((a & b) | (c & d))"

        collection = Collection.from_str(test_str)
        self.assertEqual(str(collection), test_str)

        test_str = "((a | b) & (c | d))"

        collection = Collection.from_str(test_str)
        self.assertEqual(str(collection), test_str)

if __name__ == '__main__':
    unittest.main()
