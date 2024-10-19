import os, sys
from typing import List, Tuple


def read_layout_problem(file_path):
    file: List[str] = []
    with open(file_path, 'r') as f:
        file = f.readlines()

    res: dict = {
        "seed": int(file[0].replace("seed: ", "")),
        "grid": [],
        "pacman": None,
        "ghosts": [],
        "food": []
    }

    ghosts = {}

    for x, line in enumerate(file[1:]):
        row = []
        for y, ch in enumerate(line):
            if ch == '%' or ch == ' ':
                row.append(ch)
            elif ch == '\n':
                break
            else:
                row.append(' ')
                if ch in "WXYZ":
                    ghosts[ch] = (x, y)
                elif ch == 'P':
                    res["pacman"] = (x, y)
                elif ch == '.':
                    res["food"].append((x, y))
        res["grid"].append(row)

    for ghost in sorted(ghosts.keys()):
        res['ghosts'].append(ghosts[ghost])

    return res

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        problem = read_layout_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')