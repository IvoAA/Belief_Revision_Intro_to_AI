import math
from sympy import to_cnf
from typing import List, Union
from clause import Clause


def DPLL(kb: List):
    unit_clauses = get_unit_clauses(kb)
    while unit_clauses:
        for clause in unit_clauses:
            kb = simplify(kb, clause)

            if kb == False:  # contradiction was found
                return False
            elif len(kb) == 0:  # all terms were removed
                return True

        unit_clauses = get_unit_clauses(kb)

    shortest_clause = ""
    shortest_clause_terms = math.inf

    for clause in kb:
        terms = clause.count('|')
        if terms < shortest_clause_terms:
            shortest_clause = clause
            shortest_clause_terms = terms

    term = shortest_clause.split(' |')[0]

    if DPLL([term] + kb):
        return True
    else:
        neg_term = str(to_cnf(f"~({term})",force=True))
        return DPLL([neg_term] + kb)


def get_unit_clauses(kb: List) -> List:
    unit_clauses = []
    for clause in kb:
        # if unit clause
        if '|' not in clause:
            unit_clauses.append(clause)

    return unit_clauses


def simplify(kb: List, unit: str) -> Union[List, bool]: # TODO: Why return bool here?
    neg_unit = str(to_cnf(f"~({unit})",force = True))
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


def sentence_to_clauses(sentence: str) -> List[str]:
    try:
        cnf = to_cnf(sentence, force=True)
        clauses = str(cnf).split('&')

    except SyntaxError:
        raise Exception('Formula provided has wrong format.')

    for i, clause in enumerate(clauses):
        clauses[i] = clause.replace('(', '').replace(')', '').strip()
    #TODO: Replace with map function
    return clauses
