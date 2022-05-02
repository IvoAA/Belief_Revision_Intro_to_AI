import copy
from typing import List
from itertools import combinations
from clause import Clause

from utils import DPLL, sentence_to_clauses,get_units_from_clauses, get_units_from_clauses_mastermind



class BeliefBase:
    def __init__(self):
        self.knowledge_base: List[Clause] = []
        self.nr_clause = 0

    def tell(self, sentence: str):
        clauses = sentence_to_clauses(sentence)

        # TODO check if any clause contradicts belief base before adding
        for clause in clauses:
            self.expansion(clause)

    def expansion(self, clause: str):
        if clause not in self.strip_kb(self.knowledge_base):
            self.knowledge_base.append(Clause(clause, self.clause_priority()))

    def clause_priority(self):
        priority = self.nr_clause
        self.nr_clause += 1
        return priority

    def revision(self, sentence: str):
        negated_sentence = f"~({sentence})"
        self.contraction(negated_sentence)
        self.expansion(sentence)

    def _contradiction_by_clauses(self, kb: List[Clause], nr_clauses: int, clause) -> List:
        all_combinations = combinations(kb, nr_clauses)
        contradicting_comb = []
        for combination in all_combinations:
            kb_stub = copy.deepcopy(self.knowledge_base)
            for cl in combination:
                kb_stub.remove(cl)
            if not self.check_entailment(clause, kb_stub):
                contradicting_comb.append(combination)
        return contradicting_comb

    @staticmethod
    def _combination_lowest_priority(combs: List) -> str:
        candidate = combs[0]
        for com in combs:
            if sum(c.priority for c in com) > sum(c.priority for c in candidate):
                candidate = com
        return candidate

    def _clause_contraction(self, c: str):
        contradicting_comb = None
        if self.check_entailment(c):
            for index in range(len(self.knowledge_base)):
                contradicting_comb = self._contradiction_by_clauses(self.knowledge_base, index + 1, c)
                if len(contradicting_comb) > 0:
                    break
            if contradicting_comb is None:
                raise "contradiction found in contraction, but no clause found which creates the contradiction"
            remove_clauses = self._combination_lowest_priority(contradicting_comb)
            for clause in remove_clauses:
                self.knowledge_base.remove(clause)

        if c in self.knowledge_base:
            self.knowledge_base.remove(c)

    def contraction(self, sentence: str):
        clauses = sentence_to_clauses(sentence)
        for clause in clauses:
            if clause != 'True':  # ensure we're not contracting a Tautology
                self._clause_contraction(clause)

    def check_entailment(self, sentence: str, kb: List[Clause] = None) -> bool:
        # negate sentence
        clauses = sentence_to_clauses(f"~({sentence})")

        if kb is None:
            new_kb = clauses + self.get_knowledge_base()
        else:
            new_kb = clauses + self.strip_kb(kb)
        return not DPLL(new_kb)

    def get_knowledge_base(self):
        return self.strip_kb(self.knowledge_base)

    @staticmethod
    def strip_kb(kb: List[Clause]) -> List[str]:
        order_kb = kb.copy()
        order_kb.sort(key=lambda x: x.priority)
        return list(map(lambda x: x.value, order_kb))


    def obtain_units(self):
        units = get_units_from_clauses_mastermind(self.knowledge_base)
        return units


    def obtain_truth(self):
        truths = []
        units = get_units_from_clauses(self.knowledge_base)
        for unit in units:
            if unit not in truths and self.check_entailment(unit):
                truths.append(unit)
        return truths

        
    #def obtain_truth_falsity(self):
    #   truths = []
    #    falsities = []
    #    units = get_units_from_clauses(self.__knowledge_base)
    #    for unit in units:
    #        if self.check_entailment(unit):
    #            truths.append(unit)
    #        if self.check_entailment('~'+unit):
    #            falsities.append(unit)
    #    return truths, falsities



