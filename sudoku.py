import sys
from CSP import CSP
from copy import deepcopy


#############################################################################
# ac3() - algorithm for checking arc-consistency in csp data structure
# Return: boolean
#
def ac3(csp):
    queue = list(csp.C)
    print(f"Initial queue length: {len(queue)}")
    while len(queue) > 0:
        print(f"Current queue length: {len(queue)}")
        (x_i, x_j) = queue.pop(0)
        if revise(csp, x_i, x_j):
            if len(csp.D[csp.X.index(x_i)]) == 0 or len(csp.D[csp.X.index(x_j)]) == 0:
                print("AC-3 detected an inconsistency. Arc-consistency failed.")
                return False
            for x_k in csp.get_neighbors(x_i):
                if x_k != x_j:
                    queue.append((x_k, x_i))
            for x_k in csp.get_neighbors(x_j):
                if x_k != x_i:
                    queue.append((x_k, x_j))
    print("AC-3 completed successfully.")
    return True

#############################################################################
# revise() - update the domain of one variable by excluding the domain value
#            from the other variable
# Return: boolean
#
def revise(csp, x_i, x_j):
    revised = False
    d_i = csp.D[csp.X.index(x_i)]
    d_j = csp.D[csp.X.index(x_j)]
    if len(d_i) == 1 and d_i <= d_j:
        print(f"Revise: Reducing domain of {x_j} based on {x_i}. Before: {d_j}")
        d_j -= d_i
        csp.D[csp.X.index(x_j)] = d_j
        revised = True
    elif len(d_j) == 1 and d_j <= d_i:
        print(f"Revise: Reducing domain of {x_i} based on {x_j}. Before: {d_i}")
        d_i -= d_j
        csp.D[csp.X.index(x_i)] = d_i
        revised = True
    return revised

#############################################################################
# backtrack() - algorithm to search for solution and add to assignment
# Return: assignment or False
#
def backtrack(assignment, csp):
    if csp.is_complete(assignment):
        return assignment

    x = mrv(assignment, csp)
    csp_orig = deepcopy(csp)
    for v in list(csp.D[csp.X.index(x)]):  # Use a copy of the domain set
        inferences = {}
        if csp.is_consistent(x, v):
            assignment[x] = v
            inferences = forward_check(assignment, csp, x, v)
            if isinstance(inferences, dict):
                assignment.update(inferences)
                result = backtrack(assignment, csp)
                if isinstance(result, dict):
                    return result

        # Safely remove the variable from the assignment
        if x in assignment:
            del assignment[x]

        # Safely remove inferred variables from the assignment
        if isinstance(inferences, dict):
            for i in inferences:
                if i in assignment:
                    del assignment[i]

        # Restore the original CSP state
        csp = deepcopy(csp_orig)

    return False





#############################################################################
# mrv() - minimum-remaining-value (MRV) heuristic
# Return: the variable from amongst those that have the fewest legal values
#
def mrv(assignment, csp):
    unassigned_x = {}
    index = 0
    for d in csp.D:
        if len(d) > 1:
            unassigned_x[csp.X[index]] = len(d)
        index += 1
    sorted_unassigned_x = sorted(unassigned_x, key=unassigned_x.get)
    for x in sorted(unassigned_x, key=unassigned_x.get):
        if x not in assignment:
            return x
    return False

#############################################################################
# forward_check() - implement inference finding in the neighbor variables
# Return: dict of inferences
#
def forward_check(assignment, csp, x, v):
    inferences = {}
    neighbors = csp.get_neighbors(x)
    for n in neighbors:
        s = csp.D[csp.X.index(n)]
        if len(s) > 1 and v in s:
            s -= set([v])
            csp.D[csp.X.index(n)] = s
            if len(s) == 1 and n not in assignment:
                inferences[n] = list(s)[0]
        if len(s) == 0:
            return False
    return inferences

#############################################################################
# main() - sudoku solver main process
# Return: void
#
def main(filename):
    csp = CSP(filename)

    # Print the initial Sudoku board
    print("Initial Sudoku Board:")
    csp.print_game()

    # Check for arc-consistency using AC-3
    if ac3(csp):
        print("AC-3 succeeded. Checking if the board is solved.")
        if csp.is_solved():
            print("Sudoku Solved!")
            csp.print_game()
        else:
            print("The board is arc-consistent but not solved. Starting backtracking.")
            assignment = backtrack({}, csp)
            if isinstance(assignment, dict):
                csp.assign(assignment)
                print("Sudoku Solved with backtracking!")
                csp.print_game()
            else:
                print("Backtracking failed. No solution exists.")
    else:
        print("AC-3 failed. No solution exists.")

# Ensure this is called when running the script
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sudoku.py <input_file>")
    else:
        main(sys.argv[1])
