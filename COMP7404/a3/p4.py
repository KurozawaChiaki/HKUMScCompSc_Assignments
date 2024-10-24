"""
discount: 1
noise: 0.1
livingReward: -0.01
grid:
    _    _    _    1
    _    #    _   -1
    S    _    _    _
"""
import copy, random


class QLearning:
    def __init__(self, alpha, discount, noise, living_reward, grid, eps = 1e-6):
        self.alpha = alpha
        self.discount = discount
        self.noise = noise
        self.living_reward = living_reward
        self.grid = grid
        self.eps = eps
        self.actions = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}
        self.directions = {'N':['N', 'E', 'W'], 'E':['E', 'S', 'N'], 'S':['S', 'W', 'E'], 'W':['W', 'N', 'S']}
        self.n = len(grid)
        self.m = len(grid[0])
        self.Q = [[{"N": 0.0, "E": 0.0, "S": 0.0, "W": 0.0, "x": 0.0} for _ in range(self.m)] for _ in range(self.n)]
        self.policy = [[" " for _ in range(self.m)] for _ in range(self.n)]
        self.start = (0, 0)
        self.exit_states = []

        for i in range(self.n):
            for j in range(self.m):
                if grid[i][j] == '#':
                    self.policy[i][j] = "#"
                elif grid[i][j] == 'S':
                    self.start = (i, j)
                elif grid[i][j] != "_":
                    self.exit_states.append((i, j))
                    self.policy[i][j] = "x"


    def get_action(self, location):
        if location in self.exit_states:
            return "x"

        if self.policy[location[0]][location[1]] != "":
            return random.choices(population = self.directions[self.policy[location[0]][location[1]]],
                                 weights = [1 - self.noise * 2, self.noise, self.noise])[0]

        return random.choice(list(self.actions.keys()))


    def get_max_q(self, location):
        return max(self.Q[location[0]][location[1]].values())


    def next_location(self, agent, d):
        x = agent[0] + self.actions[d][0]
        y = agent[1] + self.actions[d][1]

        if 0 <= x < self.n and 0 <= y < self.m:
            if self.grid[x][y] != "#":
                return x, y
            elif self.grid[x][y] == "#":
                return agent

        if x < 0:
            x = 0
        if x >= self.n:
            x = self.n - 1

        if y < 0:
            y = 0
        if y >= self.m:
            y = self.m - 1

        return x, y


    def get_new_policy(self, location):
        best_action = ""
        max_q = -float("inf")
        for action, value in self.Q[location[0]][location[1]].items():
            if value > max_q:
                best_action = action
                max_q = value

        return best_action


    def solve(self):
        iteration = 0
        delta = float("inf")
        while delta > self.eps:
            delta = 0.0
            agent = self.start
            iteration += 1
            Q = copy.deepcopy(self.Q)
            policy = copy.deepcopy(self.policy)
            action = ""
            while action != "x":
                action = self.get_action(agent)
                value = 0.0
                if action == "x":
                    value += int(self.grid[agent[0]][agent[1]])
                else:
                    value += self.living_reward
                    next_location = self.next_location(agent, action)
                    value += self.discount * self.get_max_q(next_location)

                Q[agent[0]][agent[1]][action] = (1 - self.alpha) * self.Q[agent[0]][agent[1]][action] + self.alpha * value
                policy[agent[0]][agent[1]] = self.get_new_policy(agent)
                delta += abs(self.Q[agent[0]][agent[1]][action] - Q[agent[0]][agent[1]][action])
                self.Q = Q
                self.policy = policy
                print(policy)


def main():
    

if __name__ == "__main__":
    main()