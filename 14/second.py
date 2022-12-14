from collections import defaultdict

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

# parse input
def parse_field():
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
    return field


def print_field():
    for i in range(y_bounds+2):
        print(i, end=" ")
        for j in range(450, 520):
            if j == 500 and i == 0:
                print("+", end="")
            else:
                print(field[(j, i)], end="")
        print()


def spawn_and_simulate_sand():
    x, y = sand_start
    while True:
        has_moved = False
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if new_y >= y_bounds:
                return x, y
            if field[(new_x, new_y)] == ".":
                x, y = new_x, new_y
                has_moved = True
                break
        if not has_moved:
            return x, y

def part():
    steps = 0
    while True:
        x, y = spawn_and_simulate_sand()
        if x == sand_start[0] and y == sand_start[1]:
            break
        steps += 1
        field[(x, y)] = "o"
    return steps + 1


field = parse_field()
sand_start = (500, 0)
directions = [(0, 1), (-1, 1), (1, 1)]
y_bounds = max([y for x, y in field]) + 2

gold = part()
print_field()
print("gold:", gold)
