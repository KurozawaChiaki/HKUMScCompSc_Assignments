import sys, grader, parse, math, random
from typing import List, Tuple, Dict

def get_possible_moves(grid: List[List[str]], position: Tuple[int, int], ghost = False, ghosts = None) -> List[str]:
    direction: List[str] = []

    if position[1] != len(grid[0]) - 1 and grid[position[0]][position[1] + 1] != '%':
        direction.append("E")
    if position[0] != 0 and grid[position[0] - 1][position[1]] != '%':
        direction.append("N")
    if position[0] != len(grid) - 1 and grid[position[0] + 1][position[1]] != '%':
        direction.append("S")
    if position[1] != 0 and grid[position[0]][position[1] - 1] != '%':
        direction.append("W")

    if ghost:
        res = [d for d in direction if move_item(position, d) not in ghosts]
        direction = res

    return direction

def print_map(grid, pacman, ghosts, food):
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

def move_item(original: Tuple[int, int], d: str) -> Tuple[int, int]:
    res: Tuple[int, int] = (-1, -1)
    if d == "E":
        res = (original[0], original[1] + 1)
    elif d == "N":
        res = (original[0] - 1, original[1])
    elif d == "S":
        res = (original[0] + 1, original[1])
    elif d == "W":
        res = (original[0], original[1] - 1)

    return res

def random_play_multiple_ghosts(problem):
    solution: str = ""

    seed: int = problem["seed"]
    solution += f"seed: {seed}\n"
    random.seed(seed, version = 1)

    step: int = 0
    solution += f"{step}\n"

    grid = problem["grid"]
    ghosts = problem["ghosts"]
    pacman = problem["pacman"]
    food = problem["food"]
    solution += print_map(grid, pacman, ghosts, food)

    score: int = 0
    while True:
        # PacMan's Turn
        step += 1
        pacman_moves = get_possible_moves(grid, pacman)
        score -= 1
        if pacman_moves:
            next_step: str = random.choice(pacman_moves)
            pacman = move_item(pacman, next_step)
            solution += f"{step}: P moving {next_step}\n"

            if pacman in ghosts:
                solution += print_map(grid, pacman, ghosts, food)
                score -= 500
                solution += f"score: {score}\n"
                solution += "WIN: Ghost"
                return solution
            elif pacman in food:
                score += 10
                food.remove(pacman)
                solution += print_map(grid, pacman, ghosts, food)

                if not food:
                    score += 500
                    solution += f"score: {score}\n"
                    solution += "WIN: Pacman"
                    return solution
                else:
                    solution += f"score: {score}\n"
            else:
                solution += print_map(grid, pacman, ghosts, food)
                solution += f"score: {score}\n"
        else:
            solution += f"{step}: P moving \n"
            solution += print_map(grid, pacman, ghosts, food)
            solution += f"score: {score}\n"

        # Ghost's Turn
        for idx, ghost in enumerate(ghosts):
            step += 1
            ghost_name = "WXYZ"[idx]
            ghost_moves = get_possible_moves(grid, ghost, True, ghosts)

            if ghost_moves:
                next_step = random.choice(ghost_moves)
                solution += f"{step}: {ghost_name} moving {next_step}\n"
                ghosts[idx] = move_item(ghost, next_step)

                if pacman in ghosts:
                    score -= 500

                    solution += print_map(grid, pacman, ghosts, food)
                    solution += f"score: {score}\n"
                    solution += "WIN: Ghost"
                    return solution

                solution += print_map(grid, pacman, ghosts, food)
                solution += f"score: {score}\n"
            else:
                solution += f"{step}: {ghost_name} moving \n"
                solution += print_map(grid, pacman, ghosts, food)
                solution += f"score: {score}\n"

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, random_play_multiple_ghosts, parse.read_layout_problem)