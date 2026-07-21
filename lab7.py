def is_safe(board, row, col):
    for prev_row in range(row):
        placed = board[prev_row]

        # Same column
        if placed == col:
            return False

        # Same diagonal
        if abs(prev_row - row) == abs(placed - col):
            return False

    return True


def solve_n_queens(n):
    board = [-1] * n
    solutions = []
    backtrack_count = [0]

    def backtrack(row):
        if row == n:
            solutions.append(board[:])
            return

        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                backtrack(row + 1)
                board[row] = -1  # Undo
                backtrack_count[0] += 1

    backtrack(0)

    return solutions, backtrack_count[0]


def display_board(solution, n):
    print(" +" + "---+" * n)

    for row in range(n):
        print(" |", end="")

        for col in range(n):
            if solution[row] == col:
                print(" Q |", end="")
            else:
                print(" . |", end="")

        print()
        print(" +" + "---+" * n)


# ---------------- Main Program ----------------

n = int(input("Enter the value of N: "))

solutions, backtracks = solve_n_queens(n)

print(f"\nN = {n}")
print(f"Total Solutions: {len(solutions)}")
print(f"Backtracking Count: {backtracks}")

choice = input("\nDo you want to display all solutions? (y/n): ")

if choice.lower() == "y":
    print(f"\nAll solutions for {n}-Queens:\n")

    for i, sol in enumerate(solutions, 1):
        print(f"Solution {i}: {sol}")
        display_board(sol, n)