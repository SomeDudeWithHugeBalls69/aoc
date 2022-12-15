
with open("example.txt", "r") as f:
    lines = f.read().splitlines()

def print_board():
    x_max = max([x for x, y in board.keys()])
    x_min = min([x for x, y in board.keys()])
    y_max = max([y for x, y in board.keys()])
    y_min = min([y for x, y in board.keys()])
    for y in range(y_min, y_max+1):
        if 0 <= y < 10:
            print(" " + str(y), end=" ")
        else:
            print(y, end=" ")
        for x in range(x_min, x_max+1):
            if (x, y) in board:
                print(board[(x, y)], end="")
            else:
                print(".", end="")
        print()

board = {}
closest = {}
sensors = set()


for line in lines:
    # too lazy for regex
    _, sx, _, sy, _, bx, _, by = line\
        .replace("y=", ":")\
        .replace("x=", ":")\
        .replace(",", ":")\
        .split(":")
    sx, sy, bx, by = map(int, (sx, sy, bx, by))
    board[(sx, sy)] = "S"
    sensors.add((sx, sy))
    board[(bx, by)] = "B"
    closest[(sx, sy)] = (bx, by)

def distance(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)

def populate():
    for sensor in sensors:
        sx, sy = sensor
        bx, by = closest[sx, sy]
        d = distance(sx, sy, bx, by)
        print("distance ", d)
        for x in range(sx - d, sx + d + 1):
            for y in range(sy - d, sy + d + 1):
                if distance(x, y, sx, sy) <= d:
                    if (x, y) not in board:
                        board[(x, y)] = "#"

def silver():
    x_max = max([x for x, y in board.keys()])
    x_min = min([x for x, y in board.keys()])
    count = 0
    for x in range(x_min, x_max + 1):
        if (x, silver_y) in board and board[(x, silver_y)] == "#":
            count += 1
    return count



silver_y = 2000000
populate()
print("silver:", silver())
print_board()
