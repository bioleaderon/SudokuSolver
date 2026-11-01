lazy import pandas as pd
from pandas import DataFrame
lazy import numpy as np

def decode(index_0_8: int):  ###decoding the 0-8-square indexing
    x = 3 * index_0_8 // 3
    index_0_8 -= (index_0_8 // 3) * 3
    return x, index_0_8  ###returns the coordinations of the first cell of the square


def decode_cell_from_square(first_x_coord: int,
                             index_in_full_list: int):  ####0-8 indexing when full list (len()=9) from get_square
    y_index = index_in_full_list - (index_in_full_list // 3) * 3
    x_index = first_x_coord + index_in_full_list // 3
    return x_index, y_index




class Sudoku:
    def __init__(self, sudoku_archieve:str):
        a = pd.read_csv(filepath_or_buffer=sudoku_archieve, header=None, keep_default_na=False, dtype="Int64")
        a = a.replace({np.nan: None})

        a = DataFrame(a)
        self.sudoku = a

    def __getitem__(self, pos1): #returns a specific cell
        x,y = pos1
        cell = self.sudoku.iat[x,y]
        if cell:
            cell = int(cell)
        return cell


    def __setitem__(self, pos1, value): #changes specified value in the dataframe
        x,y = pos1
        self.sudoku.iat[x,y] = value

    def print_board(self):
        print(self.sudoku)

    def get_square(self, cell_index_x:int, cell_index_y:int, get_none=False) -> list: #returns the existing values that exist on the square the cell exists
        square_values = []
        x = cell_index_x // 3
        y = cell_index_y // 3
        for i in range(3*x, 3*x+3):
            for j in range(3*y, 3*y+3):
                if not get_none:
                    if self[i,j]:
                        square_values.append(self[i,j])
                else:
                    square_values.append(self[i, j])
        return square_values

    def get_row(self, line_index:int, get_none=False) -> list: #0-8
        row_list = self.sudoku.iloc[line_index].tolist()
        if not get_none:
            while True:

                if None not in row_list:
                    break
                row_list.remove(None)
        return row_list

    def get_column(self, column_index:int, get_none=False) -> list: #0-8
        column_list = self.sudoku.iloc[:, column_index].tolist()
        if not get_none:
            while True:

                if None not in column_list:
                    break
                column_list.remove(None)
        return column_list




class Solver:
    def __init__(self, sudoku:Sudoku):
        self.sudoku = sudoku
        self.lines = []    ###evaluate every line based on how many values we've got
        self.columns = [] ###evaluate every column based on how many values we've got
        self.square = []  ##evaluate every square based on how many values we've got

    #grades lines, columns, squares based on how many values exist
        def grading_system(it:list):
            return len(it)

        for i in range(9):
            self.lines.append(grading_system(self.sudoku.get_row(i)))
            self.columns.append(grading_system(self.sudoku.get_column(i)))
            if i < 3:
                for j in [1,4,7]: #we enumerate every square from 0-8 (using the list's indexes)
                    self.square.append(grading_system(self.sudoku.get_square(3 * i, j)))

    def upgrade_grades(self, x:int, y:int):
        self.lines[x] += 1
        self.columns[y] += 1
        z = 3*(x//3) + y // 3
        self.square[z] += 1



    def quick_checker(self): #checks if any line, column, square exists with one value missing, making easy the search for other missing values to be found
        if len(set(self.square)) == 1:
            return -2 #sudoku solved
        if 8 in self.lines:
            return f"l{self.lines.index(8)}"
        if 8 in self.columns:
            return f"c{self.columns.index(8)}"
        if 8 in self.square:
            return f"s{self.square.index(8)}"
        return -1



    def quick_solver(self, typ:str, index:int): #finds the missing values from quick checker


        def straight_replacement(l1:list, l2:list): ##replacement for lines and columns
            solution = -1
            for i in range(1,10):
                if i not in l1:
                    solution = i
                    break
            x = index
            y = l2.index(None)
            self.sudoku[x, y] = solution
            return x, y


        if typ == "l":
            x, y = straight_replacement(self.sudoku.get_row(index), self.sudoku.get_row(index, get_none=True))
            self.upgrade_grades(x,y)

        elif typ == "c":
            x,y = straight_replacement(self.sudoku.get_column(index), self.sudoku.get_column(index, get_none=True))
            self.upgrade_grades(x,y)

        else:
            x,y = decode(index)
            l_index = self.sudoku.get_square(x, y, get_none=True).index(None) #index of give_square list
            x_index, y_index = decode_cell_from_square(x, l_index)
            solution = -1
            for i in range(1,10):
                if i not in self.sudoku.get_square(x,y):
                    solution = i
                    break
            self.sudoku[x_index, y_index] = solution

    def cls_check(self): ###checks taking into consideration columns, lines, square
        stabilizer = 1

        z = self.square.copy()
        while len(z) != 0:
            for i in z:
                if i > stabilizer and i < 9:
                    stabilizer = i
            max_square = stabilizer
            try:
                z.remove(max_square)
            except ValueError:
                pass

            x, y = decode(self.square.index(max_square))
            full_square_list = self.sudoku.get_square(x, y, get_none=True)
            value_square_list = self.sudoku.get_square(x,y)
            for i in full_square_list:
                if i is None:
                    x_index, y_index = decode_cell_from_square(x, full_square_list.index(i))
                    current_column = self.sudoku.get_column(y_index)
                    current_line = self.sudoku.get_row(x_index)
                    if len(set(current_column+current_line+value_square_list)) == 8:
                        solution = -1
                        for i in range(1,10):
                            solution = i
                            break
                        self.sudoku[x_index, y_index] = solution
                        return 1
                    else:
                        continue
        return 0 #for program control