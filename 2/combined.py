
shapes = {"A": "Rock", "B": "Paper", "C": "Scissors",
          "X": "Rock", "Y": "Paper", "Z": "Scissors"}
forced_outcome = {"X": "loss", "Y": "draw", "Z": "win"}

# fight: (other_shape, my_shape) -> outcome
fight = {"Rock":     {"Rock": "draw", "Paper": "win", "Scissors": "loss"},
         "Paper":    {"Rock": "loss", "Paper": "draw", "Scissors": "win"},
         "Scissors": {"Rock": "win", "Paper": "loss", "Scissors": "draw"}}

# guide: (other_shape, outcome) -> my_shape
guide = {k: v for k, v in fight.items()}
for other_shape, d in guide.items():
    guide[other_shape] = {v: k for k, v in d.items()}

shape_points = {"Rock": 1, "Paper": 2, "Scissors": 3}
outcome_points = {"loss": 0, "draw": 3, "win": 6}
fight_points = lambda shape, outcome: shape_points[shape] + outcome_points[outcome]


total_points1 = 0
total_points2 = 0
for line in open("input_first.txt", "r").read().splitlines():
    first, second = line.split(" ")
    opponent_shape = shapes[first]
    # part 1
    my_shape = shapes[second]
    result = fight[opponent_shape][my_shape]
    total_points1 += fight_points(my_shape, result)
    # part 2
    result = forced_outcome[second]
    my_shape = guide[opponent_shape][result]
    total_points2 += fight_points(my_shape, result)

print(total_points1)
print(total_points2)

