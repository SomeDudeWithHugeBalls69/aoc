with open("input.txt", "r") as f:
    lines = f.read().splitlines()

directions = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}

def is_close(x1, y1, x2, y2):
    return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1

def sign(a):
    return 0 if a == 0 else 1 if a > 0 else -1

def solve(rope_len):
    # knots[0] is the head, knots[-1] is the tail
    knots = [(0, 0) for _ in range(rope_len)]
    tail_path = [(0, 0)]

    for line in lines:
        direction, steps = line.split(" ")
        diff = directions[direction]
        for i in range(int(steps)):
            # update head
            knots[0] = (knots[0][0] + diff[0], knots[0][1] + diff[1])
            # update other knots
            for j in range(1, len(knots)):
                next_knot = knots[j-1]
                knot = knots[j]
                if not is_close(*next_knot, *knot):
                    hx, hy = next_knot
                    tx, ty = knot
                    knots[j] = (tx + sign(hx - tx), ty + sign(hy - ty))
            tail_path.append(knots[j])
    return len(set(tail_path))

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
