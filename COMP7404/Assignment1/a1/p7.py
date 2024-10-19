import math
import sys, parse, grader

def better_board(problem):
    min_cost = math.inf
    x: int = 0
    y: int = 0

    for i in range(8):
        for j in range(8):
            row: list[int] = [0 for temp in range(8)]
            col: list[int] = [0 for temp in range(8)]
            ldiag: list[int] = [0 for temp in range(15)]
            rdiag: list[int] = [0 for temp in range(15)]

            attacks: int = 0
            for idx, queen in enumerate(problem):
                if idx == i:
                    queen = j
                attacks += row[queen]
                attacks += col[idx]
                attacks += ldiag[idx - queen + 7]
                attacks += rdiag[idx + queen]

                row[queen] += 1
                col[idx] += 1
                ldiag[idx - queen + 7] += 1
                rdiag[idx + queen] += 1

            if attacks < min_cost:
                x = j
                y = i
                min_cost = attacks

    problem[y] = x
    solution: str = ""
    for i in range(8):
        line: str = ""
        for j in range(8):
            if j != 0:
                line += " "
            if problem[j] == i:
                line += "q"
            else:
                line += "."
        solution += (line + "\n")

    return solution[:-1]

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 7
    grader.grade(problem_id, test_case_id, better_board, parse.read_8queens_search_problem)