import itertools

def boolean_translation(guess,n_correct,n_color):
    
    #all answers are correct and should just return statement of such
    if n_correct == 4:
        return phi_g(guess)
    
    all_colors_in_guess = [x[0] for x in guess]
    all_positions = list(map(lambda y : str(y),list(range(1,5))))
    
    #need to break down logic string building by scenario
    
    #there are some correct answers
    if n_correct>0:
        
        #there are some correct colors
        if n_color>0:
    
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
                    
                    guesses_deemed_wrong = [x for x in guess if x not in possible_color_correct_combination]
                    colors_guesses_wrong = [x[0] for x in guesses_deemed_wrong]
                    positions_of_incorrect_guesses = [x for x in all_positions if x not in fixed_positions]
                    
                    po = phi_o(positions_of_colors, colors_chosen, positions_of_incorrect_guesses)
                    pr = phi_r(positions_of_incorrect_guesses, colors_guesses_wrong)

                    append_string = '('+ po + ' & ' + pr + ')' if po != '' else '(' + pr + ')'
                    inner_str_build.append(append_string)
                
                por = (' | ').join(inner_str_build)
            
                str_build.append('('+ pg + ' & ' + por + ')')
            
            return (' | ').join(str_build)
            
            
            
            
            
        #there are no correct colors - all other colors are wrong
        else:

            possible_combinations_correct = list(itertools.combinations(guess, n_correct))
            
            str_build = []
            for possible_correct_combination in possible_combinations_correct:
    
                fixed_positions = [x[-1] for x in possible_correct_combination]
                pg = phi_g(possible_correct_combination)

                guesses_deemed_wrong = [x for x in guess if x not in possible_correct_combination]
                colors_guesses_wrong = [x[0] for x in guesses_deemed_wrong]
                positions_of_incorrect_guesses = [x for x in all_positions if x not in fixed_positions]
                
                pr = phi_r(positions_of_incorrect_guesses,colors_guesses_wrong)

                append_string = '('+ pg + ' & ' + pr + ')' if pr!= '' else '('+ pg + ')'
                str_build.append(append_string)
                
            return (' | ').join(str_build)
                
                
            
    #there may some correct colors
    else:

        #there are some correct colors
        if n_color>0:

            possible_colors_correct = list(itertools.combinations(guess, n_color))
            
            str_build = []
            for possible_color_correct_combination in possible_colors_correct:
                colors_chosen = [x[0] for x in possible_color_correct_combination]
                positions_of_colors = [x[-1] for x in possible_color_correct_combination]
                
                guesses_deemed_wrong = [x for x in guess if x not in possible_color_correct_combination]
                colors_guesses_wrong = [x[0] for x in guesses_deemed_wrong]
                
                po = phi_o(positions_of_colors, colors_chosen, all_positions)

                pr = phi_r(all_positions, colors_guesses_wrong)

                if len(pr) == 0:
                    str_build.append('('+ po + ')')
                else:
                    str_build.append('('+ po + ' & ' + pr + ')')
            
            return (' | ').join(str_build)
                
                
                
            
        #they're all wrong
        else:

            return phi_r(all_positions,all_colors_in_guess)



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
            
        return (' & ').join(str_build)
    



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
    
    

    





