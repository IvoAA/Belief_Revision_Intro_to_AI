import math
import copy
from typing import List

from sympy import to_cnf
from itertools import combinations
from clause import Clause

from utils import DPLL, get_unit_clauses, simplify, sentence_to_clauses


class BeliefBase:
    def __init__(self):
        self.__knowledge_base = []
        self.nr_clause = 0

    def tell(self, sentence):
        clauses = sentence_to_clauses(sentence)

        # TODO check if any clause contradicts belief base before adding
        for clause in clauses:
            self.expansion(clause)

    def expansion(self, clause):
        if clause not in self.__knowledge_base:
            self.__knowledge_base.append(Clause(clause, self.clause_priority()))

    def clause_priority(self):
        priority = self.nr_clause
        self.nr_clause += 1
        return priority

    def revision(self, sentence):
        pass

    def _contradiction_by_clauses(self, kb: List[Clause], nr_clauses: int, clause) -> List:
        all_combinations = combinations(kb, nr_clauses)
        contradicting_comb = []
        for combination in all_combinations:
            kb_stub = copy.deepcopy(self.__knowledge_base)
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
            for index in range(len(self.__knowledge_base)):
                contradicting_comb = self._contradiction_by_clauses(self.__knowledge_base, index + 1, c)
                if len(contradicting_comb) > 0:
                    break
            if contradicting_comb is None:
                raise "contradiction found in contraction, but no clause found which creates the contradiction"
            remove_clauses = self._combination_lowest_priority(contradicting_comb)
            for clause in remove_clauses:
                self.__knowledge_base.remove(clause)

        if c in self.__knowledge_base:
            self.__knowledge_base.remove(c)

    def contraction(self, sentence: str):
        clauses = sentence_to_clauses(sentence)
        for clause in clauses:
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
        return self.strip_kb(self.__knowledge_base)

    @staticmethod
    def strip_kb(kb: List[Clause]) -> List[str]:
        order_kb = kb.copy()
        order_kb.sort(key=lambda x: x.priority)
        return list(map(lambda x: x.value, order_kb))

