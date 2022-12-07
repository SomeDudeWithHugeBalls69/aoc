


with open("input.txt", "r") as f:
    lines = f.read().splitlines()

shapes = {"A": "Rock", "B": "Paper", "C": "Scissors",
          "X": "Rock", "Y": "Paper", "Z": "Scissors"}

# A Y
# => fight[A][Y]
fight = {"Rock":     {"Rock": "draw", "Paper": "win", "Scissors": "loss"},
         "Paper":    {"Rock": "loss", "Paper": "draw", "Scissors": "win"},
         "Scissors": {"Rock": "win", "Paper": "loss", "Scissors": "draw"}}

shape_points = {"Rock": 1, "Paper": 2, "Scissors": 3}
outcome_points = {"loss": 0, "draw": 3, "win": 6}
fight_points = lambda shape, outcome: shape_points[shape] + outcome_points[outcome]

total_points = 0
for line in lines:
    first, second = line.split(" ")
    opponent_shape = shapes[first]
    my_shape = shapes[second]
    result = fight[opponent_shape][my_shape]
    total_points += fight_points(my_shape, result)

print(total_points) # 13005

