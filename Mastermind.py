from BeliefBase import BeliefBase
import random
#implementing game logic for 4 pegs, 6 colors, 10 turns (if applicable) mastermind
#possible colors are red (r), orange (o), yellow (y), green (g), blue (b), indigo (i)

class Mastermind:

    def __init__(self):
        self.mastermind_board, self.belief_base = self.initialize_mastermind_game()
        self.n_rounds = 10 #default to ten rounds of guessing

    #set number of rounds
    def __init__(self, n_rounds):
        self.mastermind_board, self.belief_base = self.initialize_mastermind_game()
        self.n_rounds = n_rounds 

    #Initializes the mastermind game by creating a random board
    #returns the board as a dictionary Keys:column number (str), Vals: color (str)
    # and as a BeliefBase object with the cnf representation of the board inserted (eg 'r_1 & b_2 & o_3 & i_4')
    def initialize_mastermind_game(self):
        #possible colors 
        colors = ['r','o','y','g','b','i']

        #list will contain each column and its corresponding, randomly assigned color
        #format is <color>_<column>
        mastermind_board = {}
        for col in range(1,5):
            mastermind_board[str(col)] = colors[random.randint(0,5)]
        final_clause = ''

        # Build the clause for the belief base
        for clause in mastermind_board.keys():
            final_clause = final_clause + str(clause)+"_"+mastermind_board[clause] + " & "
        # remove the last ' & '    
        final_clause = final_clause[:-3]
        
        belief_base = BeliefBase()
        
        belief_base.tell(final_clause)
        return mastermind_board,belief_base
        

    def mastermind_first_guess(auto = True):
        pass
    
    #checks guesses against the mastermind board
    #guesses should be given in sentences such as 'r_1 & b_2 & o_3 & i_4' order is unimportant, for example 
    # r_1 & b_2 & i_4 & o_3' is also valid
    #returns two lists, the first containing the guesses with correct color and position
    # the second with guesses with correct color and wrong position
    def check_guess(self,sentence:str):
        #convert the sentence into a dictionary representation of the board
        sentence_board = self.sentence_to_mastermind_board(sentence)
        correct_color_and_position,correct_color_wrong_position = self.compare_boards(self.mastermind_board, sentence_board)

        return correct_color_and_position,correct_color_wrong_position
    
    #converts a sentence to a mastermind board dictionary. Keys:column number (str), Vals: color (str)
    def sentence_to_mastermind_board(sentence:str):
        mastermind_board = {}
        sentence_list = sentence.split(' & ')
        for predicate in sentence_list:
            split_pred = predicate.split('_')
            mastermind_board[split_pred[1]] = split_pred[0]
        return mastermind_board

    #compares two mastermind boards in the dictionary form
    #returns two lists, the first containing the guesses with correct color and position
    # the second with guesses with correct color and wrong position
    def compare_boards(main_board : dict,board_to_compare :dict):
        correct_color_and_position = []
        correct_color_wrong_position = []
        board_copy = board_to_compare.copy()

        #first run through and check exact matches, then remove them
        for column in main_board.keys():
            if main_board[column] == board_copy[column]:
                correct_color_and_position.append(column+"_"+board_copy[column])
                board_copy.pop(column)

        # get all colors in main board and see whether color is present in check board
        #delete color from list to avoid duplicates
        colors_in_board = list(main_board.values())
        for color in list(board_copy.values()):
            if color in colors_in_board:
                correct_color_wrong_position.append(color)
                colors_in_board.pop(color)

        return correct_color_and_position, correct_color_wrong_position




