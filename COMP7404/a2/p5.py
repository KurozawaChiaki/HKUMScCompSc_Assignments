import collections
import math
import sys, parse
import time, os, copy


def min_max_multiple_ghosts(problem, k):
    pacman = problem["pacman"]
    ghosts = problem["ghosts"]
    food = problem["food"]
    layout = problem["grid"]
    food_count = len(food)

    EAT_FOOD_SCORE = 10
    PACMAN_EATEN_SCORE = -500
    PACMAN_WIN_SCORE = 500
    PACMAN_MOVING_SCORE = -1

    directions = {
        "E": (0, 1),
        "N": (-1, 0),
        "W": (0, -1),
        "S": (1, 0)
    }

    Solution = ""
    Winner = ""


    def manhattan_distance(position1, position2):
        """
        Calculate the manhattan distance between two position.

        :param position1:  The first position
        :param position2:  The second position

        :return:           The manhattan distance between
        """
        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])


    def state_score(current_pacman, current_ghosts, current_food, steps):
        """
        First, check the score of current state;
        then, we add the evaluation value if the game is not over.

        The reason of using BFS to calculate the distance to the nearest food instead of manhattan distance is
        the same as p4

        Additionally, I use the average distance of ghosts and pacman to calculate the impact ghost result.
        The reason is to make sure all the ghosts can play optimally instead of leaving one ghost chasing pacman,
        while others wander around.

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

        # If the game is over, just return the score
        state, _ = check_finish(current_pacman, current_food, current_ghosts)
        if state:
            return score

        # If the game is not over, we add evaluation value to the score
        food_distance = bfs(current_pacman, current_food)
        ghost_distance = sum([bfs(current_pacman, [g]) for g in current_ghosts]) / len(current_ghosts)
        # 10 for the EAT_FOOD_SCORE, and 11 for impacting the agent's decision more with the ghosts
        return score + 10 / (food_distance + 1) - 11 / (ghost_distance + 1)


    def bfs(s, targets):
        """
        BFS to find the distance between the starting position to nearest target

        :param s:        the given starting position
        :param targets:  the location of targets

        :return:         distance between the nearest target and starting position
        """
        queue = collections.deque()
        visited = {s}
        queue.append((s, 0))
        while queue:
            u = queue.popleft()
            if u[0] in targets:
                return u[1]

            for action in get_possible_moves(layout, u[0]):
                (nr, nc) = move_item(u[0], action)
                if (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append(((nr, nc), u[1] + 1))

        return None


    def get_possible_moves(grid, position, is_ghost=False, current_ghosts=None):
        """
        Get actions the specific agent can take.
        If the agent is a ghost, we should consider of avoiding other ghosts

        :param grid:            the layout of the game map
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


    def check_finish(current_pacman, current_food, current_ghosts):
        """
        Check if the game is over at current state.

        :param current_pacman: The position of PacMan in this specific state
        :param current_ghosts: The position of ghosts in this specific state
        :param current_food:   The position and the number of food in this specific state

        :return:               Whether the game is over
        """

        if not current_food:
            return True, True

        if current_pacman in current_ghosts:
            return True, False

        return False, False


    def minimax(depth, current_pacman, current_food, current_ghosts, steps, idx, alpha, beta):
        """
        **MINIMAX FUNCTION**

        :param depth:          the depth of the minimax tree we are
        :param current_pacman: the position of pacman in this state
        :param current_food:   the position of ghosts in this specific state
        :param current_ghosts: the position and the number of food in this specific state
        :param steps:          the number of steps PacMan has taken in this specific state
        :param idx:            index of moving agent
        :param alpha:          alpha-beta pruning
        :param beta:           alpha-beta pruning
        :return:               the best action, or the value of evaluation function
        """
        # if we reach the leaf, or the maximum depth, return the evaluation
        state, the_winner = check_finish(current_pacman, current_food, current_ghosts)
        if depth == 0 or state:
            return None, state_score(current_pacman, current_ghosts, current_food, steps), the_winner

        # if it's pacman (max agent)
        if idx == -1:
            max_value = -float("inf")
            best_action = None
            win_agent = False

            possible_moves = get_possible_moves(layout, current_pacman)
            # if the pacman can't move, just stay and move on to the ghosts' turn
            if not possible_moves:
                _, max_value, win_agent = minimax(depth - 1, current_pacman, current_food, current_ghosts, steps + 1, idx + 1, alpha, beta)
                alpha = max(alpha, max_value)
            else:
                for action in possible_moves:
                    new_food = copy.deepcopy(current_food)
                    new_pacman = move_item(current_pacman, action)
                    if new_pacman in new_food:
                        new_food.remove(new_pacman)
                    _, value, agent = minimax(depth - 1, new_pacman, new_food, current_ghosts, steps + 1, idx + 1, alpha, beta)
                    # choose the best move
                    if value > max_value:
                        max_value = value
                        best_action = action
                    if agent:
                        win_agent = True

                    # alpha-beta pruning
                    alpha = max(alpha, max_value)
                    if alpha >= beta:
                        break
            return best_action, max_value, win_agent
        # if it's a ghost (min agent)
        else:
            # calculate the next agent
            next_agent = idx + 1
            win_agent = True
            if next_agent == len(current_ghosts):
                next_agent = -1

            min_value = float("inf")
            best_action = None
            possible_moves = get_possible_moves(layout, current_ghosts[idx], True, current_ghosts)
            if not possible_moves:
                _, min_value, win_agent = minimax(depth - 1, current_pacman, current_food, current_ghosts, steps, next_agent, alpha, beta)
                beta = min(beta, min_value)
            else:
                for action in possible_moves:
                    new_ghosts = copy.deepcopy(current_ghosts)
                    new_ghosts[idx] = move_item(current_ghosts[idx], action)
                    _, value, agent = minimax(depth - 1, current_pacman, current_food, new_ghosts, steps, next_agent, alpha, beta)
                    # choose the best action (for ghosts)
                    if value < min_value:
                        min_value = value
                        best_action = action

                    if not agent:
                        win_agent = False

                    # alpha-beta pruning
                    beta = min(beta, min_value)
                    if alpha >= beta:
                        break

            return best_action, min_value, win_agent

    def print_map():
        """
        Generate the string of current map.

        :return: the map now
        """
        res = ""
        for x, line in enumerate(layout):
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


    score = 0
    step = 0
    _, _, win_agent = minimax(k, pacman, food, ghosts, 0, -1, -float("inf"), float("inf"))
    if win_agent:
        Winner = "Pacman"
    else:
        Winner = "Ghost"
    return Solution, Winner

    # THE WHOLE PROCESS OF GAME
    '''
    while True:
        # PacMan's Turn
        step += 1
        score -= 1
        pacman_move, _, _ = minimax(k, pacman, food, ghosts, step, -1, -float("inf"), float("inf"))

        if pacman_move is not None:
            pacman = move_item(pacman, pacman_move)
            Solution += f"{step}: P moving {pacman_move}\n"

            # pacman crash into a ghost
            if pacman in ghosts:
                Solution += print_map()
                score -= 500
                Solution += f"score: {score}\n"
                Solution += "WIN: Ghost"
                Winner = "Ghost"
                return Solution, Winner
            # pacman eat a food
            elif pacman in food:
                score += 10
                food.remove(pacman)
                Solution += print_map()

                # check whether the pacman win
                if not food:
                    score += 500
                    Solution += f"score: {score}\n"
                    Solution += "WIN: Pacman"
                    Winner = "Pacman"
                    return Solution, Winner
                else:
                    Solution += f"score: {score}\n"
            else:
                Solution += print_map()
                Solution += f"score: {score}\n"
        else:
            Solution += f"{step}: P moving \n"
            Solution += print_map()
            Solution += f"score: {score}\n"

        # Ghost's Turn
        for idx, ghost in enumerate(ghosts):
            step += 1
            ghost_name = "WXYZ"[idx]
            ghost_move, _, _ = minimax(k, pacman, food, ghosts, step, idx, -float("inf"), float("inf"))

            if ghost_move is not None:
                Solution += f"{step}: {ghost_name} moving {ghost_move}\n"
                ghosts[idx] = move_item(ghost, ghost_move)

                if pacman in ghosts:
                    score -= 500

                    Solution += print_map()
                    Solution += f"score: {score}\n"
                    Solution += "WIN: Ghost"
                    Winner = "Ghost"
                    return Solution, Winner

                Solution += print_map()
                Solution += f"score: {score}\n"
            else:
                Solution += f"{step}: {ghost_name} moving \n"
                Solution += print_map()
                Solution += f"score: {score}\n"
    '''


if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 5
    file_name_problem = str(test_case_id) + '.prob'
    file_name_sol = str(test_case_id) + '.sol'
    path = os.path.join('test_cases', 'p' + str(problem_id))
    problem = parse.read_layout_problem(os.path.join(path, file_name_problem))
    k = int(sys.argv[2])
    num_trials = int(sys.argv[3])
    verbose = bool(int(sys.argv[4]))
    print('test_case_id:', test_case_id)
    print('k:', k)
    print('num_trials:', num_trials)
    print('verbose:', verbose)
    start = time.time()
    win_count = 0
    for i in range(num_trials):
        solution, winner = min_max_multiple_ghosts(copy.deepcopy(problem), k)
        if winner == 'Pacman':
            win_count += 1
        if verbose:
            print(solution)
    win_p = win_count / num_trials * 100
    end = time.time()
    print('time: ', end - start)
    print('win %', win_p)
