import unittest
from BeliefBase import BeliefBase
from AGM import Contraction, Revision


class AGMTestCase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(AGMTestCase, self).__init__(*args, **kwargs)
        self.default_contraction_kb = "(p) & (p & q) & (p | q) & ((p >> q) & (q >> p))"
        self.default_revision_kb = "(p) & (q) & (p >> q)"

    def test_contraction_success(self):
        bb = BeliefBase()
        bb.tell(self.default_contraction_kb)

        self.assertTrue(Contraction.success_postulate(bb=bb, sentence="p"))

    def test_contraction_inclusion(self):
        bb = BeliefBase()
        bb.tell(self.default_contraction_kb)

        self.assertTrue(Contraction.inclusion_postulate(bb=bb, sentence="p"))

    def test_contraction_vacuity(self):
        bb = BeliefBase()
        bb.tell(self.default_contraction_kb)

        self.assertTrue(Contraction.vacuity_postulate(bb=bb, sentence="r"))

    def test_contraction_extensionality(self):
        bb = BeliefBase()
        bb.tell(self.default_contraction_kb)

        self.assertTrue(Contraction.extensionality_postulate(bb=bb, sentences=["p", "~(~p)"]))

    def test_revision_success(self):
        bb = BeliefBase()
        bb.tell(self.default_revision_kb)

        self.assertTrue(Revision.success_postulate(bb=bb, sentence="~p"))

    def test_revision_inclusion(self):
        bb = BeliefBase()
        bb.tell(self.default_revision_kb)

        self.assertTrue(Revision.inclusion_postulate(bb=bb, sentence="~p"))

    def test_revision_vacuity(self):
        bb = BeliefBase()
        bb.tell(self.default_revision_kb)
        # revision with new literal
        self.assertTrue(Revision.vacuity_postulate(bb=bb, sentence="a"))

        bb = BeliefBase()
        bb.tell(self.default_revision_kb)
        # revision with existing literal
        self.assertTrue(Revision.vacuity_postulate(bb=bb, sentence="p"))

    def test_revision_extensionality(self):
        bb = BeliefBase()
        bb.tell(self.default_revision_kb)

        self.assertTrue(Revision.extensionality_postulate(bb=bb, sentences=["~p", "~p"]))


if __name__ == '__main__':
    unittest.main()
