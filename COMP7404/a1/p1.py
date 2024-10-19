import collections
import sys, grader, parse

def dfs_search(problem):
    start: str = problem[0]
    stack: collections.deque[str] = collections.deque([start])
    goals: list[str] = problem[1]
    edges: dict[str, list[tuple[str, float]]] = problem[3]

    vis: set[str] = set()

    explored: str = ""
    while stack:
        current_path: str = stack.pop()
        u: str = current_path.split(" ")[-1]

        if u in goals:
            return explored + "\n" + current_path

        if u in vis:
            continue
        vis.add(u)

        if explored == "":
            explored += u
        else:
            explored += " " + u

        if u in edges:
            for v, _ in edges[u]:
                stack.append(current_path + " " + v)

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 1
    grader.grade(problem_id, test_case_id, dfs_search, parse.read_graph_search_problem)