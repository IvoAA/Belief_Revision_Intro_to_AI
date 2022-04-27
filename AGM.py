from BeliefBase import BeliefBase
from typing import List
import sympy

class Contraction:

    @staticmethod
    def success_postulate(bb: BeliefBase, sentence: str) -> bool:
        if bb.check_entailment(sentence=sentence, kb=[]):
            # sentence is implied by empty knowledge base, therefore this postulate is true.
            return True
        bb.contraction(sentence)
        return not bb.check_entailment(sentence)

    @staticmethod
    def inclusion_postulate(bb: BeliefBase, sentence: str) -> bool:
        kb_before = bb.get_knowledge_base()
        bb.contraction(sentence)
        kb_after = bb.get_knowledge_base()

        subset_length_check = len(kb_before) >= len(kb_after)

        elements_check = all(list(map(lambda x: x in kb_before, kb_after)))

        return subset_length_check and elements_check

    @staticmethod
    def vacuity_postulate(bb: BeliefBase, sentence: str) -> bool:
        if bb.check_entailment(sentence=sentence):
            # sentence is already implied by knowledge base, therefore this postulate is true.
            return True
        kb_before = bb.get_knowledge_base()
        bb.contraction(sentence)
        kb_after = bb.get_knowledge_base()

        kb_length_check = len(kb_before) == len(kb_after)

        elements_check = all(list(map(lambda x: x in kb_before, kb_after)))

        return kb_length_check and elements_check

    @staticmethod
    def extensionality_postulate(bb: BeliefBase, literals: List[str]) -> bool:
        # TODO: look into this again
        sentence = ""
        bb.check_entailment(sentence=sentence, kb=[])
        print()
        return False

    @staticmethod
    def consistency_postulate(bb: BeliefBase, sentence: str) -> bool:
        # TODO: not sure if this exist for contractio
        return True





