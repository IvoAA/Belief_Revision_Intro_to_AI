from Belief_Revision_Intro_to_AI.BeliefBase import BeliefBase


def print_actions():
    print('\n\nPlease input the intended action:')
    print('\tA: Add sentence to knowledge base')
    print('\tE: Check if sentence can be deduced from knowledge base')
    print('\tB: Batch, read a file with several actions')
    print('\tKB: show current knowledge base')
    print('\tH: Help')
    print('\tQ: Quit')

def show_knowledge_base(belief_base):
    print('Knowledge Base:')
    for clause in belief_base.get_knowledge_base():
        print(f"\t{clause}")

    print('--------------')


def print_help():
    print('Symbols:')
    print('\tNegation:\t\t~')
    print('\tConjuntion:\t\t&')
    print('\tDisjuntion:\t\t|')
    print('\tImplication:\t>>')


def batch_actions(belief_base):
    print('Please ensure the file is in the current folder.')
    print('Please ensure the file has the correct format:')
    print("\t- Line starts with the intended action:")
    print('\t\tA: Add sentence to knowledge base')
    print('\t\tE: Check if sentence can be deduced from knowledge base')
    print('\t- Action is followed by a space and then the logic sentence')
    print('Please input the filename:')
    filename = input()

    with open(f"Batch/{filename}.txt") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith('A'):
            belief_base.tell(line[1:].rstrip())
        elif line.startswith('E'):
            belief_base.check_entailment(line[1:].rstrip())
        else:
            print(f"Error in line {i+1}:")
            print(line)


def init():
    belief_base = BeliefBase()

    while True:
        print_actions()

        action = input().upper()
        if action == 'Q':
            break
        elif action == 'KB':
            show_knowledge_base(belief_base)
            continue
        elif action == 'H':
            print_help()
            continue
        elif action == 'B':
            batch_actions(belief_base)
            continue
        elif action not in ['A', 'E']:
            print('Please input one of the possible options.')
            continue

        print('Please input sentence:')
        sentence = input().strip()

        if action == 'A':
            belief_base.tell(sentence)
        elif action == 'E':
            print(belief_base.check_entailment(sentence))

    # add to knowledge base
    return belief_base.get_knowledge_base()


if __name__ == '__main__':
    init()
