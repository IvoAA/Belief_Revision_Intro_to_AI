import unittest
from BeliefBase import BeliefBase
from utils import DPLL

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

    def test_dpll(self):
        input_sentence_false = "(~n | ~t) & (m | q | n) & (l | ~m) & (l | ~q) & (~l | ~p) & (r | p | n) & (~r | ~l) & (t)"

        bb_false = BeliefBase()

        bb_false.tell(input_sentence_false)
        self.assertFalse(DPLL(bb_false.get_knowledge_base()))

        input_sentence_true = "(p | q | r) & (p | q | ~r) & (p | ~q | r) & (p | ~q | ~r) & (~p | q | r) & (~p | q | ~r) & (~p | ~q | r)"

        bb_true = BeliefBase()
        bb_true.tell(input_sentence_true)

        self.assertTrue(DPLL(bb_true.get_knowledge_base()))

    def test_check_entailment(self):
        input_kb = "(p) & (p & q) & (p | q) & ((p >> q) & (q >> p))"
        new_input = "p"

        bb = BeliefBase()
        bb.tell(input_kb)
        self.assertTrue(bb.check_entailment(new_input))

        input_kb = "a & b & c"
        test_inputs = [
            ("a", True),
            ("~a", False),
            ("d", False),
            ("~d", False)
        ]

        bb = BeliefBase()
        bb.tell(input_kb)
        for sentence, expected_result in test_inputs:
            self.assertEqual(bb.check_entailment(sentence), expected_result)

    def test_contraction(self):
        input_kb = "(p) & (p & q) & (p | q) & ((p >> q) & (q >> p))"
        bb = BeliefBase()
        bb.tell(input_kb)

        self.assertEqual(bb.nr_clause, 5)



        bb.contraction("p")



if __name__ == '__main__':
    unittest.main()
