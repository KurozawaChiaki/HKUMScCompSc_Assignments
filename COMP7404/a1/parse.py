import os, sys
from fileinput import close


def read_graph_search_problem(file_path):
    file: list[str] = []
    with open(file_path, 'r') as f:
        file = f.readlines()

    s: str = file[0]
    s = s.replace("start_state: ", "", 1).replace("\n", "")

    goal: str = file[1]
    goal = goal.replace("goal_states: ", "", 1)
    goals: list[str] = [x for x in goal.replace("\n", "").split(" ")]

    h: dict[str, int] = {}
    i = 2
    while i < len(file):
        param: list[str] = [x for x in file[i].replace("\n", "").split(" ")]
        d: str = param[0]
        if d in h:
            break

        h[d] = int(param[1])
        i += 1

    edges: dict[str, list[tuple[str, float]]] = {}
    while i < len(file):
        params: list[str] = [x for x in file[i].replace("\n", "").split(" ")]
        u = params[0]
        v = params[1]
        dis = float(params[2])
        if u not in edges:
            edges[u] = []

        edges[u].append((v, dis))
        i += 1

    p = (s, goals, h, edges)

    return p

def read_8queens_search_problem(file_path):
    file: list[str] = []
    with open(file_path, 'r') as f:
        file = f.readlines()
    p: list[int] = [-1, -1, -1, -1, -1, -1, -1, -1]
    for idx, line in enumerate(file):
        row: list[str] = [x for x in line.replace("\n", "").split(" ")]
        for i in range(len(row)):
            if row[i] == "q":
                p[i] = idx

    return p

if __name__ == "__main__":
    if len(sys.argv) == 3:
        problem_id, test_case_id = sys.argv[1], sys.argv[2]
        if int(problem_id) <= 5:
            problem = read_graph_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        else:
            problem = read_8queens_search_problem(os.path.join('test_cases','p'+problem_id, test_case_id+'.prob'))
        print(problem)
    else:
        print('Error: I need exactly 2 arguments!')