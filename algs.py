"""
stores all the algorithms used in solving and that are usable by the user in the infinite iteration input loop
currently the way infinite_iteration works prevents the F2l algs from being used (since they have uppercase characters)
this is essentially meant to be a way for those who use the program to solve by inputting moves to learn to recognize
cases, then to learn the algs after, as well as making it much easier to solve
"""

algorithms = {

    # <editor-fold desc="F2L (purposefully not callable)">
    # Standard formula for F2L:
    # ABC_OF_CORNER + _ + F_face_corner_face[x/y/z] + _ + AB_OF_EDGE + _ + F_face_edge_face[x/y/z]
    # pos[7:]_<not sure how to determine which is which>_pos[5:]
    # f face will always be clockwise 1 from bottom

    # Easy Cases
    'FRU_y_RU_y': "U R U' R'",
    'FRU_z_FU_z': "U' F' U F",
    'FRU_y_LU_x': "F' U' F",
    'FRU_z_BU_y': "R U R'",

    # Reposition Edge
    'FRU_y_BU_y': "U' R U R' U2 R U' R'",
    'FRU_z_LU_x': "d R' U' R U2 R' U R d'",
    'FRU_y_LU_y': "U' R U2 R' U2 R U' R'",
    'FRU_z_BU_z': "d R' U2 R U2 R' U R d'",

    # Reposition Edge and Flip Corner
    'FRU_y_BU_z': "d R' U' R U' R' U' R d'",
    'FRU_z_LU_y': "U' R U R' U R U R'",
    'FRU_y_RU_x': "U' R U2 R' d R' U' R d'",
    'FRU_z_FU_y': "d R' U2 R d' R U R'",
    'FRU_y_FU_z': "d R' U R U' R' U' R d'",
    'FRU_z_RU_y': "U' R U' R' U R U R'",

    # Split Pair by Going Over
    'FRU_y_FU_y': "y' R' U R U' d' R U R'",
    'FRU_z_RU_x': "R U' R' U d R' U' R",
    'FRU_x_RU_y': "R U2 R' U' R U R'",
    'FRU_x_FU_z': "y' R' U2 R U R' U' R",

    # Pair Made on Side
    'FRU_x_BU_y': "U R U2 R' U R U' R'",
    'FRU_x_LU_x': "y' U' R' U2 R U' R' U R y",
    'FRU_x_LU_y': "U2 R U R' U R U' R'",
    'FRU_x_BU_z': "y' U2 R' U' R U' R' U R y",

    # Weird
    'FRU_x_FU_y': "R U R' U2 R U R' U' R U R'",
    'FRU_x_RU_x': "y' R' U' R U2 R' U' R U R' U' R y",

    # Corner in Place, edge in U Face
    'DFR_z_RU_y': "d' L' U L d R U' R' d",
    'DFR_z_FU_z': "U R U' R' d' L' U L",
    'DFR_x_RU_y': "R U' R' U R U' R'",
    'DFR_y_FU_z': "y' R U R' U' R U R' y",
    'DFR_x_FU_z': "y' R' U' R U R' U' R y",
    'DFR_y_RU_y': "R U R' U' R U R'",

    # Edge in Place, Corner in U Face
    'FRU_x_FR_x': "R U' R' d R' U R",
    'FRU_x_FR_z': "R U R' U' R U R' U' R U R'",
    'FRU_y_FR_z': "U' R U' R' U2 R U' R'",
    'FRU_z_FR_z': "U' R U2 R' U R U R'",
    'FRU_y_FR_x': "U' R U R' d R' U' R d'",
    'FRU_z_FR_x': "d R' U' R d' R U R' d'",

    # Edge and Corner in Place
    'DFR_z_FR_z': "",
    'DFR_z_FR_x': "R U' R' d R' U2 R U2 R' U R",
    'DFR_x_FR_z': "R U' R' U' R U R' U2 R U' R'",
    'DFR_y_FR_z': "R U' R' U R U2 R' U R U' R'",
    'DFR_x_FR_x': "R U' R' d R' U' R U' R' U' R d'",
    'DFR_y_FR_x': "R U' R' d2 y R' U' R U' R' U R y",



    # </editor-fold>
    # <editor-fold desc="2-look OLL">

    # 2 look OLL, first look
    'oll_done': "",
    'adjacent_edges_oll': "f R U R' U' f' ",
    'line_oll': "F R U R' U' F' ",
    'dot_oll': "F R U R' U' F' f R U R' U' f' ",


    # 2 look OLL, second look
    'sune': "R U R' U R U2 R' ",
    'anti-sune': "R' U' R U' R' U2 R ",
    'headlights': "R2 D R' U2 R D' R' U2 R' ",
    'bowtie': "F' r U R' U' r' F R ",
    'chameleon': "r U R' U' r' F R F' ",
    'symmetrical_cross': "R U R' U R U' R' U R U2 R' ",
    'asymmetrical_cross': "R' U2 R2 U R2 U R2 U2 R' ",

    # </editor-fold>
    # <editor-fold desc="PLL">

    # 1 look PLL
    "pll_done": "",
    'u_perm_a': "R U' R U R U R U' R' U' R2",
    'u_perm_b': "R2 U R U R' U' R' U' R' U R'",
    'z_perm': "M2 U M2 U M' U2 M2 U2 M' U2",
    'h_perm': "M2 U M2 U2 M2 U M2",
    'a_perm_a': "R' F R' B2 R F' R' B2 R2",
    'a_perm_b': "R B' R F2 R' B R F2 R2",
    'e_perm': "x' R U' R' D R U R' D' R U R' D R U' R' D' x ",
    't_perm': "R U R' U' R' F R2 U' R' U' R U R' F'",
    'r_perm_a': "L U2 L' U2 L F' L' U' L U L F L2 U",
    'r_perm_b': "R' U2 R U2 R' F R U R' U' R' F' R2 U'",
    'j_perm_a': "R' U L' U2 R U' R' U2 R L U'",
    'j_perm_b': "R U R' F' R U R' U' R' F R2 U' R' U'",
    'f_perm': "R' U2 R' d' R' F' R2 U' R' U R' F R U' F",
    'v_perm': "R' U R' d' R' F'' R2 U'' R' U R' F R F",
    'y_perm': "F R U' R' U' R U R' F' R U R' U' R' F R F'",
    'n_perm_a': "L U' R U2 L' U R' L U' R U2 L' U R' U",
    'n_perm_b': "R' U L' U2 R U' L R' U L' U2 R U' L U'",
    'g_perm_a': "R2 U R' U R' U' R U' R2 D U' R' U R D'",
    'g_perm_b': "R' U' R U D' R2 U R' U R U' R U' R2 D",
    'g_perm_c': "U2 R2 F2 R U2 R U2 R' F R U R' U' R' F R2 U2",
    'g_perm_d': "R U R' U' D R2 U' R U' R' U R' U R2 D'",

    # </editor-fold>
    # <editor-fold desc="Other">

    'superflip': "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2",
    'checkerboard': "M2 E2 S2"

    # </editor-fold>

}
