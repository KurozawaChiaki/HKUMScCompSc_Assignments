import sys, parse, grader
from queue import PriorityQueue


def ucs_search(problem):
    start: str = problem[0]
    q: PriorityQueue = PriorityQueue()
    goals: list[str] = problem[1]
    edges: dict[str, list[tuple[str, float]]] = problem[3]

    vis: set[str] = set()

    explored: str = ""
    q.put((0, start))
    while q:
        dis, current_path = q.get()
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
            for v, d in edges[u]:
                q.put((dis + d, current_path + " " + v))

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 3
    grader.grade(problem_id, test_case_id, ucs_search, parse.read_graph_search_problem)