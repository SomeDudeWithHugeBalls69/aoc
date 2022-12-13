from collections import defaultdict

class Vertex:
    def __init__(self, height):
        self.adjacent = set() # going out
        self.height = height

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

board = [list(line) for line in lines]

# init vertices on the 2d map
heightmap = defaultdict(lambda: None) # don't want to bother with bounds checking later
elevations_with_a = []
for i in range(len(board)):
    for j in range(len(board[0])):
        if board[i][j] == "S":
            start_coords = (i, j)
            height = ord("a")
        elif board[i][j] == "E":
            end_coords = (i, j)
            height = ord("z")
        else:
            height = ord(board[i][j])

        heightmap[(i, j)] = Vertex(height)

        if board[i][j] == "a":
            elevations_with_a.append((i, j))


# add edges
for i in range(len(board)):
    for j in range(len(board[0])):
        vertex = heightmap[(i, j)]
        for n, m in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            neighbor = heightmap[(i + n, j + m)]
            if neighbor and neighbor.height - vertex.height <= 1   :
                vertex.adjacent.add(neighbor)

start = heightmap[start_coords]
end = heightmap[end_coords]

# BFS
def shortest_path_length(src):
    queue = [[src]]
    visited = set()

    while queue:
        path = queue.pop(0)
        vertex = path[-1]

        if vertex not in visited:
            for neighbor in vertex.adjacent:
                if neighbor == end:
                    return len(path)
                next_path = list(path)
                next_path.append(neighbor)
                queue.append(next_path)
            visited.add(vertex)

    return None


print("silver:", shortest_path_length(start))
gold = [shortest_path_length(heightmap[coords]) for coords in elevations_with_a]
gold = min([x for x in gold if x is not None])
print("gold:", gold)
