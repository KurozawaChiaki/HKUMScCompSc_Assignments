import copy


def read_grid_mdp_problem_p1(file_path):
    file = []
    with open(file_path, 'r') as f:
        file = f.readlines()

    for x, line in enumerate(file):
        file[x] = line.strip("\n")

    res = {
        "seed": int(file[0].replace("seed: ", "")),
        "noise": float(file[1].replace("noise: ", "")),
        "livingReward": float(file[2].replace("livingReward: ", "")),
        "grid": [],
        "policy": []
    }

    i = 3
    while i < len(file):
        line = file[i]
        if line == "grid:":
            i += 1
            while file[i] != "policy:":
                content_line = file[i]
                elements = content_line.split()
                res["grid"].append(copy.deepcopy(elements))
                i += 1
        elif line == "policy:":
            i += 1
            while i < len(file):
                content_line = file[i]
                elements = content_line.split()
                res["policy"].append(copy.deepcopy(elements))
                i += 1

    return res

def read_grid_mdp_problem_p2(file_path):
    file = []
    with open(file_path, 'r') as f:
        file = f.readlines()

    for x, line in enumerate(file):
        file[x] = line.strip("\n")

    res = {
        "discount": float(file[0].replace("discount: ", "")),
        "noise": float(file[1].replace("noise: ", "")),
        "livingReward": float(file[2].replace("livingReward: ", "")),
        "iterations": int(file[3].replace("iterations: ", "")),
        "grid": [],
        "policy": []
    }

    i = 4
    while i < len(file):
        line = file[i]
        if line == "grid:":
            i += 1
            while file[i] != "policy:":
                content_line = file[i]
                elements = content_line.split()
                res["grid"].append(copy.deepcopy(elements))
                i += 1
        elif line == "policy:":
            i += 1
            while i < len(file):
                content_line = file[i]
                elements = content_line.split()
                res["policy"].append(copy.deepcopy(elements))
                i += 1

    return res

def read_grid_mdp_problem_p3(file_path):
    #Your p3 code here
    problem = ''
    return problem