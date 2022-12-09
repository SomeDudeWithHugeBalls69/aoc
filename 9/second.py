import math

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

directions = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}

def is_close(x1, y1, x2, y2):
    if abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1:
        return True
    return False

# returns 1 if positive, -1 if negative, 0 if 0
def sign(a):
    return 0 if a == 0 else int(math.copysign(1, a))

def solve(rope_len):
    knots = []  # knots[0] is the head, knots[-1] is the tail
    for i in range(rope_len):
        knots.append([(0, 0)])

    for line in lines:
        direction, steps = line.split(" ")
        diff = directions[direction]
        for i in range(int(steps)):
            head = knots[0]
            head_pos = head[-1]
            next_head = (head_pos[0] + diff[0], head_pos[1] + diff[1])
            head.append(next_head)
            for j in range(1, len(knots)):
                next_knot = knots[j-1]
                knot = knots[j]
                if not is_close(*next_knot[-1], *knot[-1]):
                    hx, hy = next_knot[-1]
                    tx, ty = knot[-1]
                    knot.append((tx + sign(hx - tx), ty + sign(hy - ty)))
    return len(set(knots[-1]))

print("silver:", solve(2))
print("gold:", solve(10))


"""
def pretty_print(knots, line):
    head = knots[0]
    min_x = -18
    max_x = 18
    min_y = -18
    max_y = 18
    print("========", line,"========")
    for i in range(min_x, max_x):
        for j in range(min_y, max_y):
            if (i, j) == head[-1]:
                print("H", end="")
            else:
                for k in range(1, len(knots)):
                    if (i, j) == knots[k][-1]:
                        print(k, end="")
                        break
                else:
                    if (i, j) in knots[-1]:
                        print("#", end="")
                    else:
                        print(".", end="")
        print()
"""