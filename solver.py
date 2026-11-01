from obj import *

sudoku_format = Sudoku("sample.csv") #enters the csv document
solving = Solver(sudoku_format)


while True:
    x = solving.quick_checker()
    if x == -2:
        print("Sudoku Solved!")
        sudoku_format.print_board()
        break
    if x == -1:
        ch = solving.cls_check() #if 0 we use other algorhythms
        if ch == 0:
            print("There is nothing else we can do") #in newer version it will use other algorhythms to solve more difficult puzzles
            break
    else:
       x = list(x)
       solving.quick_solver(x[0], int(x[1]))
