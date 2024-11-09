from collections import deque

# Helper function to read Sudoku from a file
def read_puzzle(file_path):
    with open(file_path, 'r') as f:
        return [[int(num) for num in line.split()] for line in f]

# Helper function to print Sudoku grid
def print_board(board):
    for row in board:
        print(" ".join(str(num) if num != 0 else '.' for num in row))
    print()

# Get all peers for a given cell (row, col)
def get_peers(row, col):
    peers = set()
    for i in range(9):
        peers.add((row, i))  # Same row
        peers.add((i, col))  # Same column
    # Same 3x3 box
    box_row, box_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(box_row, box_row + 3):
        for j in range(box_col, box_col + 3):
            peers.add((i, j))
    peers.discard((row, col))  # Remove the cell itself
    return peers

# Function to check if a value can be placed in a cell without conflicts
def is_consistent(board, row, col, val):
    for peer_row, peer_col in get_peers(row, col):
        if board[peer_row][peer_col] == val:
            return False
    return True

# AC-3 algorithm implementation with queue length reporting
def ac3(board):
    queue = deque([(row, col, peer) for row in range(9) for col in range(9) if board[row][col] == 0 
                   for peer in get_peers(row, col)])

    while queue:
        print(f"Queue length: {len(queue)}")  # Print the length of the queue at each step
        row, col, (peer_row, peer_col) = queue.popleft()
        if revise(board, row, col, peer_row, peer_col):
            if not any(board[row][col] == 0 for _ in range(9)):  # No valid domain
                return False
            for peer in get_peers(row, col):
                queue.append((row, col, peer))
    return True

# Revise function to enforce arc-consistency
def revise(board, row, col, peer_row, peer_col):
    revised = False
    for val in range(1, 10):
        if board[row][col] == val and not is_consistent(board, peer_row, peer_col, val):
            board[row][col] = 0
            revised = True
    return revised

# Function to find an empty cell
def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

# Backtracking algorithm to solve Sudoku if AC-3 doesn't fully solve
def backtrack(board):
    empty = find_empty(board)
    if not empty:
        return True  # No empty cells left, puzzle solved
    row, col = empty

    for num in range(1, 10):
        if is_consistent(board, row, col, num):
            board[row][col] = num
            if backtrack(board):
                return True
            board[row][col] = 0  # Undo assignment
    return False

# Solve function
def solve_sudoku(file_path):
    board = read_puzzle(file_path)
    print("Original Sudoku:")
    print_board(board)

    if ac3(board):
        print("Sudoku after AC-3:")
        print_board(board)
        if find_empty(board):
            print("AC-3 did not completely solve the puzzle. Applying backtracking...")
            if not backtrack(board):
                print("No solution exists.")
        else:
            print("Solved using AC-3!")
    else:
        print("AC-3 failed to achieve arc-consistency.")
    print("Final Solution:")
    print_board(board)

# Example usage
solve_sudoku('sudoku.txt')
