


with open("input.txt", "r") as f:
    lines = f.read().splitlines()

shapes = {"A": "Rock", "B": "Paper", "C": "Scissors"}
forced_outcome = {"X": "loss", "Y": "draw", "Z": "win"}

# A Y
# => fight[A][Y]
fight = {"Rock":     {"Rock": "draw", "Paper": "win", "Scissors": "loss"},
         "Paper":    {"Rock": "loss", "Paper": "draw", "Scissors": "win"},
         "Scissors": {"Rock": "win", "Paper": "loss", "Scissors": "draw"}}

# fight: (other_shape, my_shape) -> outcome
# guide: (other_shape, outcome) -> my_shape
guide = {k: v for k, v in fight.items()}
for other_shape, d in guide.items():
    guide[other_shape] = {v: k for k, v in d.items()}


shape_points = {"Rock": 1, "Paper": 2, "Scissors": 3}
outcome_points = {"loss": 0, "draw": 3, "win": 6}
fight_points = lambda shape, outcome: shape_points[shape] + outcome_points[outcome]

total_points = 0
for line in lines:
    first, second = line.split(" ")
    opponent_shape = shapes[first]
    result = forced_outcome[second]
    my_shape = guide[opponent_shape][result]
    total_points += fight_points(my_shape, result)

print(total_points) # 11373

