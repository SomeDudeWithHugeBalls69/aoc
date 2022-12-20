import numpy as np
from scipy.spatial import Delaunay
import functools

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

grid = set()
for line in lines:
    x, y, z = map(int, line.split(","))
    grid.add((x, y, z))

xs = [x for x, y, z in grid]
ys = [y for x, y, z in grid]
zs = [z for x, y, z in grid]
min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)
min_z, max_z = min(zs), max(zs)

neighbor_offsets = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]

def get_neighbors(x, y, z):
    return [(x + nx, y + ny, z + nz) for nx, ny, nz in neighbor_offsets]


def solve1():
    faces = 0
    for x, y, z in grid:
        for neighbor in get_neighbors(x, y, z):
            if neighbor not in grid:
                faces += 1
    return faces


delaunay = Delaunay(np.array(list(map(list, grid))))
def in_hull(p):
    return delaunay.find_simplex(p) >= 0


def calc_outside(start):
    visited = set()
    queue = [(min_x-1, min_y, min_z)]
    while queue:
        x, y, z = queue.pop(0)
        if (x, y, z) in grid or (x, y, z) in visited:
            continue
        visited.add((x, y, z))
        neighbors = get_neighbors(x, y, z)
        for nx, ny, nz in neighbors:
            if min_x-1 <= nx <= max_x+1 and min_y-1 <= ny <= max_y+1 and min_z-1 <= nz <= max_z+1:
                queue.append((nx, ny, nz))
    return visited

def solve2():
    outside = calc_outside((min_x - 1, min_y, min_z))
    faces = 0
    for x, y, z in grid:
        for neighbor in get_neighbors(x, y, z):
            # if not in_hull(neighbor):
            if neighbor in outside:
                faces += 1
    return faces


print("silver:", solve1())
print("gold:", solve2())

# for x in range(min_x, max_x+1):
#     print("========= x=", x, " =========", sep="")
#     for y in range(min_y, max_y+1):
#         for z in range(min_z, max_z+1):
#             if (x, y, z) in grid:
#                 print("#", end="")
#             elif in_hull((x, y, z)):
#                 print("x", end="")
#             else:
#                 print(".", end="")
#         print()

