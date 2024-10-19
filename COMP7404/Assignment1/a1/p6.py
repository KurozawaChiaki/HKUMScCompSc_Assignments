import sys, parse, grader

def number_of_attacks(problem):
    ans: list[list[int]] = [[0 for i in range(8)] for j in range(8)]

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
            ans[j][i] = attacks

    solution: str = ""
    for row in ans:
        line: str = ""
        for idx, value in enumerate(row):
            if value < 10:
                line += " "
            if idx != 0:
                line += " "
            line += str(value)
        solution += (line + "\n")

    return solution[:-1]

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 6
    grader.grade(problem_id, test_case_id, number_of_attacks, parse.read_8queens_search_problem)