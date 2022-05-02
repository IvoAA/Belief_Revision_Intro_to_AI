import itertools

def boolean_translation(guess,n_correct,n_color):
    all_positions = list(map(lambda y : str(y),list(range(1,5))))
    all_colors = ['r','o','y','g','b','i']
    n_wrong = 4- n_correct- n_color
    
    colors_in_guess = list(set([x[0] for x in guess]))
    other_colors = [x for x in all_colors if x not in colors_in_guess]

    
    #all answers are correct and should just return statement of such
    if n_correct == 4:
        return phi_g(guess)
    
    #all answers are wrong, return all colors in all positions wrong
    if n_wrong == 4:
        return phi_r(all_positions,colors_in_guess)

    #all colors are correct return phi_o of each color and all other colors being wrong
    if n_color == 4:
        return "(" + phi_o(all_positions, colors_in_guess, all_positions) + '&' + phi_r(all_positions, other_colors) + ")"
    
    #there are no wrong colors return all possible combinations of correct and other colors, all other colors are wrong
    if n_wrong == 0:
        possible_combinations_correct = list(itertools.combinations(guess, n_correct))
        str_build = []
        for possible_correct_combination in possible_combinations_correct:
            #the combination that is assumed to be correct
            pg = phi_g(possible_correct_combination) 
            #the guessed colors that are assumed to be correct, but in the wrong position
            guesses_in_wrong_position = [x for x in guess if x not in possible_correct_combination]
            
            #positions that cannot be taken by any other color
            fixed_positions = [x[-1] for x in possible_correct_combination]
            
            #all possible combinations of colors guessed
            possible_colors_correct = list(itertools.combinations(guesses_in_wrong_position, n_color))
            
            inner_str_build = []
            #for each possible combination of colors 
            for possible_color_correct_combination in possible_colors_correct:
                colors_chosen = [x[0] for x in possible_color_correct_combination]
                positions_of_colors = [x[-1] for x in possible_color_correct_combination]


                positions_of_incorrect_guesses = [x[-1] for x in all_positions if x not in fixed_positions]
                
                po = phi_o(positions_of_colors, colors_chosen, positions_of_incorrect_guesses)

                inner_str_build.append(po)
            
            por = "(" + (' | ').join(inner_str_build) + ")"
            
            str_build.append('('+ pg + ' & ' + por + ')')
            
        return '(' + '(' + (' | ').join(str_build) + ')' + phi_r(all_positions,other_colors) + ')'
     
    #all guesses are either completely correct or the color is completely wrong - return each combination of color being correct, and each other color being wrong           
    if n_color == 0:
        possible_combinations_correct = list(itertools.combinations(guess, n_correct))
        str_build = []
        for possible_correct_combination in possible_combinations_correct:
            fixed_positions = [x[-1] for x in possible_correct_combination]
            positions_of_incorrect_guesses = [x[-1] for x in all_positions if x not in fixed_positions]
            #the combination that is assumed to be correct
            pg = phi_g(possible_correct_combination) 
            #the guessed colors that are assumed to be wrong
            guesses_in_wrong_position = [x for x in guess if x not in possible_correct_combination]
            colors_incorrectly_guessed = list(set([x[0] for x in guesses_in_wrong_position]))
            
            pr = phi_r(positions_of_incorrect_guesses,colors_incorrectly_guessed)
            
            str_build.append('(' + pg + ' &' + pr + ")")

            
        return '(' + (' | ').join(str_build) + ')' 
     
    #there are no correct guesses, only some colors may be correct, and the rest are wrong    
    if n_correct == 0:
        possible_colors_correct = list(itertools.combinations(guess, n_color))
            
        str_build = []
        for possible_color_correct_combination in possible_colors_correct:
            colors_chosen = [x[0] for x in possible_color_correct_combination]
            positions_of_colors = [x[-1] for x in possible_color_correct_combination]
            
            guesses_deemed_wrong = [x for x in guess if x not in possible_color_correct_combination and x[0] not in colors_chosen]
            colors_guesses_wrong = [x[0] for x in guesses_deemed_wrong]
            
            po = phi_o(positions_of_colors, colors_chosen, all_positions)

            pr = phi_r(all_positions, colors_guesses_wrong)

            str_build.append('('+ po + ' & ' + pr + ')')
        
        return "(" + (' | ').join(str_build) + ")"
    
    #there is a mix of everything
    possible_combinations_correct = list(itertools.combinations(guess, n_correct))

    str_build = []
    for possible_correct_combination in possible_combinations_correct:
        fixed_positions = [x[-1] for x in possible_correct_combination]
        pg = phi_g(possible_correct_combination)

        guesses_deemed_wrong_o = [x for x in guess if x not in possible_correct_combination]

        possible_colors_correct = list(itertools.combinations(guesses_deemed_wrong_o, n_color))
        
        inner_str_build = []
        for possible_color_correct_combination in possible_colors_correct:
            colors_chosen = [x[0] for x in possible_color_correct_combination]
            positions_of_colors = [x[-1] for x in possible_color_correct_combination]
            guesses_deemed_wrong = [x for x in guess if x not in possible_color_correct_combination and x[0] not in colors_chosen]
            colors_guesses_wrong = list(set([x[0] for x in guesses_deemed_wrong]))
            positions_of_incorrect_guesses = [x[-1] for x in all_positions if x not in fixed_positions]
            
            po = phi_o(positions_of_colors, colors_chosen, positions_of_incorrect_guesses)
            pr = phi_r(positions_of_incorrect_guesses, colors_guesses_wrong)

            append_string = '('+ po + ' & ' + pr + ')'
            inner_str_build.append(append_string)
        
        por = "(" + (' | ').join(inner_str_build) +")"
    
        str_build.append('('+ pg + ' & ' +  por + ')')
    
    return "(" + (' | ').join(str_build) + ")"
    
    
    

def phi_g(combination):

        #conjugation of what is known to be wrong
        str_build = []
        for val in combination:
            colors = ['r','o','y','g','b','i']
            taken_position = val[-1]
            taken_color = val[0]
            colors.remove(taken_color)
    
            combinations = list(map(lambda x : ('_').join(x),list(itertools.product(colors,taken_position))))
            #negated values
            combinations = list(map(lambda x : '~'+x, combinations))
            str_build.append("("+ val +' & ' + ' & '.join(combinations)+ ")") #add val, known to be corect
            
        return "(" + (' & ').join(str_build) + ")"
    



def phi_o(positions,colors_chosen, free_positions):
    other_positions = []
    for position in positions:
        other_positions.append([x for x in free_positions if x != position])
        
    zipped = list(zip(other_positions,colors_chosen))

    str_build= []

    for (position_list,color) in zipped:
        if len(position_list)>0:

            mapped_list = [color+ '_' + position for position in position_list]
            str_build.append('('+(' | ').join(mapped_list)+')')
        
    return_string = '('+(' & ').join(str_build)+')' if len(str_build)>0 else ''
    return return_string
        
    
    

def phi_r(positions, colors):
    final_list = [f'{a}_{b}' for a in colors for b in positions]
    final_list = list(map(lambda y: '~'+y,final_list))
    return_string= "(" + (' & ').join(final_list) + ')' if len(final_list)>0 else ''
    return return_string
    
    

    





