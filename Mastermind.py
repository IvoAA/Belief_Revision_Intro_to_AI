from BeliefBase import BeliefBase
import boolean_translation
import itertools
import random
from utils import get_units_from_clauses


# implementing game logic for 4 pegs, 6 colors, 10 turns (if applicable) mastermind
# possible colors are red (r), orange (o), yellow (y), green (g), blue (b), indigo (i)

class Mastermind:
    # set board
    def __init__(self, board: str):
        self.colors = ['r', 'o', 'y', 'g', 'b', 'i']
        self.mastermind_board, self.belief_base = self.initialize_mastermind_game(board)

    # Initializes the mastermind game with a user-defined board
    # returns the board as a dictionary Keys:column number (str), Vals: color (str)
    # and a belief base of basic Mastermind logic
    def initialize_mastermind_game(self, board: str):
        if board == '':
            mastermind_board = {}
            for col in range(1, 5):
                mastermind_board[str(col)] = self.colors[random.randint(0, 5)]

            return mastermind_board, self.create_mastermind_logic()
        else:
            return self.sentence_to_mastermind_board(board), self.create_mastermind_logic()

    # converts a sentence to a mastermind board dictionary. Keys:column number (str), Vals: color (str)
    def sentence_to_mastermind_board(self, sentence: str):
        mastermind_board = {}
        sentence_list = sentence.split(' & ')
        for predicate in sentence_list:
            split_pred = predicate.split('_')
            mastermind_board[split_pred[1]] = split_pred[0]
        # print(mastermind_board)
        return mastermind_board

    # takes in a list of all possible colors in a single column and produces a string
    # in the form (o1 >> ~y1 & ~g1 & ~b1 & ~i1)
    # to denote only one color allowed per column
    def only_one_color(self, position):
        # create or clauses
        or_clauses = []
        for color in self.colors:
            colors = ['r', 'o', 'y', 'g', 'b', 'i']
            # create or of all other colors
            colors.remove(color)
            all_together = [col + '_' + position for col in colors]
            all_together = list(map(lambda y: '~' + y, all_together))
            or_string = "(" + (' & ').join(all_together) + ")"

            or_clauses.append(f"{color}_{position} >> {or_string}")
            # negate all predicates

        return ' & '.join(or_clauses)

    # inserts basic knowledge about the game into a belief base that is then returned when a new
    # Mastermind object is created. 
    # Logic follows solutions to week 10 exerises
    def create_mastermind_logic(self):
        game_rule_belief_base = BeliefBase()

        # all possible positions logic

        positions = ['1', '2', '3', '4']

        for position in positions:
            # there must be one color in each position
            all_colors_in_position = [color + '_' + position for color in self.colors]
            sentence = (' | ').join(all_colors_in_position)
            sentence = "(" + sentence + ")"

            game_rule_belief_base.tell(sentence)

            # there can only be one color in each position
            sentence = self.only_one_color(position)

            game_rule_belief_base.tell(sentence)

        # add shortcuts to negate colors (e.g. ~r means red is not in any of the 4 positions)
        for color in self.colors:
            game_rule_belief_base.tell(f"~{color} >> (~{color}_1 & ~{color}_2 & ~{color}_3 & ~{color}_4)")

        return game_rule_belief_base

    # compares two mastermind boards in the dictionary form
    # returns two lists, the first containing the guesses with correct color and position
    # the second with guesses with correct color and wrong position
    def compare_boards(self, main_board: dict, board_to_compare: dict):
        correct_color_and_position = 0
        correct_color_wrong_position = 0
        board_copy = board_to_compare.copy()
        main_board_copy = main_board.copy()

        # first run through and check exact matches, then remove them
        for position in ['1', '2', '3', '4']:
            if board_copy[position] == main_board_copy[position]:
                correct_color_and_position += 1
                del board_copy[position]
                del main_board_copy[position]

        # get all colors in main board and see whether color is present in check board
        # delete color from list to avoid duplicates

        colors_in_main_board = list(main_board_copy.values()).copy()
        colors_in_compare_board = list(board_copy.values()).copy()
        for color in colors_in_compare_board:
            if color in colors_in_main_board:
                correct_color_wrong_position += 1
                colors_in_main_board.remove(color)

        wrong_color_wrong_position = 4 - correct_color_and_position - correct_color_wrong_position  # hardcoded 4 positions

        return correct_color_and_position, correct_color_wrong_position, wrong_color_wrong_position, correct_color_and_position == 4

    # checks guesses against the mastermind board
    # guesses should be given in sentences such as 'r_1 & b_2 & o_3 & i_4' order is unimportant, for example
    # r_1 & b_2 & i_4 & o_3' is also valid
    # returns two lists, the first containing the guesses with correct color and position
    # the second with guesses with correct color and wrong position
    def check_guess(self, sentence: str):
        # convert the sentence into a dictionary representation of the board
        sentence_board = self.sentence_to_mastermind_board(sentence)
        correct_color_and_position, correct_color_wrong_position, wrong_color_wrong_position, game_over = self.compare_boards(
            self.mastermind_board, sentence_board)
        # game is over if all four positions have been correctly guessed
        return correct_color_and_position, correct_color_wrong_position, wrong_color_wrong_position, game_over

    def __str__(self):
        str_build = '| '
        for col in self.mastermind_board.keys():
            str_build = str_build + self.mastermind_board[col] + "_" + col + " | "
        return str_build


class Mastermind_AI:

    def __init__(self, board: str):
        self.mastermind = Mastermind(board)
        self.belief_base = self.mastermind.belief_base
        self.colors = self.mastermind.colors
        self.game_over = False
        self.correct_color_and_position = 0
        self.correct_color_wrong_position = 0
        self.wrong_color_wrong_position = 0
        self.guess = []
        self.guessed = []
        self.n_rounds = 10  # hardcoded maximum 10 rounds
        self.boolean_translation_guess = ''
        self.best_first_guess_flag = True
        self.all_guesses = self.create_all_possible_guesses()
        self.truths = []
        self.falsities = []

    # taken from wikipedia Knuth five-guess algorithm as being best first guess
    def best_first_guess(self):
        guess = "r_1 & r_2 & o_3 & o_4"
        guess_l = guess.split(' & ')
        print('The guessed value is: ' + guess)
        self.correct_color_and_position, self.correct_color_wrong_position, self.wrong_color_wrong_position, self.game_over = self.mastermind.check_guess(
            guess)
        print('number correct: ' + str(self.correct_color_and_position))
        print('colors correct: ' + str(self.correct_color_wrong_position))
        print('totally wrong: ' + str(self.wrong_color_wrong_position))
        self.guess = guess
        self.guessed.append(guess)
        self.boolean_translation_guess = boolean_translation.boolean_translation(guess_l,
                                                                                 self.correct_color_and_position,
                                                                                 self.correct_color_wrong_position)
        print('boolean translation:')
        print(self.boolean_translation_guess)
        print("unit clauses before telling:")
        print(self.belief_base.obtain_units())
        self.belief_base.revision(self.boolean_translation_guess)
        print("unit clauses after telling:")
        print(self.belief_base.obtain_units())
        unit_clauses = self.belief_base.obtain_units()
        self.truths.extend([x for x in unit_clauses if '~' not in x])
        self.falsities.extend([x for x in unit_clauses if '~' in x])
        self.falsities = list(map(lambda y: y[1:], self.falsities))

    def random_first_guess(self):
        guess = ' & '.join([self.colors[random.randint(0, 4)] + '_' + str(x) for x in range(1, 5)])
        guess_l = guess.split(' & ')
        print('The guessed value is: ' + guess)
        self.correct_color_and_position, self.correct_color_wrong_position, self.wrong_color_wrong_position, self.game_over = self.mastermind.check_guess(
            guess)
        print('number correct: ' + str(self.correct_color_and_position))
        print('colors correct: ' + str(self.correct_color_wrong_position))
        print('totally wrong: ' + str(self.wrong_color_wrong_position))
        self.guess = guess
        self.guessed.append(guess)
        self.boolean_translation_guess = boolean_translation.boolean_translation(guess_l,
                                                                                 self.correct_color_and_position,
                                                                                 self.correct_color_wrong_position)
        print('boolean translation:')
        print(self.boolean_translation_guess)
        print("unit clauses before telling:")
        print(self.belief_base.obtain_units())
        self.belief_base.tell(self.boolean_translation_guess)
        print("unit clauses after telling:")
        print(self.belief_base.obtain_units())
        unit_clauses = self.belief_base.obtain_units()
        self.truths.extend([x for x in unit_clauses if '~' not in x])
        self.falsities.extend([x for x in unit_clauses if '~' in x])
        self.falsities = list(map(lambda y: y[1:], self.falsities))

    def manual_guess(self):
        guess = "b_1 & g_2 & i_3 & o_4"
        guess_l = guess.split(' & ')
        print('The guessed value is: ' + guess)
        self.correct_color_and_position, self.correct_color_wrong_position, self.wrong_color_wrong_position, self.game_over = self.mastermind.check_guess(
            guess)
        print('number correct: ' + str(self.correct_color_and_position))
        print('colors correct: ' + str(self.correct_color_wrong_position))
        print('totally wrong: ' + str(self.wrong_color_wrong_position))
        self.guess = guess
        self.guessed.append(guess)
        self.boolean_translation_guess = boolean_translation.boolean_translation(guess_l,
                                                                                 self.correct_color_and_position,
                                                                                 self.correct_color_wrong_position)
        print('boolean translation:')
        print(self.boolean_translation_guess)
        print("unit clauses before telling:")
        print(self.belief_base.obtain_units())
        self.belief_base.tell(self.boolean_translation_guess)
        print("unit clauses after telling:")
        print(self.belief_base.obtain_units())
        unit_clauses = self.belief_base.obtain_units()
        self.truths.extend([x for x in unit_clauses if '~' not in x])
        self.falsities.extend([x for x in unit_clauses if '~' in x])
        self.falsities = list(map(lambda y: y[1:], self.falsities))

    def informed_guess(self):
        positions = {}

        positions['1'] = [x + '_1' for x in self.colors]
        positions['2'] = [x + '_2' for x in self.colors]
        positions['3'] = [x + '_3' for x in self.colors]
        positions['4'] = [x + '_4' for x in self.colors]

        truth = {}
        truth['1'] = [x for x in self.truths if x[-1] == '1']
        truth['2'] = [x for x in self.truths if x[-1] == '2']
        truth['3'] = [x for x in self.truths if x[-1] == '3']
        truth['4'] = [x for x in self.truths if x[-1] == '4']

        falsity = {}
        falsity['1'] = [x for x in self.falsities if len(x) == 1 or x[-1] == '1']
        falsity['2'] = [x for x in self.falsities if len(x) == 1 or x[-1] == '2']
        falsity['3'] = [x for x in self.falsities if len(x) == 1 or x[-1] == '3']
        falsity['4'] = [x for x in self.falsities if len(x) == 1 or x[-1] == '1']

        guess = self.guess
        while guess in self.guessed:
            guess_a = []
            missing_positions = ['1', '2', '3', '4']

            for t in truth:
                guess_a.append(t)
                missing_positions.remove(t[-1])

            while missing_positions:
                pos = missing_positions[0]

                possible_guesses = [x for x in positions[pos] if x not in falsity[pos]]
                x = random.choice(possible_guesses)

                new_guess = f"{x}_{pos}"
                if self.belief_base.check_entailment(' & '.join(guess_a) + ' & ' + new_guess):
                    guess_a.append(new_guess)
                    missing_positions.remove(pos)

            guess = ' & '.join(guess_a)


        print('making an informed guess')

        print('The guessed value is: ' + guess)
        self.correct_color_and_position, self.correct_color_wrong_position, self.wrong_color_wrong_position, self.game_over = self.mastermind.check_guess(
            guess)
        print('number correct: ' + str(self.correct_color_and_position))
        print('colors correct: ' + str(self.correct_color_wrong_position))
        print('totally wrong: ' + str(self.wrong_color_wrong_position))
        self.guess = guess
        self.guessed.append(guess)
        self.boolean_translation_guess = boolean_translation.boolean_translation(guess_a,
                                                                                 self.correct_color_and_position,
                                                                                 self.correct_color_wrong_position)
        print('boolean translation: ')
        print(self.boolean_translation_guess)
        print("unit clauses before telling:")
        print(self.belief_base.obtain_units())

        self.belief_base.tell(self.boolean_translation_guess)
        print("unit clauses after telling:")
        print(self.belief_base.obtain_units())
        unit_clauses = self.belief_base.obtain_units()
        self.truths.extend([x for x in unit_clauses if '~' not in x])
        self.falsities.extend([x for x in unit_clauses if '~' in x])
        self.falsities = list(map(lambda y: y[1:], self.falsities))

    def brute_force_guess(self):
        print('brute forcing guess')
        self.belief_base.revision(self.boolean_translation_guess)
        for guess in self.all_guesses:
            if guess not in self.guessed:
                if self.belief_base.check_entailment(guess):
                    print('The guessed value is: ' + guess)
                    guess_l = guess.split(' & ')

                    self.correct_color_and_position, self.correct_color_wrong_position, self.wrong_color_wrong_position = self.mastermind.check_guess(
                        guess)
                    print('number correct: ' + str(self.correct_color_and_position))
                    print('colors correct: ' + str(self.correct_color_wrong_position))
                    print('totally wrong: ' + str(self.wrong_color_wrong_position))
                    self.guess = guess
                    self.guessed.append(guess)
                    self.boolean_translation_guess = boolean_translation.boolean_translation(guess_l,
                                                                                             self.correct_color_and_position,
                                                                                             self.correct_color_wrong_position)
                    self.belief_base.tell(self.boolean_translation_guess)

    def create_all_possible_guesses(self):
        all_guesses = []
        position_1 = [x + '_1' for x in self.colors]
        position_2 = [x + '_2' for x in self.colors]
        position_3 = [x + '_3' for x in self.colors]
        position_4 = [x + '_4' for x in self.colors]

        product = itertools.product(position_1, position_2, position_3, position_4)

        for guess in product:
            all_guesses.append((' & ').join(guess))

        return all_guesses

    def play(self):
        print('Welcome to Mastermind')
        print('The board is: ' + str(self.mastermind) + ' But the computer doesn\'t know this')

        if self.best_first_guess_flag:
            self.best_first_guess()
            # self.manual_guess()
        else:
            self.random_first_guess()

        turn = self.n_rounds - 1
        while not (self.game_over) and turn > 0:
            print('new turn, hit enter')
            input()
            self.informed_guess()
        if self.game_over:
            print('the computer successfully guessed the board')
        else:
            print('the computer could not figure out the board')
