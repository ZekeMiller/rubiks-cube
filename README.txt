DISCLAIMER: I have been working on this project for less than a week, and I realize it is not perfect.  However, it is functional, and constantly being updated/improved.  Please bear with me through some of the semantic issues.


Rubik's Cube Solver Project:

This is a personal solo passion project I have started in which I devised a way to store the cube's state, perform turns, interpret strings of characters as moves, and automatically solve the cube using the CFOP speedcubing method.

Required Reading:
Standard cube notation https://ruwix.com/the-rubiks-cube/notation/advanced/
Fridrich / CFOP: A speedcubing method that solves Cross, then First 2 layers (f2l), the Orient last layer (OLL, currently this program uses a variation called 2 look oll), and Permute the last layer (PLL)
the program output will tell you when you reach each step, making it easier to follow along.
the algorithms used will also be listed in the program output to help the user learn what the moves mean.
THE REST OF THIS DOCUMENT AND THE PROGRAM ASSUMES YOU KNOW THIS INFORMATION, KNOWING HOW TO SOLVE THE CUBE BY YOURSELF IS NOT NECESSARY


USAGE:

When run, the program prompts the user to either start with a solved cube (which can be scrambled), or to input the cube state face by face (to solve a user's cube).  If inputting by face, the program will go tile by tile and prompt the user to input the color of the currently marked tile.  The program does some light error checking on the inputted state, but there are illegal positions that will pass the basic error checking, that will not be solvable.
After the cube is created (either starting with solved or inputted face by face), the program will prompt the user to input a command.

COMMANDS: 

<any turn in standard notation>     Accepts a turn, or a string of turns seperated by spaces, written in standard notation
2 look oll               			Does both looks of OLL
cross								Does the naive version of cross
exit/quit							Exits the program
f2l									Does F2L (first two layers sans bottom cross)
oll look 1							Does the first look of OLL (the cross)
oll look 2							Does the second look of OLL (the corners)
pll									Does PLL (permutes the top row)
scramble							Prompts the user for the type of scramble, and whether to print the moves, then scrambles the cube
solve								Does all steps in CFOP and prints the moves

ALGORITHM NAMES:
the patterns to recognize can be found in the pdf in this directory

OLL:


Look 1:

adjacent_edges_oll
line_oll
dot_oll


Look 2:

sune
anti-sune
headlights
bowtie
chameleon
symmetrical cross
asymmetrical cross							


PLL:

u_perm_a
u_perm_b
z_perm
h_perm
a_perm_a
a_perm_b
e_perm
t_perm
r_perm_a
r_perm_b
j_perm_a
j_perm_b
f_perm
v_perm
y_perm
n_perm_a
n_perm_b
g_perm_a
g_perm_b
g_perm_c
g_perm_d


Other:

superflip							Flips each edge
checkerboard						Makes a checkerboard on a solved cube


ACKNOWLEDGEMENTS:
All credit for the algorithm pdf goes to badmephisto of kungfoomanchoo.com
I modified the file a bit for my personal use, but I did not originally create it