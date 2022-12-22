import re
from collections import defaultdict

with open("input.txt", "r") as f:
    data = f.read()

OPEN_TILE = "."
SOLID_WALL = "#"

# too lazy to deal with the wrap around in an indexed data structure
class Tile:
    OPEN = "."
    SOLID = "#"
    EMPTY = " "
    def __init__(self, value, row, col):
        self.val = value
        self.row = int(row)
        self.col = int(col)
        self.up = None
        self.down = None
        self.right= None
        self.left = None

    def __repr__(self):
        up_str = "; up=(" + str(self.up.row) + ", " + str(self.up.col) + ")" if self.up is not None else "; up=None"
        down_str = "; down=(" + str(self.down.row) + ", " + str(self.down.col) + ")" if self.down is not None else "; down=None"
        right_str = "; right=(" + str(self.right.row) + ", " + str(self.right.col) + ")" if self.right is not None else "; right=None"
        left_str = "; left=(" + str(self.left.row) + ", " + str(self.left.col) + ")" if self.left is not None else "; left=None"
        return "{val=" + str(self.val) + "; row=" + str(self.row) + "; col=" + str(self.col) \
               + up_str + down_str + right_str + left_str + "}"


empty_tile = Tile(Tile.EMPTY, -1, -1)
tiles = defaultdict(lambda: empty_tile)
start_tile = None
board, password = data.split("\n\n")
steps = list(map(int, re.findall(r'\d+', password)))
turns = re.findall(r'\D+', password)

# 0-index it, needs to be adjusted at the end result
isFirst = True
for i, row in enumerate(board.splitlines()):
    for j, c in enumerate(row):
        if c in (Tile.OPEN, Tile.SOLID):
            tiles[(i, j)] = Tile(c, i, j)
            if isFirst:
                start_tile = tiles[(i, j)]
                isFirst = False

# wire up
for tile in list(tiles.values()):
    tile.up = tiles[(tile.row - 1, tile.col)]
    tile.down = tiles[(tile.row + 1, tile.col)]
    tile.right = tiles[(tile.row, tile.col + 1)]
    tile.left = tiles[(tile.row, tile.col - 1)]

# add wrap-arounds
for tile in tiles.values():
    if tile == empty_tile:
        continue
    if tile.up.val == Tile.EMPTY:
        bottom = tile
        while bottom.down.val != Tile.EMPTY:
            bottom = bottom.down
        tile.up = bottom
        bottom.down = tile

    if tile.left.val == Tile.EMPTY:
        right_border = tile
        while right_border.right.val != Tile.EMPTY:
            right_border = right_border.right
        tile.left = right_border
        right_border.right = tile


# turn -> (cur_dir -> new_dir)
turn_map = {
    "L": {"up": "left", "left": "down", "down": "right", "right": "up"},
    "R": {"up": "right", "right": "down", "down": "left", "left": "up"}
}

dir = "right"
pos = start_tile
# consume first step since len(steps) == len(turns) + 1
for _ in range(steps[0]):
    new_pos = getattr(pos, dir)
    if new_pos.val == Tile.SOLID:
        break
    pos = new_pos

# do the rest
for turn, step in zip(turns, steps[1:]):
    dir = turn_map[turn][dir]
    for _ in range(step):
        new_pos = getattr(pos, dir)
        if new_pos.val == Tile.SOLID:
            break
        pos = new_pos


dir_score = { "right": 0, "down": 1, "left": 2, "up": 3}
print(pos.row, pos.col, dir)
print("silver:", (pos.row+1) * 1000 + (pos.col+1) * 4 + dir_score[dir])


