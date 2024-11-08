# Purpose: A data structure to represent constraint satisfaction problems
#          which consists of three components: variables, domain, constraints
import sys
import re

var_char = ['A','B','C','D','E','F','G','H','I']

class CSP:

    def __init__(self,filename):
        self.X = []
        self.D = []
        self.C = []
        self.init(filename)

    #########################################################################
    # init() - initialization of adding all values for variables, domains.
    # Return: void
    #
    def init(self, filename):
        for i in range(9):
            for j in range(1, 10):
                var = var_char[i] + str(j)
                self.X.append(var)
                domain = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
                self.D.append(domain)

        gamelist = []
        try:
            for line in open(filename):
                if len(line) != 10:
                    print("Error: file format invalid")
                    sys.exit(1)
                gamelist += list(line.rstrip())
        except IOError as e:
            print("Error: file cannot be opened")
            sys.exit(1)

        for i in range(len(gamelist)):
            if re.match(r"\d+", gamelist[i]):
                value = int(gamelist[i])
                if value == 0:
                    # Empty cell, use full domain {1-9}
                    self.D[i] = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
                else:
                    # Pre-filled cell, set domain to the single value
                    self.D[i] = set([value])
        
        self.set_constraints()


    #########################################################################
    # set_constraints() - setting all variables for arc-consistency(row,col).
    # Return: void
    #
    def set_constraints(self):
        for x in self.X:
            for y in self.X:
                if((x[0] == y[0] and x[1] != y[1]) or (x[1] == y[1] and x[0] != y[0])):
                    flag = True
                    for c in self.C:
                        if(x in c and y in c):
                            flag = False
                    if(flag):
                        self.C.append(set([x,y]))

        for a in [0,3,6]:
            for b in [0,3,6]:
                self.set_cube_constraints(a,b)

    #########################################################################
    # set_cube_constraints() - setting variables for arc-consistency(cube).
    # Return: void
    #
    def set_cube_constraints(self,a,b):
        cubelist = []
        for i in range(a,a+3):
            for j in range(b,b+3):
                x = var_char[i]+str(j+1)
                cubelist.append(x)
        for x in cubelist:
            for y in cubelist:
                if(x[0] != y[0] or x[1] != y[1]):
                    flag = True
                    for c in self.C:
                        if(x in c and y in c):
                            flag = False
                    if(flag):
                        self.C.append(set([x,y]))

    #########################################################################
    # get_neighbors() - find all connected variables(row,col,cube).
    # Return: list of neighbor variables
    #
    def get_neighbors(self, x):
        index = self.X.index(x)
        row = index // 9
        col = index % 9
        neighbors = []
        for i in range(1, 10):
            var_row = var_char[row] + str(i)
            var_col = var_char[i - 1] + str(col + 1)
            if i != col + 1:
                neighbors.append(var_row)
            if i != row + 1:
                neighbors.append(var_col)
        a = (row // 3) * 3
        b = (col // 3) * 3
        for i in range(a, a + 3):
            for j in range(b, b + 3):
                y = var_char[i] + str(j + 1)
                if y != x and y not in neighbors:
                    neighbors.append(y)
        return neighbors


    #########################################################################
    # is_complete() - check if assignment has complete assigned all domains.
    # Return: boolean
    #
    def is_complete(self,assignment):
        index = 0
        for d in self.D:
            if(len(d)>1 and self.X[index] not in assignment):
                return False
            index += 1
        return True

    #########################################################################
    # is_consistent() - check if selected value consistent with assignment.
    # Return: boolean
    #
    def is_consistent(csp, x, v):
        # Check row consistency
        row = x[0]
        for col in range(1, 10):
            neighbor = row + str(col)
            if neighbor != x and v in csp.D[csp.X.index(neighbor)] and len(csp.D[csp.X.index(neighbor)]) == 1:
                return False

        # Check column consistency
        col = x[1]
        for r in var_char:
            neighbor = r + col
            if neighbor != x and v in csp.D[csp.X.index(neighbor)] and len(csp.D[csp.X.index(neighbor)]) == 1:
                return False

        # Check block consistency
        row_block = (var_char.index(row) // 3) * 3
        col_block = (int(col) - 1) // 3 * 3
        for i in range(row_block, row_block + 3):
            for j in range(col_block, col_block + 3):
                neighbor = var_char[i] + str(j + 1)
                if neighbor != x and v in csp.D[csp.X.index(neighbor)] and len(csp.D[csp.X.index(neighbor)]) == 1:
                    return False

        return True





    #########################################################################
    # print_game() - pretty print the sudoku game board to standard output.
    # Return: void 
    #
    def print_game(self):
        count = 0
        for d in self.D:
            if len(d) == 1:
                # Get the only element from the set
                value = list(d)[0]
            else:
                # If the domain is empty or has multiple values, it's an error
                value = "?"
            sys.stdout.write(str(value))
            count += 1
            if (count % 9) == 0:
                print("")


    #########################################################################
    # is_solved() - check if all variables' domain has been assigned.
    # Return: boolean
    #
    def is_solved(self):
        solved = True
        for d in self.D:
            if(len(d)>1):
                solved = False
        return solved

    #########################################################################
    # assign() - apply the assignment to the csp's domains.
    # Return: void
    #
    def assign(self,assignment):
        for x in assignment:
            self.D[self.X.index(x)] = set([assignment[x]])