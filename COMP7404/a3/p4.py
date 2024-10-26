"""
The data has been hard coded in the program, thus just click run.
However, if there is a demand of changing parameters, modifying variables in main() function is available.
The policy calculated in each iteration will be printed in the terminal.
"""
import copy, random


class QLearning:
    """
    The main class of implementing Q Learning
    """
    def __init__(self, alpha, discount, noise, living_reward, grid, eps=1e-6):
        """
        Initialization of the instance

        :param alpha:            Learning rate
        :param discount:         Discount factor, which is the lambda in slides
        :param noise:            Possibility of unintended moves (not for the epsilon-greedy!)
        :param living_reward:    Living reward
        :param grid:             Map of the game
        :param eps:              seems to be useless, but maybe someday I need it to compare floats
        """
        self.alpha = alpha
        self.discount = discount
        self.noise = noise
        self.living_reward = living_reward
        self.grid = grid
        self.eps = eps
        self.actions = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}
        self.directions = {'N': ['N', 'E', 'W'], 'E': ['E', 'S', 'N'], 'S': ['S', 'W', 'E'], 'W': ['W', 'N', 'S']}
        self.n = len(grid)
        self.m = len(grid[0])
        self.Q = [[{"N": 0.0, "E": 0.0, "S": 0.0, "W": 0.0, "x": 0.0} for _ in range(self.m)] for _ in range(self.n)]
        self.policy = [[" " for _ in range(self.m)] for _ in range(self.n)]
        self.start = (0, 0)
        self.exit_states = []
        self.symbols = {
            "N": "↑", "E": "→", "W": "←", "S": "↓",
            "x": "x", "#": "#", " ": " "
         }
        self.epsilon = 0.6              # Here is the epsilon for epsilon-greedy algorithm
        self.epsilon_decay = 0.995      # Decay rate for epsilon
        self.alpha_decay = 0.995        # Decay rate for alpha (learning rate)

        # Initialize important parameters
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
        """
        Get the action for agent in iteration.

        :param location:  the location of the agent now
        :return:          the action agent should take next
        """
        if location in self.exit_states:
            return "x"

        # choose the "best" action according to Q values
        best_action = self.get_new_policy(location, self.Q[location[0]][location[1]])

        if random.uniform(0, 1) < self.epsilon:
            available_actions = [action for action in self.actions]
            chosen_action = random.choice(available_actions)
        else:
            chosen_action = best_action

        self.epsilon *= self.epsilon_decay
        return chosen_action

    def get_max_q(self, location):
        return max(self.Q[location[0]][location[1]].values())

    def print_policy(self):
        res = ""
        for i in range(self.n):
            for j in range(self.m):
                res += f"| {self.symbols[self.policy[i][j]]} |"
            res += "\n"
        res += "-----------------------\n"
        print(res[:-1])

    def next_location(self, agent, intended_direction):
        chosen_direction = random.choices(
            population=self.directions[intended_direction],
            weights=[1 - 2 * self.noise, self.noise, self.noise]
        )[0]

        x, y = agent[0] + self.actions[chosen_direction][0], agent[1] + self.actions[chosen_direction][1]

        if 0 <= x < self.n and 0 <= y < self.m and self.grid[x][y] != "#":
            return x, y
        return agent

    def check_complete(self, policy):
        for i in range(self.n):
            for j in range(self.m):
                if policy[i][j] != self.policy[i][j]:
                    return False
        return True

    def get_new_policy(self, location, Q_cell):
        if self.policy[location[0]][location[1]] == "x":
            return "x"

        best_action = ""
        max_q = -float("inf")
        for action, value in Q_cell.items():
            if action == "x":
                continue
            if value > max_q:
                best_action = action
                max_q = value

        return best_action

    def solve(self):
        iteration = 0
        complete = False
        while (not complete) or iteration < 1000:
            agent = self.start
            iteration += 1
            Q = copy.deepcopy(self.Q)
            policy = copy.deepcopy(self.policy)
            action = ""
            while action != "x":
                print(f"{action} {agent}")
                action = self.get_action(agent)
                value = 0.0
                new_agent = copy.deepcopy(agent)
                if action == "x":
                    value += int(self.grid[agent[0]][agent[1]])
                else:
                    value += self.living_reward
                    next_location = self.next_location(agent, action)
                    value += self.discount * self.get_max_q(next_location)
                    new_agent = next_location

                Q[agent[0]][agent[1]][action] = ((1 - self.alpha) * self.Q[agent[0]][agent[1]][action]
                                                 + self.alpha * value)
                policy[agent[0]][agent[1]] = self.get_new_policy(agent, Q[agent[0]][agent[1]])
                agent = new_agent
                self.Q = Q

            complete = self.check_complete(policy)
            self.policy = policy
            self.print_policy()
            self.alpha *= self.alpha_decay


def main():
    discount = 1
    noise = 0.1
    living_reward = -0.01
    grid = [
        ["_", "_", "_", "1"],
        ["_", "#", "_", "-1"],
        ["S", "_", "_", "_"],
    ]
    instance = QLearning(0.01, discount, noise, living_reward, grid)
    instance.solve()


if __name__ == "__main__":
    main()
