from BeliefBase import BeliefBase
from Mastermind import Mastermind_AI


def print_actions():
    print('\n\nPlease input the intended action:')
    print('\tA: Add a sentence to knowledge base')
    print('\tC: Contract a sentence to knowledge base')
    print('\tE: Check if sentence can be deduced from knowledge base')
    print('\tB: Batch, read a file with several actions')
    print('\tKB: show current knowledge base')
    print('\tM: Play Mastermind')
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
    print('\t\tC: Contract sentence from knowledge base')
    print('\t\tE: Check if sentence can be deduced from knowledge base')
    print('\t- Action is followed by a space and then the logic sentence')
    print('Please input the filename:')
    filename = input()

    with open(f"Batch/{filename}.txt") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        sentence = line[1:].rstrip()

        if line.startswith('A'):
            belief_base.tell(sentence)
        elif line.startswith('E'):
            belief_base.check_entailment(sentence)
        elif line.startswith('C'):
            belief_base.contraction(sentence)
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
        elif action == 'M':
            print('do you want to create your own board [y] or have one auto-generated? [n]')
            action = input()
            while action not in ['y','n']:
                print('please choose y/n')
                action = input().upper()
            if action == 'y':
                print('please input your board as a stirng of the form (r_1 & o_2 & y_3 & g_4)')
                print('possible colors are [r,o,y,g,b,i] \n')
                action = input()
                mastermind = Mastermind_AI(action)
                mastermind.play()
            elif action == 'n':
                mastermind = Mastermind_AI('')
                mastermind.play()
        elif action not in ['A', 'E', 'C','M']:
            print('Please input one of the possible options.')
            continue

        print('Please input sentence:')
        sentence = input().strip()

        if action == 'A':
            belief_base.tell(sentence)
        elif action == 'E':
            print(belief_base.check_entailment(sentence))
        elif action == 'C':
            belief_base.contraction(sentence)

    # add to knowledge base
    return belief_base.get_knowledge_base()


if __name__ == '__main__':
    init()
