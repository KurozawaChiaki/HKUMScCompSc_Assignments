import collections
import sys, grader, parse

def bfs_search(problem):
    start: str = problem[0]
    q: collections.deque[str] = collections.deque([start])
    goals: list[str] = problem[1]
    edges: dict[str, list[tuple[str, float]]] = problem[3]

    vis: set[str] = set()

    explored: str = ""
    while q:
        current_path: str = q.popleft()
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
                q.append(current_path + " " + v)

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 2
    grader.grade(problem_id, test_case_id, bfs_search, parse.read_graph_search_problem)