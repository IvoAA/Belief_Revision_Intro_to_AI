import unittest
from BeliefBase import BeliefBase
from AGM import Contraction


class AGMTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(AGMTestCase, self).__init__(*args, **kwargs)
        self.default_kb = "(p) & (p & q) & (p | q) & ((p >> q) & (q >> p))"

    def test_contraction_success(self):
        bb = BeliefBase()
        bb.tell(self.default_kb)

        self.assertTrue(Contraction.success_postulate(bb=bb, sentence="p"))

    def test_contraction_inclusion(self):
        bb = BeliefBase()
        bb.tell(self.default_kb)

        self.assertTrue(Contraction.inclusion_postulate(bb=bb, sentence="p"))

    def test_contraction_vacuity(self):
        bb = BeliefBase()
        bb.tell(self.default_kb)

        self.assertTrue(Contraction.vacuity_postulate(bb=bb, sentence="r"))

    def test_contraction_extensionality(self):
        bb = BeliefBase()
        bb.tell(self.default_kb)

        self.assertTrue(Contraction.extensionality_postulate(bb=bb, literals=["p", "p"]))





if __name__ == '__main__':
    unittest.main()
