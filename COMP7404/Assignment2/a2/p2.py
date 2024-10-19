import collections
import functools
import sys, parse, random
import time, os, copy
from sys import maxsize

from p3 import print_map


def better_play_single_ghosts(problem):
    DIRECTIONS = {
        "E": (0, 1),
        "N": (-1, 0),
        "S": (1, 0),
        "W": (0, -1)
    }

    SEED = problem["seed"]
    GRID = problem["grid"]
    Ghosts = problem["ghosts"]
    PacMan = problem["pacman"]
    Food = problem["food"]
    Solution = ""
    Winner = ""

    def move_item(original, d: str):
        """
        Get the position of an agent take an action.

        :param original:  agent's original position
        :param d:         the action agent will take

        :return:          agent's position after the action
        """
        res = None
        if d == "E":
            res = (original[0], original[1] + 1)
        elif d == "N":
            res = (original[0] - 1, original[1])
        elif d == "S":
            res = (original[0] + 1, original[1])
        elif d == "W":
            res = (original[0], original[1] - 1)

        return res

    def get_possible_moves(position, ghost=False, ghosts=None):
        """
        Get actions the specific agent can take.
        If the agent is a ghost, we should consider of avoiding other ghosts

        :param position:        the agent's position
        :param is_ghost:        whether the agent is a ghost
        :param current_ghosts:  the position of ghosts

        :return:                actions the agent can take
        """
        direction = []

        if position[1] != len(GRID[0]) - 1 and GRID[position[0]][position[1] + 1] != '%':
            direction.append("E")
        if position[0] != 0 and GRID[position[0] - 1][position[1]] != '%':
            direction.append("N")
        if position[0] != len(GRID) - 1 and GRID[position[0] + 1][position[1]] != '%':
            direction.append("S")
        if position[1] != 0 and GRID[position[0]][position[1] - 1] != '%':
            direction.append("W")

        if ghost:
            res = [d for d in direction if move_item(position, d) not in ghosts]
            direction = res

        return direction

    def bfs(s, current_target):
        """
        BFS to find the distance between the starting position to nearest target

        :param s:              the given starting position
        :param current_target: the location of targets

        :return:               distance between the nearest target and starting position
        """
        queue = collections.deque()
        visited = {s}
        queue.append((s, 0))
        while queue:
            u = queue.popleft()
            if u[0] in current_target:
                return u[1]

            for direction in get_possible_moves(u[0]):
                (nr, nc) = move_item(u[0], direction)
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), u[1] + 1))

        return None


    def evaluation_function(pacman_x, pacman_y, ghost_x, ghost_y, food):
        """
        The reason of using BFS instead of manhattan distance here is
        the usage of manhattan distance caused a strange scenario like below:

        ...
        %%%
         P

        The evaluation using manhattan distance will let the PacMan keep crashing into the wall.
        So I choose BFS in order to prevent this situation.

        :param pacman_x:  pacman's position in x-axis
        :param pacman_y:  pacman's position in y-axis
        :param ghost_x:   ghost's position in x-axis
        :param ghost_y:   ghost's position in y-axis
        :param food:      the position of food

        :return:          the value of the evaluation function
        """
        food_distance = bfs((pacman_x, pacman_y), food)
        ghost_distance = bfs((pacman_x, pacman_y), [(ghost_x, ghost_y)])
        return 10 / (food_distance + 1) - 11 / (ghost_distance + 1)

    def MoveRandomly(layout, x, y) -> str:
        """
        Get the random action for agent

        :param layout:  the map of the game now
        :param x:       the position of agent in x-axis
        :param y:       the position of agent in y-axis
        :return:        the random action
        """
        n: int = len(layout)
        m: int = len(layout[0])

        res = []
        for direction, (dx, dy) in DIRECTIONS.items():
            vx = x + dx
            vy = y + dy
            if 0 <= vx < n and 0 <= vy < m and layout[vx][vy] != '%':
                res.append(direction)

        return random.choice(res)


    def move_with_evaulation(x, y) -> str:
        """
        Get the best action for agent
        :param x:  the position of agent in x-axis
        :param y:  the position of agent in y-axis
        :return:   the best action (or at least one of the best)
        """
        n: int = len(GRID)
        m: int = len(GRID[0])
        res = []
        max_value = -float("inf")

        for direction, (dx, dy) in DIRECTIONS.items():
            vx = x + dx
            vy = y + dy
            if 0 <= vx < n and 0 <= vy < m and GRID[vx][vy] != '%':
                score_now = evaluation_function(vx, vy, Ghosts[0][0], Ghosts[0][1], Food)
                if score_now > max_value:
                    max_value = score_now
                    res = [direction]
                elif score_now == max_value:
                    res.append(direction)

        return random.choice(res)

    def PrintMap() -> str:
        res: str = ""
        for x, line in enumerate(GRID):
            out_line: str = ""
            for y, ch in enumerate(line):
                if (x, y) == Ghosts[0]:
                    out_line += "W"
                elif (x, y) == PacMan:
                    out_line += "P"
                elif (x, y) in Food:
                    out_line += '.'
                else:
                    out_line += ch
            res += (out_line + "\n")

        return res


    step = 0
    Solution += f"seed: {SEED}\n"
    Solution += f"{step}\n"
    Solution += PrintMap()

    score = 0
    while True:
        # PacMan's Turn
        step += 1
        score -= 1
        PacManMove = move_with_evaulation(PacMan[0], PacMan[1])
        dx, dy = DIRECTIONS[PacManMove]
        PacMan = (PacMan[0] + dx, PacMan[1] + dy)
        Solution += f"{step}: P moving {PacManMove}\n"

        if PacMan in Food:
            Food.remove(PacMan)
            score += 10
            Solution += PrintMap()

            if not Food:
                score += 500

                Solution += f"score: {score}\n"
                Solution += "WIN: Pacman"
                Winner = "Pacman"

                return Solution, Winner
            else:
                Solution += f"score: {score}\n"
        else:
            Solution += PrintMap()
            Solution += f"score: {score}\n"

        # Ghost's Turn
        step += 1
        GhostMove = MoveRandomly(GRID, Ghosts[0][0], Ghosts[0][1])
        dx, dy = DIRECTIONS[GhostMove]
        Ghosts[0] = (Ghosts[0][0] + dx, Ghosts[0][1] + dy)
        Solution += f"{step}: W moving {PacManMove}\n"

        if PacMan in Ghosts:
            score -= 500

            Solution += PrintMap()
            Solution += f"score: {score}\n"
            Solution += "WIN: Ghost"
            Winner = "Ghost"

            return Solution, Winner

        Solution += PrintMap()
        Solution += f"score: {score}\n"


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 2
    file_name_problem = str(test_case_id)+'.prob' 
    file_name_sol = str(test_case_id)+'.sol'
    path = os.path.join('test_cases','p'+str(problem_id)) 
    problem = parse.read_layout_problem(os.path.join(path,file_name_problem))
    num_trials = int(sys.argv[2])
    verbose = bool(int(sys.argv[3]))
    print('test_case_id:',test_case_id)
    print('num_trials:',num_trials)
    print('verbose:',verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = better_play_single_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)