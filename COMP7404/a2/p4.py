import sys, parse, random, collections
import time, os, copy
from typing import Tuple, List


def better_play_multiple_ghosts(problem):
    directions = {
        "E": (0, 1),
        "N": (-1, 0),
        "S": (1, 0),
        "W": (0, -1)
    }
    EAT_FOOD_SCORE = 10
    PACMAN_EATEN_SCORE = -500
    PACMAN_WIN_SCORE = 500
    PACMAN_MOVING_SCORE = -1

    grid = problem["grid"]
    ghosts = problem["ghosts"]
    pacman = problem["pacman"]
    food = problem["food"]

    food_count = len(food)

    def manhattan_distance(position1, position2):
        """
        Calculate the manhattan distance between two position.

        :param position1:  The first position
        :param position2:  The second position

        :return:           The manhattan distance between
        """
        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])


    def bfs(s, current_target):
        """
        BFS to find the distance between the starting position to nearest target

        :param s:        the given starting position
        :param current_target:  the location of targets

        :return:         distance between the nearest target and starting position
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


    def get_possible_moves(position, is_ghost=False, current_ghosts=None):
        """
        Get actions the specific agent can take.
        If the agent is a ghost, we should consider of avoiding other ghosts

        :param position:        the agent's position
        :param is_ghost:        whether the agent is a ghost
        :param current_ghosts:  the position of ghosts

        :return:                actions the agent can take
        """
        possible_moves = []

        n = len(grid)
        m = len(grid[0])
        for action, (dx, dy) in directions.items():
            vx = position[0] + dx
            vy = position[1] + dy
            if 0 <= vx < n and 0 <= vy < m and grid[vx][vy] != '%':
                if (is_ghost and (vx, vy) not in current_ghosts) or (not is_ghost):
                    possible_moves.append(action)

        return possible_moves


    def move_item(original, d):
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


    def evaluate_state(current_pacman, current_ghosts, current_food, steps):
        """
        First, check the score of current state;
        then, we add the evaluation value if the game is not over.

        The reason of using BFS instead of manhattan distance here is
        the usage of manhattan distance caused a strange scenario like below:

        ...
        %%%
         P

        The evaluation using manhattan distance will let the PacMan keep crashing into the wall.
        So I choose BFS in order to prevent this situation.

        :param current_pacman:  The position of PacMan in this specific state
        :param current_ghosts:  The position of ghosts in this specific state
        :param current_food:    The position and the number of food in this specific state
        :param steps:           The number of steps PacMan has taken in this specific state

        :return:                The value of the evaluation function
        """
        score = steps * PACMAN_MOVING_SCORE
        if len(current_food) != food_count:
            score += EAT_FOOD_SCORE * (food_count - len(current_food))

            if not current_food:
                score += PACMAN_WIN_SCORE

        if current_pacman in current_ghosts:
            score += PACMAN_EATEN_SCORE

        if check_finish(current_pacman, current_food, current_ghosts):
            return score

        # Get the distance between pacman and the nearest food
        food_distance = bfs(current_pacman, current_food)
        # If pacman and a ghost are not even close to each other, then we just ignore the ghost
        if min([manhattan_distance(current_pacman, g) for g in current_ghosts]) >= 5:
            return score + 10 / (food_distance + 1)

        # If pacman and a ghost are close enough, we should take the ghost into consideration
        ghost_distance = min([manhattan_distance(current_pacman, g) for g in current_ghosts])
        # 10 for the EAT_FOOD_SCORE, and 11 for impacting the agent's decision more with the ghosts
        return score + 10 / (food_distance + 1) - 11 / (ghost_distance + 1)


    def check_finish(current_pacman, current_food, current_ghosts):
        """
        Check if the game is over at current state.

        :param current_pacman: The position of PacMan in this specific state
        :param current_ghosts: The position of ghosts in this specific state
        :param current_food:   The position and the number of food in this specific state

        :return:               Whether the game is over
        """
        if not current_food:
            return True

        if current_pacman in current_ghosts:
            return True

        return False


    def move_with_evaulation(x, y, steps) -> str:
        """
        Move the agent with evaluation function.

        :param x:     agent's position in axis-x
        :param y:     agent's position in axis-y
        :param steps: the number of steps agent has taken in this specific state
        :return:      the best (or at least one of the best) action the agent can take
        """
        n: int = len(grid)
        m: int = len(grid[0])
        res = []
        max_value = -float("inf")

        for direction, (dx, dy) in directions.items():
            vx = x + dx
            vy = y + dy
            if 0 <= vx < n and 0 <= vy < m and grid[vx][vy] != '%':
                score_now = evaluate_state((vx, vy), ghosts, food, steps)
                if score_now > max_value:
                    max_value = score_now
                    res = [direction]
                elif score_now == max_value:
                    res.append(direction)

        return random.choice(res)


    def print_map():
        """
        Generate the string of current map.

        :return: the map now
        """
        res = ""
        for x, line in enumerate(grid):
            out_line: str = ""
            for y, ch in enumerate(line):
                if (x, y) in ghosts:
                    out_line += "WXYZ"[ghosts.index((x, y))]
                elif (x, y) == pacman:
                    out_line += "P"
                elif (x, y) in food:
                    out_line += '.'
                else:
                    out_line += ch
            res += (out_line + "\n")

        return res


    res_solution = ""
    res_winner = ""

    seed = problem["seed"]
    res_solution += f"seed: {seed}\n"

    step: int = 0
    res_solution += f"{step}\n"
    res_solution += print_map()

    score = 0
    while True:
        # PacMan's Turn
        step += 1
        pacman_moves = move_with_evaulation(pacman[0], pacman[1], step)
        score -= 1
        if pacman_moves:
            next_step: str = random.choice(pacman_moves)
            pacman = move_item(pacman, next_step)
            res_solution += f"{step}: P moving {next_step}\n"

            if pacman in ghosts:
                res_solution += print_map()
                score -= 500
                res_solution += f"score: {score}\n"
                res_solution += "WIN: Ghost"
                res_winner = "Ghost"
                return res_solution, res_winner
            elif pacman in food:
                score += 10
                food.remove(pacman)
                res_solution += print_map()

                if not food:
                    score += 500
                    res_solution += f"score: {score}\n"
                    res_solution += "WIN: Pacman"
                    res_winner = "Pacman"
                    return res_solution, res_winner
                else:
                    res_solution += f"score: {score}\n"
            else:
                res_solution += print_map()
                res_solution += f"score: {score}\n"
        else:
            res_solution += f"{step}: P moving \n"
            res_solution += print_map()
            res_solution += f"score: {score}\n"

        # Ghost's Turn
        for idx, ghost in enumerate(ghosts):
            step += 1
            ghost_name = "WXYZ"[idx]
            ghost_moves = get_possible_moves(ghost, True, ghosts)

            if ghost_moves:
                next_step = random.choice(ghost_moves)
                res_solution += f"{step}: {ghost_name} moving {next_step}\n"
                ghosts[idx] = move_item(ghost, next_step)

                if pacman in ghosts:
                    score -= 500

                    res_solution += print_map()
                    res_solution += f"score: {score}\n"
                    res_solution += "WIN: Ghost"
                    res_winner = "Ghost"
                    return res_solution, res_winner

                res_solution += print_map()
                res_solution += f"score: {score}\n"
            else:
                res_solution += f"{step}: {ghost_name} moving \n"
                res_solution += print_map()
                res_solution += f"score: {score}\n"


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])    
    problem_id = 4
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
        solution, winner = better_play_multiple_ghosts(copy.deepcopy(problem))
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count/num_trials * 100
    end = time.time()
    print('time: ',end - start)
    print('win %',win_p)