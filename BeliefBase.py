import math

from sympy import to_cnf


class BeliefBase:
    def __init__(self):
        self.knowledge_base = []

    def tell(self, sentence):
        clauses = self.sentence_to_clauses(sentence)

        # TODO check if any clause contradicts belief base before adding
        for clause in clauses:
            self.addition(clause)

    def addition(self, clause):
        if clause not in self.knowledge_base:
            self.knowledge_base.append(clause)

    def revision(self, sentence):
        pass

    def contraction(self, sentence):
        pass

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

    def check_entailment(self, sentence):
        # negate sentence
        clauses = self.sentence_to_clauses(f"~({sentence})")

        new_kb = clauses + self.knowledge_base
        return not self.DPLL(new_kb)

    def get_knowledge_base(self):
        return self.knowledge_base

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
