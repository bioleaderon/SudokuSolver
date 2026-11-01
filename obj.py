lazy import pandas as pd
from pandas import DataFrame
lazy import numpy as np

def decode(index_0_8: int):  ###decoding the 0-8-square indexing
    x = 3 * (index_0_8 // 3)
    y = (index_0_8 - (3*(index_0_8//3))) * 3
    return x, y  ###returns the coordinations of the first cell of the square



class Sudoku:
    def __init__(self, sudoku_archive:str):
        a = pd.read_csv(filepath_or_buffer=sudoku_archive, header=None, keep_default_na=False, dtype="Int64")
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
            new_row_list = [i for i in row_list if i is not None]
            return new_row_list
        return row_list

    def get_column(self, column_index:int, get_none=False) -> list: #0-8
        column_list = self.sudoku.iloc[:, column_index].tolist()
        if not get_none:
            new_column_list = [i for i in column_list if i is not None]
            return new_column_list
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

    def decode_cell_from_square(self, index_of_square: int): #returns the coordinates where None cell exists on the dataframe
        x_initial, y_initial = decode(index_of_square)
        index_of_full_list = self.sudoku.get_square(x_initial, y_initial, get_none=True).index(None)
        x = x_initial + (index_of_full_list // 3)
        y = index_of_full_list - (3 * (index_of_full_list // 3)) + y_initial
        return x, y

    def quick_checker(self): #checks if any line, column, square exists with one value missing, making easy the search for other missing values to be found
        if len(set(self.square)) == 1:
            return -2 #sudoku solved
        if 8 in self.lines:
            return f"l{self.lines.index(8)}"
        if 8 in self.columns:
            return f"c{self.columns.index(8)}"
        if 8 in self.square:
            return f"s{self.square.index(8)}"
        return -1 #quick solver can't solve the puzzle



    def quick_solver(self, typ:str, index:int): #finds the missing values from quick checker


        def straight_replacement(l1:list, l2:list): ##replacement for lines and columns
            solution = -1
            for i in range(1,10):
                if i not in l1:
                    solution = i
                    break
            i = index
            other_i = l2.index(None)
            return i, other_i, solution


        if typ == "l":
            x, y, solution = straight_replacement(self.sudoku.get_row(index), self.sudoku.get_row(index, get_none=True))
            self.sudoku[x, y] = solution
            self.upgrade_grades(x,y)

        elif typ == "c":
            y,x,solution = straight_replacement(self.sudoku.get_column(index), self.sudoku.get_column(index, get_none=True))
            self.sudoku[x, y] = solution
            self.upgrade_grades(x,y)

        else:
            x_initial, y_initial = decode(index) #coord of the first element of the square
            x_index, y_index = self.decode_cell_from_square(index)
            solution = -1
            for i in range(1,10):
                if i not in self.sudoku.get_square(x_initial,y_initial):
                    solution = i
                    break
            self.sudoku[x_index, y_index] = solution
            self.upgrade_grades(x_index, y_index)

    def cls_check(self): ###checks taking into consideration columns, lines, square

        exact_copy = self.square.copy()
        z = [i for i in sorted(self.square.copy(), reverse=True) if i != 9]
        for max_square in z:

            x, y = decode(exact_copy.index(max_square))
            value_square_list = self.sudoku.get_square(x,y)
            x_index, y_index = self.decode_cell_from_square(exact_copy.index(max_square))
            exact_copy[exact_copy.index(max_square)] = -1
            current_column = self.sudoku.get_column(y_index)
            current_line = self.sudoku.get_row(x_index)
            super_set = set(current_column+current_line+value_square_list)
            if len(super_set) == 8:
                solution = -1
                for i in range(1,10):
                    if i not in super_set:
                        solution = i
                        break
                self.sudoku[x_index, y_index] = solution
                self.upgrade_grades(x_index, y_index)
                return 1 #found a solution
            else:
                continue
        return 0 #can't do anything else
