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

    def check_entailment(self, sentence):
        entails = True

        clauses = self.sentence_to_clauses(sentence)
        for clause in clauses:
            # TODO derive sentence, instead of checking if it's litterally there
            if clause not in self.knowledge_base:
                return False

        return entails

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
