import numpy as np
from scipy.spatial import Delaunay
import functools

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

grid = set()
for line in lines:
    x, y, z = map(int, line.split(","))
    grid.add((x, y, z))

max_x = max([x for x, y, z in grid])
min_x = min([x for x, y, z in grid])
max_y = max([y for x, y, z in grid])
min_y = min([y for x, y, z in grid])
max_z = max([z for x, y, z in grid])
min_z = min([z for x, y, z in grid])

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


# def in_hull(p, hull):
#     return Delaunay(hull).find_simplex(p) >= 0
#
# def solve2():
#     grid_array = np.array(list(map(list, grid)))
#     is_in_hull = {}
#     faces = 0
#     for x, y, z in grid:
#         for neighbor in get_neighbors(x, y, z):
#             if neighbor not in is_in_hull:
#                 is_in_hull[neighbor] = in_hull(np.array(neighbor), grid_array)
#             if is_in_hull[neighbor]:
#                 faces += 1
#     print(len(is_in_hull))
#     print(is_in_hull)
#     return faces


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
            if neighbor in outside:
                faces += 1
    return faces


print("silver:", solve1())
print("gold:", solve2())
