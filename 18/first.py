import itertools
from collections import defaultdict

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

grid = set()

for line in lines:
    x, y, z = map(int, line.split(","))
    grid.add((x, y, z))

#visited = set()
#queue = list(grid)
neighbor_offsets = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]

# faces = 0
# while queue:
#     x, y, z = queue.pop(0)
#     neighbors = [(x + nx, y + ny, z + nz) for nx, ny, nz in neighbor_offsets]
#     for neighbor in neighbors:
#         if neighbor in grid:
#             if neighbor not in visited:
#                 queue.append(neighbor)
#                 visited.add(neighbor)
#         else:
#             faces += 1

def solve1():
    faces = 0
    for x, y, z in grid:
         neighbors = [(x + nx, y + ny, z + nz) for nx, ny, nz in neighbor_offsets]
         for neighbor in neighbors:
             if neighbor not in grid:
                 faces += 1
    return faces

print("silver:", solve1())

