import sys, grader, parse
import random

def play_episode(problem):
    ran_seed = problem["seed"]
    if ran_seed != -1:
        random.seed(ran_seed, version = 1)

    noise = problem["noise"]
    directions = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}
    d_offset = {
        "E": (0, 1),
        "S": (1, 0),
        "W": (0, -1),
        "N": (-1, 0)
    }

    grid = problem["grid"]
    policy = problem["policy"]
    living_reward = problem["livingReward"]


    def get_start_state():
        for i, line in enumerate(grid):
            for j, content in enumerate(line):
                if content == "S":
                    return i, j


    def get_next_action(intend):
        return random.choices(population = directions[intend], weights = [1 - noise * 2, noise, noise])[0]


    def print_map(agent):
        res = ""
        for i, line in enumerate(grid):
            for j, content in enumerate(line):
                if (i, j) == agent:
                    res += "{:>5}".format("P")
                else:
                    res += "{:>5}".format(grid[i][j])
            res += "\n"
        return res


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

    def format_float(num, eps=1e-6):
        least_decimal = 1
        base = 10 ** least_decimal
        is_neg = bool(num < eps)
        num = -num if is_neg else num  # convert to positive
        while abs(float(num * base) - round(num * base)) > eps:
            least_decimal += 1
            base *= 10
        num = -num if is_neg else num  # convert to positive
        ret_str = f"{num:.{least_decimal}f}"
        return ret_str


    experience = ""
    agent_location = get_start_state()
    reward = 0.0
    experience += "Start state:\n"
    experience += print_map(agent_location)
    experience += f"Cumulative reward sum: {reward}\n-------------------------------------------- \n"

    while True:
        if policy[agent_location[0]][agent_location[1]] == "exit":
            exit_reward = int(grid[agent_location[0]][agent_location[1]])
            reward += exit_reward
            agent_location = (-1, -1)
            experience += "Taking action: exit (intended: exit)\n"
            experience += f"Reward received: {format_float(exit_reward)}\n"
            experience += "New state:\n"
            experience += print_map(agent_location)
            experience += f"Cumulative reward sum: {format_float(reward)}"
            break

        intended = policy[agent_location[0]][agent_location[1]]
        next_action = get_next_action(intended)
        agent_location = next_location(agent_location, next_action)
        reward += living_reward
        experience += f"Taking action: {next_action} (intended: {intended})\n"
        experience += f"Reward received: {format_float(living_reward)}\n"
        experience += "New state:\n"
        experience += print_map(agent_location)
        experience += f"Cumulative reward sum: {format_float(reward)}\n-------------------------------------------- \n"

    return experience

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    #test_case_id = 1
    problem_id = 1
    grader.grade(problem_id, test_case_id, play_episode, parse.read_grid_mdp_problem_p1)