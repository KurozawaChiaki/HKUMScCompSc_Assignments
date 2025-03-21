import sys, parse, grader
from queue import PriorityQueue

def astar_search(problem):
    start: str = problem[0]
    q: PriorityQueue = PriorityQueue()
    goals: list[str] = problem[1]
    edges: dict[str, list[tuple[str, float]]] = problem[3]
    h: dict[str, int] = problem[2]

    vis: set[str] = set()

    explored: str = ""
    q.put((h[start], start))
    while q:
        dis, current_path = q.get()
        u: str = current_path.split(" ")[-1]
        dis -= h[u]

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
                q.put((dis + d + h[v], current_path + " " + v))

if __name__ == "__main__":
    test_case_id = int(sys.argv[1])
    problem_id = 5
    grader.grade(problem_id, test_case_id, astar_search, parse.read_graph_search_problem)