import copy

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
    def extensionality_postulate(bb: BeliefBase, sentences: List[str]) -> bool:
        bb_1 = copy.deepcopy(bb)
        bb_2 = copy.deepcopy(bb)

        bb_1.contraction(sentence=sentences[0])
        bb_2.contraction(sentence=sentences[1])

        size_check = len(bb_1.get_knowledge_base()) == len(bb_2.get_knowledge_base())

        all_elements_check = all(list(map(lambda x: x in bb_1.get_knowledge_base(), bb_2.get_knowledge_base())))

        return size_check and all_elements_check

    @staticmethod
    def consistency_postulate(bb: BeliefBase, sentence: str) -> bool:
        # Consistency is not existent for contraction
        return True


class Revision:
    @staticmethod
    def success_postulate(bb: BeliefBase, sentence: str) -> bool:
        bb.revision(sentence=sentence)

        return sentence in bb.get_knowledge_base()

    @staticmethod
    def inclusion_postulate(bb: BeliefBase, sentence: str) -> bool:
        kb_only_expansion = bb.get_knowledge_base() + [sentence]
        bb.revision(sentence=sentence)
        kb_revision = bb.get_knowledge_base()

        size_check = len(kb_only_expansion) >= len(kb_revision)

        all_elements_check = all(list(map(lambda x: x in kb_only_expansion, kb_revision)))

        return size_check and all_elements_check

    @staticmethod
    def vacuity_postulate(bb: BeliefBase, sentence: str) -> bool:
        negated_sentence = sympy.to_cnf(f"~({sentence})")

        if str(negated_sentence) in bb.get_knowledge_base():
            # if negated sentence is in the knowledge base, this postulate is true
            return True

        kb_only_expansion = bb.get_knowledge_base()
        if sentence not in kb_only_expansion:
            kb_only_expansion += [sentence]
        bb.revision(sentence)

        kb_revision = bb.get_knowledge_base()

        all_elements_check = all(list(map(lambda x: x in kb_only_expansion, kb_revision)))

        size_check = len(kb_revision) == len(kb_only_expansion)

        return all_elements_check and size_check

    @staticmethod
    def extensionality_postulate(bb: BeliefBase, sentences: List[str]) -> bool:
        bb_1 = copy.deepcopy(bb)
        bb_2 = copy.deepcopy(bb)

        bb_1.revision(sentence=sentences[0])
        bb_2.revision(sentence=sentences[1])

        size_check = len(bb_1.get_knowledge_base()) == len(bb_2.get_knowledge_base())

        all_elements_check = all(list(map(lambda x: x in bb_1.get_knowledge_base(), bb_2.get_knowledge_base())))

        return size_check and all_elements_check


