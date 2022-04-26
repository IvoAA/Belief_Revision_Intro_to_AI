import math

import copy

from sympy import to_cnf
from itertools import combinations


from clause import Clause


class BeliefBase:
    def __init__(self):
        self.__knowledge_base = []
        self.nr_clause = 0

    def tell(self, sentence):
        clauses = self.sentence_to_clauses(sentence)

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

    def _contradiction_by_clauses(self, kb, nr_clauses, clause):
        comb = combinations(kb, nr_clauses)
        contradicting_comb = []
        for c in comb:
            kb_stub = copy.deepcopy(self.__knowledge_base)
            for cl in c:
                kb_stub.remove(cl)
            if not self.check_entailment(clause, kb_stub):
                contradicting_comb.append(c)
        return contradicting_comb

    def _combination_lowest_priority(self, combs):
        candidate = combs[0]
        for com in combs:
            if sum(c.priority for c in com) > sum(c.priority for c in candidate):
                candidate = com
        return candidate

    def _clause_contraction(self, c):
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

    def contraction(self, sentence):
        clauses = self.sentence_to_clauses(sentence)
        for clause in clauses:
            self._clause_contraction(clause)

    @staticmethod
    def get_unit_clauses(kb):
        unit_clauses = []
        for clause in kb:
            # if unit clause
            if '|' not in clause:
                unit_clauses.append(clause)

        return unit_clauses

    @staticmethod
    def simplify(kb, unit):
        neg_unit = str(to_cnf(f"~({unit})"))
        space_unit = f" {unit}"

        new_kb = []
        for clause in kb:
            # if we look for the unit 'p' in the sentence 'r | ~p' it is found
            # therefore we will look for the string ' p', to ensure it has no negation
            if clause == unit or space_unit in clause:
                continue

            if neg_unit in clause:
                if '|' not in clause:  # unit clause of neg_unit implies a contradiction in kb
                    return False

                # remove the negated unit from clauses
                if f"{neg_unit} | " in clause:
                    new_kb.append(clause.replace(f"{neg_unit} | ", ""))
                else:
                    new_kb.append(clause.replace(f" | {neg_unit}", ""))

            else:
                new_kb.append(clause)
        return new_kb

    def DPLL(self, kb):
        unit_clauses = self.get_unit_clauses(kb)
        while unit_clauses:
            for clause in unit_clauses:
                kb = self.simplify(kb, clause)

                if kb == False:  # contradiction was found
                    return False
                elif len(kb) == 0:  # all terms were removed
                    return True

            unit_clauses = self.get_unit_clauses(kb)

        shortest_clause = ""
        shortest_clause_terms = math.inf

        for clause in kb:
            terms = clause.count('|')
            if terms < shortest_clause_terms:
                shortest_clause = clause
                shortest_clause_terms = terms

        term = shortest_clause.split(' |')[0]

        if self.DPLL([term] + kb):
            return True
        else:
            neg_term = str(to_cnf(f"~({term})"))
            return self.DPLL([neg_term] + kb)

    def check_entailment(self, sentence, kb=None):
        # negate sentence
        clauses = self.sentence_to_clauses(f"~({sentence})")

        if kb is None:
            new_kb = clauses + self.get_knowledge_base()
        else:
            new_kb = clauses + self.strip_kb(kb)
        return not self.DPLL(new_kb)

    def get_knowledge_base(self):
        return self.strip_kb(self.__knowledge_base)

    @staticmethod
    def strip_kb(kb):
        order_kb = kb
        order_kb.sort(key=lambda x: x.priority)
        output = []
        for k in order_kb:
            output.append(k.value)
        return output

    @staticmethod
    def sentence_to_clauses(sentence):
        try:
            cnf = to_cnf(sentence)
            clauses = str(cnf).split('&')

        except SyntaxError:
            raise Exception('Formula provided has wrong format.')

        for i, clause in enumerate(clauses):
            clauses[i] = clause.replace('(', '').replace(')', '').strip()

        return clauses
