"""
The data has been hard coded in the program, thus just click run.
However, if there is a demand of changing parameters, modifying variables in main() function is available.
The final policy calculated for each attempt will be printed in the terminal.

From the result, it's easy to find that most of the cells can get an optimal action, while the policy of starting
location often leads to a crash into a wall. It's possible that due to the discount and living reward are pretty
loose for wasting time crashing into walls, this kind of action may not lead the agent to further punishment.
Introducing extra discount can improve the result a lot according to my own experiment.
"""
import copy, random


class QLearning:
    """
    The main class of implementing Q Learning
    """
    def __init__(self, alpha, discount, noise, living_reward, grid, eps = 1e-6):
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
        self.epsilon = 0.7                 # Here is the epsilon for epsilon-greedy algorithm
        self.epsilon_decay = 1 - 1e-5      # Decay rate for epsilon
        self.alpha_decay = 1 - 1e-5        # Decay rate for alpha (learning rate)

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

        # the epsilon-greedy process
        if random.uniform(0, 1) < self.epsilon:
            available_actions = [action for action in self.actions]
            available_actions.remove(best_action)
            chosen_action = random.choice(available_actions)
        else:
            chosen_action = best_action

        # epsilon will decay every time the epsilon-greedy algorithm runs
        self.epsilon *= self.epsilon_decay
        return chosen_action

    def get_max_q(self, location):
        """
        Get the maximum Q value for the given location.

        :param location:  the location of the agent now
        :return:          the maximum Q value
        """
        if location in self.exit_states:
            return self.Q[location[0]][location[1]]["x"]

        return max(self.Q[location[0]][location[1]].values())

    def print_policy(self):
        """
        Print the current policy.

        :return: string containing the current policy
        """
        res = ""
        for i in range(self.n):
            for j in range(self.m):
                res += f"| {self.symbols[self.policy[i][j]]} |"
            res += "\n"
        res += "-----------------------\n"
        print(res[:-1])

    def next_location(self, agent, intended_direction):
        """
        Get the location where the given agent is after taking action.

        :param agent:               agent location now
        :param intended_direction:  the action agent should take
        :return:                    the location next
        """
        # The agent may not get the right location
        chosen_direction = random.choices(
            population=self.directions[intended_direction],
            weights=[1 - 2 * self.noise, self.noise, self.noise]
        )[0]

        x, y = agent[0] + self.actions[chosen_direction][0], agent[1] + self.actions[chosen_direction][1]

        if 0 <= x < self.n and 0 <= y < self.m and self.grid[x][y] != "#":
            return x, y
        return agent

    def check_complete(self, policy):
        """
        Check if the policy is identical to the previous one

        :param policy: new policy
        :return:       whether the policy is identical to the previous one
        """
        for i in range(self.n):
            for j in range(self.m):
                if policy[i][j] != self.policy[i][j]:
                    return False
        return True

    def get_new_policy(self, location, Q_cell):
        """
        Get the new policy for the given location according to new Q value.

        :param location:  the given location
        :param Q_cell:    new Q value
        :return:          new policy
        """
        # If the agent can only exit
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
        """
        The Q Learning Process

        :return: the optimal policy
        """
        iteration = 0
        complete = False
        # We need the Q Learning run enough times in order to get optimal policy
        while (not complete) or iteration < 5000:
            agent = self.start
            iteration += 1
            Q = copy.deepcopy(self.Q)
            policy = copy.deepcopy(self.policy)
            action = ""
            while action != "x":
                action = self.get_action(agent)
                new_agent = copy.deepcopy(agent)

                value = 0.0
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
            self.alpha *= self.alpha_decay

        return self.policy


def main():
    # BASIC DATA IN P3 CASE 2
    discount = 1
    noise = 0.1
    living_reward = -0.01
    grid = [
        ["_", "_", "_", "1"],
        ["_", "#", "_", "-1"],
        ["S", "_", "_", "_"],
    ]

    run_times = int(input("NUMBER OF ATTEMPT: "))
    for _ in range(run_times):
        instance = QLearning(0.01, discount, noise, living_reward, grid)
        instance.solve()
        print(f"ATTEMPT {_ + 1}: ")
        instance.print_policy()


if __name__ == "__main__":
    main()
