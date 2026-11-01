from obj import *

c = Sudoku("very_simple_sudoku.csv") #enters the csv document
b = Solver(c)


while True:

    x = b.quick_checker()
    if x == -2:
        print("Sudoku Solved!")
        c.print_board()
        break
    if x == -1:
        b.cls_check()
    else:
        x = list(x)
        b.quick_solver(x[0], int(x[1]))
