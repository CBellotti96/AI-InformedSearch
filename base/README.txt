This program is a small scale model of some commonly used AI search functions.

The problem used is the pancake problem:
https://en.wikipedia.org/wiki/Pancake_sorting

In this implementation, a pancake "stack" of 4 is provided by the user. Each
pancake has a unique number 1-4, 1 being the smallest pancake and 4 being the largest.
The user provides the order of the stack as well as a character representing each
search algorithm:
    d: depth-first search
    u: uniform-cost search
    g: greedy search
    a: a-star search
    
Based on the character provided, the program will run the corresponding algorithm and
find a path to flip the pancakes so that they are in order with the smallest "on top"
of the stack. The path will be printed, along with any cost or heuristic values that
are associated with the designated algorithm.

When you run the py script, it will ask for a starting state and search method

This should be entered in the form "####X", where #### is the 4-digit ID of the
start state, and X is the letter associated with the search method. 

Examples: "3421u", "4213d", "1423a", "2314g"

All input and output is in the console. Once an output is provided, it will
prompt you for another input. If you are finished testing, you can enter q to
exit.
