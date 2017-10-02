"""
Written by Ezekiel Miller
Started 9/27/17 (give or take a day)
cubology.py
"""
import algs
from variables_n_such import *
import random
import copy

# <editor-fold desc="GLOBAL VARIABLES">
current_cube_pos = solved_cube_pos
current_cube_col = solved_cube_col
performed_moves = []
performed_moves_and_algs = []


# </editor-fold>


# <editor-fold desc="SCRAMBLERS">


def basic_scramble():
    """
    does 21 random moves (not including small letters or full rotations, with the restriction that consecutive moves
    will not be pointless.  In essence this means that if an R (or R' or R2) move is done, the following move
    will not be any R or L (or ' or 2 of course)
    pre-conditions: None
    post-conditions: scrambled (hopefully)
    :return: list, the scramble
    """
    moves = []
    modifier = 17
    move = acceptable_list[random.randrange(0, modifier)]
    turn_interpreter(move)
    moves.append(move)
    for x in range(20):
        move = scramble_list[move[0]][random.randrange(0, 11)]
        turn_interpreter(move)
        moves.append(move)
    return moves


def hardcore_scramble():
    """
    does 21 random moves, including small letters or full rotations, with the restriction that consecutive moves
    will not be pointless.  In essence this means that if an R (or R' or R2) move is done, the following move
    will not be any R or L (or ' or 2 of course)
    pre-conditions: None
    post-conditions: scrambled (hopefully)
    :return: list, the scramble
    """
    moves = []
    move = acceptable_list[random.randrange(0, 54)]
    turn_interpreter(move)
    moves.append(move)
    for x in range(20):
        if move[0].lower() in list(scramble_list.keys()):
            move = scramble_list[move[0]][random.randrange(0, 26)]
        else:
            move = acceptable_list[random.randrange(0, 54)]
        turn_interpreter(move)
        moves.append(move)
    return moves


def scramble_u():
    """
    scrambles only the top layer of the cube by doing a randomized series of 5 oll and U-turn pairs
    pre-conditions: None (I mean if you call it I assume the bottom two layers are solved but I'm not judging)
    post-conditions: Only the top layer has been changed from before function call
    :return: list, the scramble
    """
    moves = []
    for _ in range(5):
        move = algs.algorithms[random.choice(["adjacent_edges_oll", "line_oll", "dot_oll", "sune", "bowtie",
                                              "symmetrical_cross"])]
        turn_string_parser(move)
        moves.append(move)
        move = random.choice(["U", "U", "U2"])
        turn_interpreter(move)
        moves.append(move)
    return moves


# </editor-fold>


# <editor-fold desc="DISPLAY / RETRIEVE DATA FROM CUBE"


def display_cube_state():
    """
    displays the cube's current state.  The cube is retrieved piece by piece from get_piece_color, which this function
    calls repeatedly
    pre-conditions: A cube exists for get_piece_color to call
    post-conditions: prints out the cube as ASCII
    :return: None
    """
    colors = []
    for call in range(0, len(indexes_for_printing), 2):
        colors.append(get_piece_color(indexes_for_printing[call], indexes_for_printing[call + 1]))
    print("\n    +---+\n    |",

          # Top square
          colors[0], colors[1], colors[2], "|\n    |",
          colors[3], colors[4], colors[5], "|\n    |",
          colors[6], colors[7], colors[8], "|\n+---+---+---+---+\n|",

          # Top row
          colors[9], colors[10], colors[11], "|",
          colors[12], colors[13], colors[14], "|",
          colors[15], colors[16], colors[17], "|",
          colors[18], colors[19], colors[20], "|\n|",

          # Middle row
          colors[21], colors[22], colors[23], "|",
          colors[24], colors[25], colors[26], "|",
          colors[27], colors[28], colors[29], "|",
          colors[30], colors[31], colors[32], "|\n|",

          # Bottom Row
          colors[33], colors[34], colors[35], "|",
          colors[36], colors[37], colors[38], "|",
          colors[39], colors[40], colors[41], "|",
          colors[42], colors[43], colors[44], "|\n+---+---+---+---+\n    |",

          # Bottom square
          colors[45], colors[46], colors[47], "|\n    |",
          colors[48], colors[49], colors[50], "|\n    |",
          colors[51], colors[52], colors[53], "|\n    +---+",
          sep='')


def get_piece_color(position, face):
    """
    Gets a face color based on the piece it belongs to, and the axis of the face
    :param position: list, the three position indices of the piece which the face in question belongs to
    :param face: str, 'x', 'y', or 'z', the axis which is perpendicular to the requested face
    :return:
    """
    if face == 'x':
        face = 0
    elif face == 'y':
        face = 1
    else:
        face = 2
    return current_cube_col[list(current_cube_pos.keys())[list(current_cube_pos.values()).index(position)]][face]


def is_solved():
    """
    checks if the cube is solved (regardless of orientation)
    pre-conditions: none
    post-conditions: none
    :return: bool, True if solved, False if not
    """
    colors = []
    for call in range(0, len(indexes_for_printing), 2):
        colors.append(get_piece_color(indexes_for_printing[call], indexes_for_printing[call + 1]))
    if colors[0] == colors[1] == colors[2] == colors[3] == colors[4] == colors[5] == colors[6] == colors[7] == \
            colors[8]:
        if colors[9] == colors[10] == colors[11] == colors[21] == colors[22] == colors[23] == colors[33] == \
                colors[34] == colors[35]:
            if colors[12] == colors[13] == colors[14] == colors[24] == colors[25] == colors[26] == colors[36] == \
                    colors[37] == colors[38]:
                if colors[15] == colors[16] == colors[17] == colors[27] == colors[28] == colors[29] == colors[39] == \
                        colors[40] == colors[41]:
                    if colors[18] == colors[19] == colors[20] == colors[30] == colors[31] == colors[32] == \
                            colors[42] == colors[43] == colors[44]:
                        if colors[45] == colors[46] == colors[47] == colors[48] == colors[49] == colors[50] == \
                                colors[51] == colors[52] == colors[53]:
                            return True
    return False


def pll_sequencer():
    """
    returns a relative list of the top rows current state in the same order as they would be displayed in ASCII text
    (starting at the ULB's L face and wrapping around towards the front)
    :return: list, the sequence of colors as numbers
    """
    sequence = []
    encountered_colors = {}
    for x in pll_sequencer_faces:
        current_face = get_piece_color(x[:3], x[3])
        if current_face not in encountered_colors:
            encountered_colors[current_face] = len(encountered_colors) + 1
        sequence.append(encountered_colors[current_face])
    # print(sequence)
    # display_cube_state()
    return sequence


# </editor-fold>


# <editor-fold desc="OTHER MATH">


def reduce_values(rotation, value):
    """

    :param rotation:
    :param value:
    :return: str, the calculated value with a space at the end
    """
    if value % 4 == 0:
        return ''
    elif value % 4 == 1:
        return rotation + ' '
    elif value % 4 == 2:
        return rotation + '2 '
    else:
        return rotation + "' "


# </editor-fold>


# <editor-fold> desc="CUBE MANIPULATION / TURNS">


def turn(direction, letter):
    """

    :param direction: int, 1 for A, -1 for A'
    :param letter:
    :return:
    """
    positions = turn_positions[letter]
    global current_cube_pos, current_cube_col
    letter = letter.upper()
    direction = int(direction)
    new_cube_pos = copy.deepcopy(current_cube_pos)
    new_cube_col = copy.deepcopy(current_cube_col)
    affected_name = []
    affected_col = []
    for x in positions:
        affected_name.append(list(current_cube_pos.keys())[list(current_cube_pos.values()).index(x)])
        affected_col.append(current_cube_col[list(current_cube_pos.keys())[list(current_cube_pos.values()).index(x)]])
    for piece in affected_name:
        number = affected_name.index(piece)
        new_pos = positions[(number + 2 * direction) % 8]
        new_cube_pos[piece] = new_pos
        col1 = current_cube_col[piece][0]
        col2 = current_cube_col[piece][1]
        col3 = current_cube_col[piece][2]
        if direction != 2:
            if letter == 'U' or letter == 'E' or letter == 'D':
                new_cube_col[piece] = [col3, col2, col1]
            elif letter == 'L' or letter == 'M' or letter == 'R':
                new_cube_col[piece] = [col1, col3, col2]
            else:
                new_cube_col[piece] = [col2, col1, col3]
    current_cube_pos = copy.deepcopy(new_cube_pos)
    current_cube_col = copy.deepcopy(new_cube_col)


def turn_interpreter(letter):
    """

    :param letter:
    :return:
    """
    if letter == '':
        pass
    else:
        performed_moves.append(letter)
        if len(letter) == 1:
            letter = letter + '1'
        elif letter[1] == '\'':
            letter = letter[0] + '-1'
        let = letter[0]
        for x in translation[let]:
            turn(letter[1:], x)
        """
        if len(letter) > 1:
            if let.isupper():
                if letter[1] != '2':        # A'
                    turn(turn_positions[let], -1, let)
                else:                       # A2
                    turn(turn_positions[let], 2, let)
            else:                           # a'
                if letter[1] != '2':
                    turn(turn_positions[translation[let][0]], -1, let)
                    turn(turn_positions[translation[let][1]], -1, let)
    6
                else:                       # a2
                    turn(turn_positions[translation[let][0]], 2, let)
                    turn(turn_positions[translation[let][1]], 2, let)
        else:                               # A
            if let.isupper():
                turn(turn_positions[let], 1, let)
            else:                           # a
                turn(turn_positions[translation[let][0]], 1, let)
                turn(turn_positions[translation[let][1]], 1, let)
        """


def turn_string_parser(string):
    alg = string.split()
    for individual_turn in alg:
        turn_interpreter(individual_turn)


# </editor-fold>


# <editor-fold desc="SOLVERS">


def solve():
    """
    this function houses calls to each individual step method (Cross F2l Oll Pll = CFOP.  In this case I use 2look OLL)
    :return: bool, True if cube solved, False (and the step it broke at) if not
    """
    if cross_naive():
        if f2l():
            if oll_look_1():
                if oll_look_2():
                    if pll():
                        if is_solved():
                            return True
                        else:
                            print("Something went wrong, but I'm not sure where")
                            return False
                    else:
                        print("pll failed.  If cross, f2l, and oll, all passed and this failed, likely unsolvable")
                        return False
                else:
                    print("oll look 2 failed.  If cross and f2l passed and this failed, look 1 probably passed by"
                          "chance, and the cube is probably unsolvable.")
                    return False
            else:
                print("oll look 1 failed.  If cross and f2l passed and this failed, the cube is likely not solvable.")
                return False
        else:
            print("f2l failed.  This pretty unlikely.")
            return False
    else:
        print("cross failed.  This should never happen, so feel special if it does")
        return False


def cross_naive():
    """
    Solves the cross of the bottom color (color neutral but not as efficient as dynamic bottom)
    pre-conditions: assumes cube is solvable
    post-conditions: bottom edges are oriented and permuted
    :return: bool, True if
    """
    bottom = get_piece_color([0, -1, 0], 'y')
    big_u_turns, d_turns = 0, 0
    iterations = 0
    while True:
        iterations += 1
        # display_cube_state()
        if get_piece_color([0, -1, 1], 'y') == bottom and \
            get_piece_color([0, -1, 1], 'z') == get_piece_color([0, 0, 1], 'z') and \
            get_piece_color([0, -1, -1], 'y') == bottom and \
            get_piece_color([0, -1, -1], 'z') == get_piece_color([0, 0, -1], 'z') and \
            get_piece_color([1, -1, 0], 'y') == bottom and \
            get_piece_color([1, -1, 0], 'x') == get_piece_color([1, 0, 0], 'x') and \
            get_piece_color([-1, -1, 0], 'y') == bottom and \
                get_piece_color([-1, -1, 0], 'x') == get_piece_color([-1, 0, 0], 'x'):
            return True
        elif iterations > 20:
            return False
        for _ in range(4):  # clears middle row edges
            if get_piece_color([1, 0, 1], 'z') == bottom or get_piece_color([1, 0, 1], 'x') == bottom:
                while get_piece_color([0, 1, 1], 'z') == bottom or get_piece_color([0, 1, 1], 'y') == bottom:
                    big_u_turns += 1
                    turn(1, "U")
                big_u_turns_final = reduce_values("U", big_u_turns)
                d_turns_final = reduce_values("d", d_turns)
                big_u_turns, d_turns = 0, 0
                # print(big_u_turns_final, d_turns_final, "R U' R'", end=' ')
                turn_string_parser("R U' R'")
                temp_turns = ''
                if big_u_turns_final != '':
                    temp_turns += big_u_turns_final
                if d_turns_final != '':
                    temp_turns += d_turns_final
                temp_turns += "R U' R'"
                performed_moves_and_algs.append(temp_turns)
            d_turns += 1
            turn(-1, "E")
            turn(1, "D")

        for _ in range(4):  # gets all incorrect pieces out of bottom layer without putting anything in E row
            if (get_piece_color([0, -1, 1], 'y') == bottom and get_piece_color([0, -1, 1], 'z') != get_piece_color([
                    0, 0, 1], 'z')) or get_piece_color([0, -1, 1], 'z') == bottom:  # DF contains white but is incorrect
                d_turns = 0
                while get_piece_color([0, 1, 1], 'z') == bottom or get_piece_color([0, 1, 1], 'y') == bottom:
                    # display_cube_state()
                    big_u_turns += 1
                    turn(1, "U")
                d_turns_final = reduce_values("d", d_turns)
                big_u_turns_final = reduce_values("U", big_u_turns)
                big_u_turns, d_turns = 0, 0
                turn_string_parser("F2")
                # print(d_turns_final, big_u_turns_final, "F2", end=' ')
                temp_turns = ''
                if big_u_turns_final != '':
                    temp_turns += big_u_turns_final
                if d_turns_final != '':
                    temp_turns += d_turns_final
                temp_turns += "F2"
                performed_moves_and_algs.append(temp_turns)

            d_turns += 1
            turn(-1, "E")
            turn(1, "D")

        big_u_turns, d_turns = 0, 0
        for __ in range(4):  # gets all pieces out of top layer correctly in bottom layer
            if get_piece_color([0, 1, 1], 'y') == bottom:  # white piece top layer facing U
                while get_piece_color([0, 1, 1], 'z') != get_piece_color([0, 0, 1], 'z'):  # the piece matches center
                    d_turns += 1
                    turn(-1, 'E')
                    turn(1, 'D')
                big_u_turns_final = reduce_values("U", big_u_turns)
                d_turns_final = reduce_values("d", d_turns)
                big_u_turns, d_turns = 0, 0
                # print(big_u_turns_final, d_turns_final, "F2", end=' ')
                temp_turns = ''
                if big_u_turns_final != '':
                    temp_turns += big_u_turns_final
                if d_turns_final != '':
                    temp_turns += d_turns_final
                temp_turns += "F2"
                performed_moves_and_algs.append(temp_turns)
                turn_interpreter('F2')  # flips the piece into place

            if get_piece_color([0, 1, 1], 'z') == bottom:  # white piece top layer facing F
                while get_piece_color([0, 1, 1], 'y') != get_piece_color([0, 0, 1], 'z'):  # the piece matches center
                    d_turns += 1
                    turn(-1, 'E')
                    turn(1, 'D')
                big_u_turns_final = reduce_values("U", big_u_turns)
                d_turns_final = reduce_values("d", d_turns)
                big_u_turns, d_turns = 0, 0
                # print(big_u_turns_final, d_turns_final, "U' R' F R", end=' ')
                temp_turns = ''
                if big_u_turns_final != '':
                    temp_turns += big_u_turns_final
                if d_turns_final != '':
                    temp_turns += d_turns_final
                temp_turns += "U' R' F R"
                performed_moves_and_algs.append(temp_turns)
                turn_string_parser("U' R' F R")  # flips the piece into place
            turn(1, 'U')


def f2l():
    """
    completely color neutral, simply assumes the current bottom is the bottom to be solved, and that it's cross is done
    solves bottom corners and middle layer edges
    :return: bool, True if f2l solved, False if not
    """
    bottom = get_piece_color([0, -1, 0], 'y')
    if not (get_piece_color([1, -1, 0], 'y') == bottom and get_piece_color([-1, -1, 0], 'y') == bottom and
            get_piece_color([0, -1, 1], 'y') == bottom and get_piece_color([0, -1, -1], 'y') == bottom):
        print("cross failed")
    bottom = get_piece_color([0, -1, 0], 'y')
    front = get_piece_color([0, 0, 1], 'z')
    right = get_piece_color([1, 0, 0], 'x')
    left = get_piece_color([-1, 0, 0], 'x')
    back = get_piece_color([0, 0, -1], 'z')
    corner1 = "corner_" + ''.join(sorted(bottom + front + right))
    corner2 = "corner_" + ''.join(sorted(bottom + back + right))
    corner3 = "corner_" + ''.join(sorted(bottom + front + left))
    corner4 = "corner_" + ''.join(sorted(bottom + back + left))
    edge1 = "edge_" + ''.join(sorted(front + right))
    edge2 = "edge_" + ''.join(sorted(back + right))
    edge3 = "edge_" + ''.join(sorted(front + left))
    edge4 = "edge_" + ''.join(sorted(back + left))

    corners = [corner1, corner2, corner3, corner4]
    edges = [edge1, edge2, edge3, edge4]
    # corners = ["corner_brw", "corner_bow", "corner_grw", "corner_gow"]
    # edges = ["edge_br", "edge_bo", "edge_gr", "edge_go"]
    # could make color neutral by generating these lists from centers

    for value in range(4):
        corner, edge = corners[value], edges[value]
        # print(corner)
        # display_cube_state()
        # print(corner + " " + edge)
        # display_cube_state()
        color_list = [corner[7], corner[8], corner[9]]
        # print(color_list)
        color_list_2 = [get_piece_color([current_cube_pos[corner][0], 0, 0], 'x'),
                        get_piece_color([0, current_cube_pos[corner][1], 0], 'y'),
                        get_piece_color([0, 0, current_cube_pos[corner][2]], 'z')]
        if color_list == color_list_2.sort():   # corner is in place, not necessarily oriented correctly
            pass

        elif current_cube_pos[corner][1] == -1:         # corner in bottom
            d_turns = 0
            while not current_cube_pos[corner] == [1, -1, 1]:  # gets active corner to DFR
                turn(-1, "E")
                turn(1, "D")
                d_turns += 1
            if current_cube_pos[edge] == [0, 1, -1]:  # makes sure active edge won't go to FR
                turn_interpreter("U'")
                performed_moves_and_algs.append("U'")
            final_d_turns = reduce_values("d", d_turns)
            temp_turns = final_d_turns + "R U R'"
            turn_string_parser("R U R'")
            performed_moves_and_algs.append(temp_turns)

        # after this the active corner should be either in place or in U

        if current_cube_pos[edge][1] == 0:  # goal edge is in E
            d_turns = 0
            while current_cube_pos[edge] != [1, 0, 1]:  # gets active edge to FR
                turn(-1, "E")
                turn(1, "D")
                d_turns += 1
            if current_cube_pos[corner] == [1, 1, 1]:  # makes sure active corner won't go to DFR
                turn_interpreter("U")
                performed_moves_and_algs.append("U'")
            final_d_turns = reduce_values("d", d_turns)
            temp_turns = final_d_turns + "R U R'"
            performed_moves_and_algs.append(temp_turns)
            turn_string_parser("R U R'")

        # at this point both the active edge and active corner should be either permuted correctly or in U

        non_bottom_colors = corner.replace('corner_', '')
        non_bottom_colors = non_bottom_colors.replace(get_piece_color([0, -1, 0], 'y'), '')
        non_bottom_colors = [non_bottom_colors[0], non_bottom_colors[1]]
        d_turns = 0
        while not (get_piece_color([0, 0, 1], 'z') in non_bottom_colors and
                   get_piece_color([1, 0, 0], 'x') in non_bottom_colors):  # gets active corner spot to DFR
            turn(-1, "E")
            turn(1, "D")
            d_turns += 1
        final_d_turns = reduce_values("U", d_turns)
        performed_moves_and_algs.append(final_d_turns)

        # at this point the corner and edge should either be in place or in U, and the active slot should be DFR/FR

        u_turns = 0
        while not (current_cube_pos[corner] == [1, 1, 1] or current_cube_pos[corner] == [1, -1, 1]):  # corner DFR/FRU
            u_turns += 1
            turn(1, "U")
        final_u_turns = reduce_values("U", u_turns)
        performed_moves_and_algs.append(final_u_turns)
        front_temp = get_piece_color([0, 0, 1], 'z')
        u_turns = 0
        while True:
            case = (list(f2l_position_translator.keys())[list(f2l_position_translator.values()).index(current_cube_pos[
                                                                                                    corner])] + '_')
            case += (f2l_position_translator[(current_cube_col[corner].index(front_temp))] + '_')
            case += (list(f2l_position_translator.keys())[list(f2l_position_translator.values()).index(current_cube_pos[
                                                                                                    edge])] + '_')
            case += (f2l_position_translator[(current_cube_col[edge].index(front_temp))])
            if case in algs.algorithms:
                break
            else:
                u_turns += 1
                turn(1, "U")
        performed_moves_and_algs.append(reduce_values("U", u_turns))
        turn_string_parser(algs.algorithms[case])

    if get_piece_color([-1, 0, 1], 'z') == get_piece_color([-1, -1, 1], 'z') == get_piece_color([0, 0, 1], 'z') == \
            get_piece_color([1, 0, 1], 'z') == get_piece_color([1, -1, 1], 'z') and \
            get_piece_color([-1, 0, -1], 'z') == get_piece_color([-1, -1, -1], 'z') == \
            get_piece_color([0, 0, -1], 'z') == get_piece_color([1, 0, -1], 'z') == \
            get_piece_color([1, -1, -1], 'z') and \
            get_piece_color([-1, 0, -1], 'x') == get_piece_color([-1, -1, -1], 'x') == \
            get_piece_color([-1, 0, 0], 'x') == get_piece_color([-1, 0, 1], 'x') == \
            get_piece_color([-1, -1, 1], 'x') and \
            get_piece_color([1, 0, -1], 'x') == get_piece_color([1, -1, -1], 'x') == \
            get_piece_color([1, 0, 0], 'x') == get_piece_color([1, 0, 1], 'x') == get_piece_color([1, -1, 1], 'x'):
        return True
    else:
        return False


def oll_look_1():
    """
    determines the correct first look OLL algorithm to do, prints its name and its moves, and performs it
    pre-conditions: cube has f2l solved and on bottom (the unsolved layer is U).  Will temporarily only work with
    yellow, but will return and make it work with all later
    post-conditions: cube has f2l solved and down, and all of U is oriented correctly (the top face will all be yellow)
    :return: bool, True if look 1 done, False if not
    """
    u_r_edge_top = get_piece_color([1, 1, 0], 'y')
    u_l_edge_top = get_piece_color([-1, 1, 0], 'y')
    u_f_edge_top = get_piece_color([0, 1, 1], 'y')
    u_b_edge_top = get_piece_color([0, 1, -1], 'y')
    top = get_piece_color([0, 1, 0], 'y')
    u_turns = 0
    if u_r_edge_top == top and u_f_edge_top == top and u_l_edge_top == top and u_b_edge_top == top:
        case = 'oll_done'
    else:
        for _ in range(4):
            # print(get_piece_color([1, 1, 0], 'y'))
            if get_piece_color([1, 1, 0], 'y') == top and get_piece_color([-1, 1, 0], 'y') == top:
                case = "line_oll"  # U-R edge and U-L edge
                break
            elif get_piece_color([1, 1, 0], 'y') == top and get_piece_color([0, 1, 1], 'y') == top:
                case = "adjacent_edges_oll"  # U-R edge and U-F edge
                break
            else:
                # print('U', end=' ')
                u_turns += 1
                turn_interpreter('U')

        else:
            case = "dot_oll"
    final_u_turns = reduce_values("U", u_turns)
    temp_turns = final_u_turns + case + '(' + algs.algorithms[case] + ')'
    performed_moves_and_algs.append(temp_turns)
    performed_moves.append(algs.algorithms[case])
    turn_string_parser(algs.algorithms[case])

    u_r_edge_top = get_piece_color([1, 1, 0], 'y')
    u_l_edge_top = get_piece_color([-1, 1, 0], 'y')
    u_f_edge_top = get_piece_color([0, 1, 1], 'y')
    u_b_edge_top = get_piece_color([0, 1, -1], 'y')
    if u_r_edge_top == top and u_f_edge_top == top and u_l_edge_top == top and u_b_edge_top == top:
        return True
    else:
        print("top cross is not complete, and is either not solvable or the previous steps were not complete")
        return False


def oll_look_2():
    """
    determines the correct second look OLL algorithm to do, prints its name and its moves, and performs it on current U
    pre-conditions: f2l is solved and down, top cross (color neutral) is oriented
    post-conditions: f2l is solved and down, top face is yellow
    :return: bool, True if second look done, False if not
    """
    u_r_f_top = get_piece_color([1, 1, 1], 'y')
    u_l_f_top = get_piece_color([-1, 1, 1], 'y')
    u_r_b_top = get_piece_color([1, 1, -1], 'y')
    u_l_b_top = get_piece_color([-1, 1, -1], 'y')
    top = get_piece_color([0, 1, 0], 'y')
    corner_pieces_oriented = 0
    u_turns = 0
    if u_r_b_top == top:
        corner_pieces_oriented += 1
    if u_r_f_top == top:
        corner_pieces_oriented += 1
    if u_l_f_top == top:
        corner_pieces_oriented += 1
    if u_l_b_top == top:
        corner_pieces_oriented += 1

    if corner_pieces_oriented == 4:  # solved top cross
        return True

    if corner_pieces_oriented == 0:  # cross (symmetrical or asymmetrical)
        while get_piece_color([-1, 1, 1], 'x') != top or get_piece_color([-1, 1, -1], 'x') != top:  # get pair to LF
            u_turns += 1
            turn(1, 'U')
        if get_piece_color([1, 1, 1], 'z') == top:  # asymmetrical_cross
            case = 'asymmetrical_cross'
        else:  # symmetrical_cross
            case = 'symmetrical_cross'

    elif corner_pieces_oriented == 1:  # sune or anti-sune
        while get_piece_color([-1, 1, 1], 'y') != top:  # get yellow top to ULF
            u_turns += 1
            turn(1, 'U')
        if get_piece_color([1, 1, 1], 'z') == top:  # sune
            case = 'sune'
        else:  # anti-sune
            case = 'anti-sune'
            u_turns += 1
            turn(1, 'U')

    elif corner_pieces_oriented == 2:  # headlights, chameleon, or bowtie
        while get_piece_color([1, 1, 1], 'z') != top:  # get a yellow piece to URF facing F
            u_turns += 1
            turn(1, 'U')
        if get_piece_color([-1, 1, 1], 'z') == top:  # headlights
            case = 'headlights'
        elif get_piece_color([-1, 1, -1], 'x') == top:  # bowtie
            case = 'bowtie'
        else:  # chameleon
            u_turns += 2
            turn(2, 'U')
            case = 'chameleon'
    else:
        print("Cube is either unsolvable, or the previous steps were not successfully completed")
        return False

    final_turn = reduce_values('U', u_turns)
    if final_turn != '':
        temp_turns = final_turn + case + "(" + algs.algorithms[case] + ")"
        performed_moves_and_algs.append(temp_turns)
    turn_string_parser(algs.algorithms[case])

    # cross should be completed at this point

    u_r_f_top = get_piece_color([1, 1, 1], 'y')
    u_l_f_top = get_piece_color([-1, 1, 1], 'y')
    u_r_b_top = get_piece_color([1, 1, -1], 'y')
    u_l_b_top = get_piece_color([-1, 1, -1], 'y')
    if u_r_b_top == top and u_l_b_top == top and u_l_f_top == top and u_r_f_top == top:
        return True
    else:
        return False


def pll():
    """
    calculates and performs the correct pre-moves, algorithm, and post moves to solve the cube (and it's color neutral!)
    pre-conditions: the cube has f2l done and down, and the top layer oriented correctly
    post-conditions: the cube is solved!
    :return: bool, True if pll is done, False if not (though if it isn't it's probably gonna crash anyway)
    """
    u_turns = 0
    for _ in range(4):
        sequence = pll_sequencer()
        if sequence in list(pll_sequences.values()):
            case = list(pll_sequences.keys())[list(pll_sequences.values()).index(sequence)]
            if case != "pll_done":
                u_turns_final = reduce_values("U", u_turns)
                temp_turns = u_turns_final + case + "(" + algs.algorithms[case] + ")"
                performed_moves_and_algs.append(temp_turns)
                performed_moves.append(u_turns_final)
                turn_string_parser(algs.algorithms[case])
                break
            else:
                break
        else:
            turn(1, "U")
            u_turns += 1
    else:
        return False
    u_turns = 0
    if list(pll_sequences.keys())[list(pll_sequences.values()).index(pll_sequencer())] == 'pll_done':
        while get_piece_color([0, 1, 1], 'z') != get_piece_color([0, 0, 1], 'z'):
            turn(1, "U")
            u_turns += 1
        u_turns_final = reduce_values("U", u_turns)
        performed_moves_and_algs.append(u_turns_final)
        performed_moves.append(u_turns_final)
        return True
    else:
        return False


# </editor-fold>


# <editor-fold desc="TESTING">


def test_forever(scramble_type):
    """

    :param scramble_type:
    :return:
    """
    while True:
        if scramble_type.lower() == 'u':
            scramble_u()
        elif scramble_type.lower() == 'basic':
            basic_scramble()
        elif scramble_type.lower() == 'hardcore':
            hardcore_scramble()
            display_cube_state()
        solve()
        if not is_solved():
            print("Failed on a", scramble_type, "scramble")
            break
        else:
            print("solved")
            print(' '.join(performed_moves_and_algs))
            display_cube_state()


# </editor-fold>


# <editor-fold desc="OTHER">


def infinite_iteration():
    """
    Simply loops to let the user manipulate the cube how they wish, using a set of commands
    :return: None
    """
    while True:
        display_cube_state()
        if is_solved():
            print("The cube is solved! Ta-da!")
        request = input("Which turn or alg to perform? ('exit' to exit, 'help' for additional commands) ")
        if request.lower() == "exit":
            print("Program will now exit")
            exit()  # could add option to save state to file
        elif request.lower() == "scramble":
            while True:
                scramble_type = input("What kind of scramble? [u/basic/hardcore] ")
                if scramble_type.lower() == 'u':
                    scramble = scramble_u()
                elif scramble_type.lower() == 'basic':
                    scramble = basic_scramble()
                elif scramble_type.lower() == 'hardcore':
                    scramble = hardcore_scramble()
                else:
                    print("Invalid scramble type")
                    continue
                if input("Print the scramble? [y/n] ") == 'y':
                    print(' '.join(scramble))
                break
        elif request == "solvesolvesolvethanks":
            for piece in current_cube_pos:
                current_cube_pos[piece] = solved_cube_pos[piece]
                current_cube_col[piece] = solved_cube_col[piece]
        elif request.lower() == "moves performed":
            print(len(performed_moves), "moves")
            print(' '.join(performed_moves_and_algs))
            print(' '.join(performed_moves))
            # print(performed_moves)
        elif request.lower() == "solve":
            if not solve():
                print("Sorry, I couldn't figure out how to solve it.  Make sure the cube is solvable!")
            #
        elif request.lower() == "cross naive":
            cross_naive()
            #
        elif request.lower() == "f2l":
            f2l()
            #
        elif request.lower() == "2 look oll":
            oll_look_1()
            oll_look_2()
        elif request.lower() == "oll look 1":
            oll_look_1()
            #
        elif request.lower() == "oll look 2":
            oll_look_2()
            #
        elif request.lower() == "pll":
            pll()
            #
        elif request.lower() == "pll sequence":
            pll_sequencer()
            #
        elif request in acceptable_list:
            turn_interpreter(request)
            #
        elif request.lower() in list(algs.algorithms.keys()):
            turn_string_parser(algs.algorithms[request.lower()])
            #
        else:
            print("Input not recognized.")


# </editor-fold>


def main():
    # starting_cube_pos = solved_cube_pos
    # starting_cube_col = solved_cube_col
    global current_cube_pos, current_cube_col
    current_cube_pos = copy.deepcopy(solved_cube_pos)
    current_cube_col = copy.deepcopy(solved_cube_col)
    # test_forever('hardcore')
    infinite_iteration()


main()
