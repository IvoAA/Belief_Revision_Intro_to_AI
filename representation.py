from typing import List
import re
from abc import ABC, abstractmethod


class Variable:
    def __init__(self, name: str, negated: bool):
        self.name = name.replace(" ", "_")
        self.negated = negated

    def __str__(self):
        return ("~" if self.negated else "") + self.name

    @staticmethod
    def from_str(content: str):
        if content.count("|") > 0 or content.count("&") > 0:
            raise Exception(f"Can't decode variable from string! '{content}'")
        negated = content.count("~") > 0

        return Variable(name=content.replace("~", ""), negated=negated)

    def perform_negation(self):
        self.negated = not self.negated
        return self


class Collection(ABC):

    def __init__(self, variables: List = None, negated: bool = False):
        if not variables:
            self.variables = []
        else:
            self.variables = variables
        self.operator = 'X'
        self.negated = negated
        self.name = ""

    def __str__(self):
        return ("~" if self.negated else "") + "(" + f" {self.operator} ".join(list(map(str, self.variables))) + ")"

    def perform_negation(self):
        if self.negated:
            return self
        new_variables = []

        for variable in self.variables:
            if isinstance(variable, Variable):
                new_variables.append(variable.perform_negation())
            else:
                new_variables.append(variable.resolve_negation())

        if self.operator == "&":
            return OrCollection(variables=new_variables, negated=not self.negated)
        else:
            return AndCollection(variables=new_variables, negated=not self.negated)

    def resolve_negation(self):
        if not self.negated:
            return self

        new_variables = []
        for variable in self.variables:
            new_variables.append(variable.perform_negation())

        if self.operator == "&":
            return OrCollection(variables=new_variables, negated=not self.negated)
        else:
            return AndCollection(variables=new_variables, negated=not self.negated)


    @staticmethod
    def _convert_to_collection(content: str):
        negated = content.startswith("~")
        content = content.replace("(", "").replace(")", "").replace("~", "", 1 if negated else 0)
        or_operator = content.count("|")
        and_operator = content.count("&")

        if or_operator > 0 and and_operator > 0:
            raise Exception(f"Use parenthesis! '{content}'")
        if or_operator + and_operator == 0:
            raise Exception(f"No expression! '{content}'")
        used_operator = "|" if or_operator > 0 else "&"

        values = list(map(str.strip, content.split(used_operator)))


        if or_operator > 0:
            return OrCollection(variables=list(map(Variable.from_str, values)), negated=negated)
        else:
            return AndCollection(variables=list(map(Variable.from_str, values)), negated=negated)

    @staticmethod
    def from_str(content: str):
        regex_patter = r"(\~?\([^\(]*?\))"
        matches = re.findall(regex_patter, content)
        open_parenthesis = content.count("(")
        counter = 0
        generated_collections = {}
        if len(matches) <= 1 and open_parenthesis <= 1:
            return Collection._convert_to_collection(content)
        else:
            while len(matches) >= 1:
                match = matches[0]
                content = content.replace(match, f"tmp_{counter}")
                generated_collections[f"tmp_{counter}"] = Collection._convert_to_collection(match)
                matches = re.findall(regex_patter, content)
                counter += 1

            for key in reversed(generated_collections.keys()):
                value: Collection = generated_collections.get(key)
                key_intersection = set(list(map(str, value.variables))).intersection(set(generated_collections.keys()))
                for key_of_collection_to_insert in list(key_intersection):
                    index_to_remove = list(map(lambda x: x.name, value.variables)).index(key_of_collection_to_insert)
                    value.variables.pop(index_to_remove)
                    value.variables.insert(index_to_remove, generated_collections.get(key_of_collection_to_insert))
                    print()
            return list(generated_collections.values())[-1]


class OrCollection(Collection):
    def __init__(self, variables: List = None, negated: bool = False):
        super().__init__(variables, negated)
        self.operator = "|"



class AndCollection(Collection):
    def __init__(self, variables: List = None, negated: bool = False):
        super().__init__(variables, negated)
        self.operator = "&"


if __name__ == '__main__':
    a_1 = Variable.from_str("A")
    b_1 = Variable.from_str("~B asdf")

    print(Collection.from_str("(a | (a & b &~c))"))


