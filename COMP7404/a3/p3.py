import sys, grader, parse
import copy

def value_iteration(problem):
    discount = problem["discount"]
    living_reward = problem["livingReward"]
    noise = problem["noise"]
    iterations = problem["iterations"]
    grid = problem["grid"]

    d_offset = {
        "E": (0, 1),
        "S": (1, 0),
        "W": (0, -1),
        "N": (-1, 0)
    }
    directions = {'N': ['E', 'W'], 'E': ['S', 'N'], 'S': ['W', 'E'], 'W': ['N', 'S']}
    actions = ["N", "E", "S", "W"]

    def next_location(agent, action):
        x = agent[0] + d_offset[action][0]
        y = agent[1] + d_offset[action][1]

        if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
            if grid[x][y] != "#":
                return x, y
            elif grid[x][y] == "#":
                return agent

        if x < 0:
            x = 0
        if x >= len(grid):
            x = len(grid) - 1

        if y < 0:
            y = 0
        if y >= len(grid[0]):
            y = len(grid[0]) - 1

        return x, y

    v = []
    p = []
    for i, line in enumerate(grid):
        line_cell = []
        line_p = []
        for j, cell in enumerate(line):
            if cell == "#":
                line_cell.append(float("inf"))
                line_p.append("#")
            else:
                line_cell.append(0.0)
                line_p.append("x")
        v.append(line_cell)
        p.append(line_p)

    res = "V_k=0\n"
    for i, line in enumerate(v):
        for j, cell in enumerate(line):
            if cell == float("inf"):
                res += "| ##### |"
            else:
                res += "|{:7.2f}|".format(cell)
        res += "\n"

    for _ in range(iterations - 1):
        new_v = copy.deepcopy(v)
        new_p = copy.deepcopy(p)
        for i, line in enumerate(grid):
            for j, cell in enumerate(line):
                if cell == "#":
                    new_v[i][j] = float("inf")
                    new_p[i][j] = "#"
                    continue

                if cell != "_" and cell != "S" and cell != "#":
                    new_v[i][j] = float(cell)
                    new_p[i][j] = "x"
                    continue

                new_v[i][j] = -float("inf")
                for action in actions:
                    x, y = next_location((i, j), action)
                    new_value = (v[x][y] * discount + living_reward) * (1 - (2 * noise))
                    for unintended in directions[action]:
                        x, y = next_location((i, j), unintended)
                        new_value += (v[x][y] * discount + living_reward) * noise

                    if new_value > new_v[i][j]:
                        new_v[i][j] = new_value
                        new_p[i][j] = action

        v = new_v
        p = new_p
        res += f"V_k={_ + 1}\n"
        for i, line in enumerate(v):
            for j, cell in enumerate(line):
                if cell == float("inf"):
                    res += "| ##### |"
                else:
                    res += "|{:7.2f}|".format(cell)
            res += "\n"
        res += f"pi_k={_ + 1}\n"
        for i, line in enumerate(p):
            for j, cell in enumerate(line):
                res += f"| {cell} |"
            res += "\n"

    return res[:-1]

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -4
    problem_id = 3
    grader.grade(problem_id, test_case_id, value_iteration, parse.read_grid_mdp_problem_p3)