import itertools

def boolean_translation(guess,n_correct,n_color):
    all_positions = list(map(lambda y : str(y),list(range(1,5))))
    all_colors = ['r','o','y','g','b','i']
    n_wrong = 4 - n_correct- n_color
    
    colors_in_guess = list(set([x[0] for x in guess]))
    other_colors = [x for x in all_colors if x not in colors_in_guess]

    
    #all answers are correct and should just return statement of such
    if n_correct == 4:
        return phi_g(guess)
    
    #all answers are wrong, state that the correct answer as neither of the guessed colors
    if n_wrong == 4:
        str_builder = []
        for color in colors_in_guess:
            for position in range(1, 5):
                str_builder.append(f"{color}_{position}")

        return ' & '.join(str_builder)

    #all colors are correct return phi_o of each color and all other colors being wrong
    if n_color == 4:
        guess_is_wrong = '~' + '  & ~'.join(guess)
        other_colors_wrong = []
        for color in other_colors:
            for position in range(1, 5):
                other_colors_wrong.append(f"{color}_{position}")
        return f"{guess_is_wrong} & {' & '.join(other_colors_wrong)}"
    
    #there are no wrong colors return all possible combinations of correct and other colors, all other colors are wrong
    if n_wrong == 0:
        other_colors_wrong_a = []
        for color in other_colors:
            for position in range(1, 5):
                other_colors_wrong_a.append(f"{color}_{position}")
        other_colors_wrong = ' & '.join(other_colors_wrong_a)

        possible_combinations_correct = list(itertools.combinations(guess, n_correct))
        str_build = []
        for possible_correct_combination in possible_combinations_correct:
            #the combination that is assumed to be correct
            pg = phi_g(possible_correct_combination)

            #the guessed colors that are assumed to be correct, but in the wrong position
            guesses_in_wrong_position = [x for x in guess if x not in possible_correct_combination]


            #positions that cannot be taken by any other color
            fixed_positions = [x[-1] for x in possible_correct_combination]

            # colors in wrong positions
            missing_colors = list(set([x[0] for x in guesses_in_wrong_position]))

            possible_positions_for_color = {}
            for color in missing_colors:
                possible_positions_for_color[color] = []
                for position in range(1, 5):
                    if str(position) not in fixed_positions and f"{color}_{position}" not in guesses_in_wrong_position:
                        possible_positions_for_color[color].append(position)

            possibilities_colors = []
            for color, possible_positions in possible_positions_for_color.items():
                possibilities_colors.append('(' + " | ".join([f"{color}_{pos}" for pos in possible_positions]) + ')')

            str_build.append(f"{pg} & {' & '.join(possibilities_colors)}")
        return f"{other_colors_wrong} & (({') | ('.join(list(set(str_build)))}))"
     
    #all guesses are either completely correct or the color is completely wrong - return each combination of color being correct, and each other color being wrong           
    if n_color == 0:
        possible_combinations_correct = list(itertools.combinations(guess, n_correct))
        str_build = []
        for possible_correct_combination in possible_combinations_correct:
            #the combination that is assumed to be correct
            pg = phi_g(possible_correct_combination)

            #the guessed colors that are assumed to be correct, but in the wrong position
            guesses_in_wrong_position = [x for x in guess if x not in possible_correct_combination]


            #positions that cannot be taken by any other color
            fixed_positions = [x[-1] for x in possible_correct_combination]

            # colors in wrong positions
            wrong_colors = list(set([x[0] for x in guesses_in_wrong_position if x[0]]))

            impossible_color_positions = []
            for color in wrong_colors:
                for position in range(1, 5):
                    if str(position) not in fixed_positions:
                        impossible_color_positions.append(f"~{color}_{position}")

            str_build.append(f"{pg} & {' & '.join(impossible_color_positions)}")

        return f"(({') | ('.join(list(set(str_build)))}))"
     
    #there are no correct guesses, only some colors may be correct, and the rest are wrong    

    if n_correct == 0:
        possible_colors_correct = list(itertools.combinations(guess, n_color))
            
        str_build = []
        for possible_color_correct_combination in possible_colors_correct:
            colors_chosen = [x[0] for x in possible_color_correct_combination]
            colors_not_chosen = list(set([x[0] for x in guess if x[0] not in colors_chosen]))

            wrong_positions = []
            possible_positions_for_color = {}
            for color in colors_chosen:
                possible_positions_for_color[color] = []
                for position in range(1, 5):
                    if guess[position-1][0] == color:
                        wrong_positions.append(f"~{color}_{position}")
                    else:
                        possible_positions_for_color[color].append(f"{color}_{position}")

            possibilities_colors = []
            for possible_positions in possible_positions_for_color.values():
                possibilities_colors.append(f"({' | '.join(possible_positions)})")

            if len(possibilities_colors) == n_color:
                inner_str = []
                if colors_not_chosen:
                    other_colors_wrong_a = []
                    for color in colors_not_chosen:
                        for position in range(1, 5):
                            other_colors_wrong_a.append(f"{color}_{position}")
                    inner_str.append(' & '.join(other_colors_wrong_a))
                inner_str.append(' & '.join(wrong_positions))
                inner_str.append(' & '.join(possibilities_colors))
                str_build.append(' & '.join(inner_str))
        
        return f"({') | ('.join(list(set(str_build)))})"
    
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

    return f"({') | ('.join(str_build)})"


def phi_g(combination):
    return ' & '.join(combination)
    



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
    
    

    





