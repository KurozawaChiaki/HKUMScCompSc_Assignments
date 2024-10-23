import sys, grader, parse
import copy

def policy_evaluation(problem):
    discount = problem["discount"]
    living_reward = problem["livingReward"]
    noise = problem["noise"]
    iterations = problem["iterations"]
    grid = problem["grid"]
    policy = problem["policy"]

    d_offset = {
        "E": (0, 1),
        "S": (1, 0),
        "W": (0, -1),
        "N": (-1, 0)
    }
    directions = {'N': ['E', 'W'], 'E': ['S', 'N'], 'S': ['W', 'E'], 'W': ['N', 'S']}

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
    for i, line in enumerate(grid):
        line_cell = []
        for j, cell in enumerate(line):
            if cell == "#":
                line_cell.append(float("inf"))
            else:
                line_cell.append(0.0)
        v.append(line_cell)

    res = "V^pi_k=0\n"
    for i, line in enumerate(v):
        for j, cell in enumerate(line):
            if cell == float("inf"):
                res += "| ##### |"
            else:
                res += "|{:7.2f}|".format(cell)
        res += "\n"

    for _ in range(iterations - 1):
        new_v = copy.deepcopy(v)
        for i, line in enumerate(policy):
            for j, cell in enumerate(line):
                if cell == "#":
                    new_v[i][j] = float("inf")
                    continue
                action = cell
                if action == "exit":
                    new_v[i][j] = float(grid[i][j])
                else:
                    x, y = next_location((i, j), action)
                    new_v[i][j] = (v[x][y] * discount + living_reward) * (1 - (2 * noise))
                    for unintended in directions[action]:
                        x, y = next_location((i, j), unintended)
                        new_v[i][j] += (v[x][y] * discount + living_reward) * noise

        v = new_v
        res += f"V^pi_k={_ + 1}\n"
        for i, line in enumerate(v):
            for j, cell in enumerate(line):
                if cell == float("inf"):
                    res += "| ##### |"
                else:
                    res += "|{:7.2f}|".format(cell)
            res += "\n"

    return res[:-1]


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = -7
    problem_id = 2
    grader.grade(problem_id, test_case_id, policy_evaluation, parse.read_grid_mdp_problem_p2)