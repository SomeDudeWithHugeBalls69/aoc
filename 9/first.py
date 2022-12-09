# see second.py for polished+correct version

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

# paths
head = [(0, 0)]
tail = [(0, 0)]

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

for line in lines:
    direction, steps = line.split(" ")
    diff = directions[direction]
    for i in range(int(steps)):
        cur_head = head[-1]
        next_head = (cur_head[0] + diff[0], cur_head[1] + diff[1])
        head.append(next_head)
        if not is_close(*next_head, *tail[-1]):
            hx, hy = head[-1]
            tx, ty = tail[-1]
            # the following rules work for part 1, but are incorrect and won't work for part 2
            if hx == tx or hy == ty:
                tail.append((tx + diff[0], ty + diff[1]))
            elif direction in ("R", "L"):
                tail.append((tx + diff[0], hy))
            elif direction in ("U", "D"):
                tail.append((hx, ty + diff[1]))

print("silver:", len(set(tail)))


"""
def pretty_print():
    min_x = min([coords[0] for coords in head])
    max_x = max(max([coords[0] for coords in head]), 8)
    min_y = min([coords[1] for coords in head])
    max_y = max(min([coords[1] for coords in head]), 8)
    for i in range(min_x, max_x):
        for j in range(min_y, max_y):
            #print(i, j)
            if (i, j) == head[-1]:
                print("H", end="")
            elif (i, j) == tail[-1]:
                print("T", end="")
            elif (i, j) in tail:
                print("#", end="")
            else:
                print(".", end="")
        print()
    print("=================")
"""