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

    def test_negation_collection(self):
        test_str = "~(a | b)"

        collection = Collection.from_str(test_str)
        self.assertTrue(collection.negated)
        self.assertEqual(test_str, str(collection))

        test_str = "(a & ~(b | c))"

        collection = Collection.from_str(test_str)
        self.assertFalse(collection.negated)
        self.assertTrue(collection.variables[1].negated)
        self.assertEqual(test_str, str(collection))


    def test_double_nested_collection(self):
        test_str = "((a & b) | (c & d))"

        collection = Collection.from_str(test_str)
        self.assertEqual(str(collection), test_str)

        test_str = "((a | b) & (c | d))"

        collection = Collection.from_str(test_str)
        self.assertEqual(str(collection), test_str)

    def test_negation_variable(self):

        a = Variable.from_str("a")
        not_a = Variable.from_str("~a")

        self.assertFalse(a.negated)
        a.perform_negation()
        self.assertTrue(a.negated)

        self.assertTrue(not_a.negated)
        not_a.perform_negation()
        self.assertFalse(not_a.negated)

    def test_negation_parsing(self):
        test_str = "~(~a & ~b)"
        negated_test_str = "(a | b)"

        collection = Collection.from_str(test_str)
        self.assertEqual(negated_test_str, str(collection.resolve_negation()))
        print()

    def test_negation_conversion_of_collection(self):
        collection_str = "(a | b)"
        negated_collection_str = "~(~a & ~b)"

        collection = Collection.from_str(collection_str)
        self.assertFalse(collection.negated)

        new_collection = collection.perform_negation()
        self.assertEqual(negated_collection_str, str(new_collection))

        self.assertEqual(collection_str, str(new_collection.resolve_negation()))

        collection_str = "~(a | ~b)"
        negated_collection_str = "(~a & b)"
        collection = Collection.from_str(collection_str)
        new_collection = collection.resolve_negation()

        self.assertEqual(negated_collection_str, str(new_collection))

        self.assertEqual(collection_str, str(new_collection.perform_negation()))

        collection_str = "~(a | (~b & ~c))"
        negated_collection_str = "(~a & (b | c))"
        collection = Collection.from_str(collection_str)
        self.assertTrue(collection.negated)
        new_collection = collection.resolve_negation()
        self.assertFalse(new_collection.negated)
        self.assertEqual(negated_collection_str, str(new_collection))


        print()

if __name__ == '__main__':
    unittest.main()
