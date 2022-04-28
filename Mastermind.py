from BeliefBase import BeliefBase
import random

from main import init
#implementing game logic for 4 pegs, 6 colors, 10 turns (if applicable) mastermind
#possible colors are red (r), orange (o), yellow (y), green (g), blue (b), indigo (i)

class Mastermind:

    def __init__(self):
        self.mastermind_board, self.belief_base = self.initialize_mastermind_game()
        self.colors = ['r','o','y','g','b','i']

    #set board
    def __init__(self, board :str):
        self.mastermind_board, self.belief_base = self.initialize_mastermind_game(board)
        self.colors = ['r','o','y','g','b','i']

    #Initializes the mastermind game by creating a random board
    #returns the board as a dictionary Keys:column number (str), Vals: color (str)
    # and a belief base of basic Mastermind logic
    def initialize_mastermind_game(self):
        mastermind_board = {}
        for col in range(1,5):
            mastermind_board[str(col)] = self.colors[random.randint(0,5)]

        return mastermind_board, self.create_mastermind_logic()

    #Initializes the mastermind game with a user-defined board
    #returns the board as a dictionary Keys:column number (str), Vals: color (str)
    # and a belief base of basic Mastermind logic
    def initialize_mastermind_game(self, board: str):
        return self.sentence_to_mastermind_board(board), self.create_mastermind_logic()
    
    #converts a sentence to a mastermind board dictionary. Keys:column number (str), Vals: color (str)
    def sentence_to_mastermind_board(sentence:str):
        mastermind_board = {}
        sentence_list = sentence.split(' & ')
        for predicate in sentence_list:
            split_pred = predicate.split('_')
            mastermind_board[split_pred[1]] = split_pred[0]
        return mastermind_board

    #takes in a list of all possible colors in a single column and produces a string
    # in the form (¬t1 ∨ ¬s1) ∧ (¬s1 ∨ ¬d1) ∧ (¬d1 ∨ ¬t1) 
    # to denote only one color allowed per column
    def only_one_color(column):
        #create or clauses
        or_clauses = []
        for color in column:
            #create or of all other colors
            other_colors = column.copy().pop(color)
            #negate all predicates
            negated_predicates = ['~'+pred for pred in other_colors]
            or_clauses.append('('+' | '.join(negated_predicates)+')')
        
        return ' & '.join(or_clauses)

    #inserts basic knowledge about the game into a belief base that is then returned when a new
    # Mastermind object is created. 
    # Logic follows solutions to week 10 exerises
    def create_mastermind_logic(self):
        game_rule_belief_base = BeliefBase()

        #all possible positions logic

        positions = {}
        for pos in range(1,5): #number of positions is hardcoded
            positions[pos] = [str(color)+"_"+str(pos) for color in self.colors]
        
        for column in positions.values():
            #there must be one color in a given position
            sentence = '('+' | '.join(column)+')'
            game_rule_belief_base.tell(sentence)

            #there can only be one color in a given position
            game_rule_belief_base.tell(self.only_one_color(column))

        return game_rule_belief_base
    

    #compares two mastermind boards in the dictionary form
    #returns two lists, the first containing the guesses with correct color and position
    # the second with guesses with correct color and wrong position
    def compare_boards(main_board : dict,board_to_compare :dict):
        correct_color_and_position = 0
        correct_color_wrong_position = 0
        board_copy = board_to_compare.copy()

        #first run through and check exact matches, then remove them
        for column in main_board.keys():
            if main_board[column] == board_copy[column]:
                correct_color_and_position+=1
                board_copy.pop(column)

        # get all colors in main board and see whether color is present in check board
        #delete color from list to avoid duplicates
        colors_in_board = list(main_board.values())
        for color in list(board_copy.values()):
            if color in colors_in_board:
                correct_color_wrong_position+=1
                colors_in_board.pop(color)

        return correct_color_and_position, correct_color_wrong_position

    #checks guesses against the mastermind board
    #guesses should be given in sentences such as 'r_1 & b_2 & o_3 & i_4' order is unimportant, for example 
    # r_1 & b_2 & i_4 & o_3' is also valid
    #returns two lists, the first containing the guesses with correct color and position
    # the second with guesses with correct color and wrong position
    def check_guess(self,sentence:str):
        #convert the sentence into a dictionary representation of the board
        sentence_board = self.sentence_to_mastermind_board(sentence)
        correct_color_and_position,correct_color_wrong_position = self.compare_boards(self.mastermind_board, sentence_board)
        #game is over if all four positions have been correctly guessed
        game_over = (correct_color_and_position == 4)
        return correct_color_and_position,correct_color_wrong_position, game_over

    def __str__(self):
        str_build = '|| '
        for col in self.mastermind_board.keys():
            str_build = str_build + col+ "_" +self.mastermind_board[col] + " || "
        return str_build


class Mastermind_AI:

    def __init__(self):
        self.mastermind = Mastermind()
        self.belief_base = self.mastermind.belief_base
        self.colors = self.mastermind.colors
        self.game_over = False
        self.correct_color_and_position = []
        self.correct_color_wrong_position = []
        self.guessed = []
        self.n_rounds = 10 #hardcoded maximum 10 rounds

    def __init__(self,n_rounds):
        self.__init__()
        self.n_rounds = n_rounds

    #taken from wikipedia Knuth five-guess algorithm as being best guess
    def best_first_guess(self):
        guess = "r_1 & r_2 & o_3 & o_4"
        self.correct_color_and_position,self.correct_color_wrong_position, self.game_over = self.mastermind.check_guess(guess)
        self.guessed.append(guess)
    
    def random_first_guess(self):
        guess = ' & '.join(self.colors[random.randint(0,5)]+'_'+x for x in range(1,5))
        self.correct_color_and_position,self.correct_color_wrong_position, self.game_over = self.mastermind.check_guess(guess)
        self.guessed.append(guess)

    def informed_guess(self):
        pass

    def update_belief_base(self):
        # update belief base with completely correct information
        #for pred in self.correct_color_and_position:
        pass

    def boolean_translation(conjecture, feedback):
        pass






class Interactive_Mastermind_AI(Mastermind_AI):













