import unittest
from BeliefBase import BeliefBase

class MyTestCase(unittest.TestCase):
    def test_telling_sentence_behaviour(self):
        bb = BeliefBase()

        self.assertEqual(len(bb.get_knowledge_base()), 0)

        clause_1 = "a | b"

        bb.tell(clause_1)
        self.assertEqual(len(bb.get_knowledge_base()), 1)

        clause_2 = "c & d"

        bb.tell(clause_2)
        self.assertEqual(len(bb.get_knowledge_base()), 3)


if __name__ == '__main__':
    unittest.main()
