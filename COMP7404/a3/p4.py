"""
discount: 1
noise: 0.1
livingReward: -0.01
grid:
    _    _    _    1
    _    #    _   -1
    S    _    _    _
"""

def main():
    discount = 1
    noise = 0.1
    living_reward = -0.01
    grid = [
        ["_", "_", "_", "1"],
        ["_", "#", "_", "-1"],
        ["S", "_", "_", "_"]
    ]

if __name__ == "__main__":
    main()