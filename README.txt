This is pretty much where I kept notes to keep everything straight in my mind while working.




Storing State Notation
name = corner_abc where a, b, and c are in alphabetical order
     = edge_ab where a and b are in alphabetical order
     = center_a
     colors:
        blue = b
        green = g
        orange = o
        red = r
        white = w
        yellow = y
    assumed cube layout is:
            +---+
            | Y |
        +---+---+---+---+
        | R | G | O | B |
        +---+---+---+---+
            | W |
            +---+

    therefore, the corner pieces will be corner_bow, corner_boy, corner_brw, corner_bry, corner_gow, corner_goy,
                                            corner_grw, and corner gry
               the edge pieces will be edge_bo, edge_br, edge_bw, edge_by, edge_go, edge_gr, edge_gw, edge_gy, edge_ow,
                                            edge_oy, edge_rw, and edge_ry
               the center pieces will be center_b, center_g, center_o, center_r, center_w, and center_y

Piece position:
    each piece has an x-coord, a y-coord, and a z-coord
    each of these is equal to -1, 0, or 1
    x:
        -1 = L slice, 0 = M slice, 1 = R slice
    y:
        -1 = D slice, 0 = E slice, 1 = U slice
    z:
        -1 = B slice, 0 = S slice, 1 = F slice
    therefore, in a solved cube in standard position, corner_goy has pos 1,1,1
    additionally, this means:
        corner piece will only ever have pos values of -1 or 1
        edges will always have one 0, and two other values that are either -1 or 1
        centers will have two 0s, and one other value that is either -1 or 1




reduction U0 = U-8,-4,0,4,8; U1 = U-7,-3,1,5,9; U2 = U-6,-2,2,6,10; U'(-1(3)) = U-5,-1,3,7,11


Ideas for expansion (large things):
    - AI
        - Quantify 'easiness' in f2l by how many are in D or E but not in position
            - for each of the 4 cycles, quantify each corner and edge that isn't solved, something along the lines of
              +1 for a non-permuted corner in D, +1 for a non-permuted edge in E, then take the min and solve it
        - Improve cross
        - 1 Look OLL using PLL-like sequencing
    - Allow user input for starting position
        - would have to verify that each unique piece exists
            - in order to make color neutral (a user can submit any color (eg pink instead of red on a pastel cube) or
              the sides can be arranged in a non-normal order (eg red opposite white)), would have to generate a list
              of pieces based off of the centers or something, then check the goal list against a list of pieces
              generated based on the face colors
            - there would be three main cases:
                - solvable
                - legally unsolvable
                    no set of legal moves can solve it
                - legally impossible
                    there are not equal amounts of face colors, or a piece has two matching faces, something nonsensical
            - solvable is easy since it's solvable, and impossible is easy since you can do specific error checking,
              but unsolvable would not fail a possibility test, but could not be solved.  The only way I can think for
              this to happen would be if a corner or edge was rotated, which would mean that at the very least you would
              be able to solve cross and f2l (I think).  If you get to oll and the case doesn't exist (eg a sune but the
              corner that should be oriented to start is not
                - the easiest way to check would be to have each step of CFOP return a bool for if it was successful,
                  and only continue if it was

    - Render a cube
    - Allow user input as coloring on the cube?


Ideas just for improvement (to do list essentially):
    - Might be a good idea to have each step return the string of moves it used, then have them added in solve or
      somewhere else (could actually probably get rid of all global variables by doing this, and having a function
      to create the cube
    - 'help' and other commands