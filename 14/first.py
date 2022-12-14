from collections import defaultdict
import math


with open("input.txt", "r") as f:
    lines = f.read().splitlines()

# parse input
field = defaultdict(lambda: ".")
for line in lines:
    points = line.split(" -> ")
    for i in range(1, len(points)):
        x1, y1 = map(int, points[i - 1].split(","))
        x2, y2 = map(int, points[i].split(","))
        if x1 == x2:
            y1, y2 = min(y1, y2), max(y1, y2)
            for y in range(y1, y2 + 1):
                field[(x1, y)] = "#"
        elif y1 == y2:
            x1, x2 = min(x1, x2), max(x1, x2)
            for x in range(x1, x2 + 1):
                field[(x, y1)] = "#"


def print_field():
    for i in range(200):
        print(i, end=" ")
        for j in range(450, 520):
            if j == 500 and i == 0:
                print("+", end="")
            else:
                print(field[(j, i)], end="")
        print()


# simulate sand
sand_start = (500, 0)
directions = [(0, 1), (-1, 1), (1, 1)]
y_bounds = 1000

def spawn_and_simulate_sand():
    x, y = sand_start
    while True:
        has_moved = False
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if new_y >= y_bounds:
                return -math.inf, -math.inf
            if field[(new_x, new_y)] == ".":
                x, y = new_x, new_y
                has_moved = True
                break
        if not has_moved:
            return x, y


steps = 0
while True:
    x, y = spawn_and_simulate_sand()
    if y == -math.inf:
        break
    steps += 1
    field[(x, y)] = "o"

print_field()
print("silver:", steps)
