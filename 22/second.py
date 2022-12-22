import re
from collections import defaultdict

with open("input.txt", "r") as f:
    data = f.read()


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
        self.right = None
        self.left = None

    def __repr__(self):
        up_str = "; up=(" + str(self.up.row) + ", " + str(self.up.col) + ")" if self.up is not None else "; up=None"
        down_str = "; down=(" + str(self.down.row) + ", " + str(
            self.down.col) + ")" if self.down is not None else "; down=None"
        right_str = "; right=(" + str(self.right.row) + ", " + str(
            self.right.col) + ")" if self.right is not None else "; right=None"
        left_str = "; left=(" + str(self.left.row) + ", " + str(
            self.left.col) + ")" if self.left is not None else "; left=None"
        return "{val=" + str(self.val) + "; row=" + str(self.row) + "; col=" + str(self.col) \
               + up_str + down_str + right_str + left_str + "}"


empty_tile = Tile(Tile.EMPTY, -1, -1)
tiles = {}
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
for tile in tiles.values():
    if (tile.row - 1, tile.col) in tiles:
        tile.up = tiles[(tile.row - 1, tile.col)]
    if (tile.row + 1, tile.col) in tiles:
        tile.down = tiles[(tile.row + 1, tile.col)]
    if (tile.row, tile.col + 1) in tiles:
        tile.right = tiles[(tile.row, tile.col + 1)]
    if (tile.row, tile.col - 1) in tiles:
        tile.left = tiles[(tile.row, tile.col - 1)]

# add wrap-arounds
# tried a general solution, but fuck layout+edge+orientation detection... gonna hardcode it
side_length = 50
# side a is most upper-left top-side, then labeling them clock-wise
# side_name -> (from_pos, to_pos, direction_into_edge)
# sides = {
#     "a": ((0, 1), (0, 2), "up"),
#     "b": ((0, 2), (0, 3), "up"),
#     "c": ((0, 3), (1, 3), "right"),
#     "d": ((1, 2), (1, 3), "down"),
#     "e": ((1, 2), (2, 2), "right"),
#     "f": ((2, 2), (3, 2), "right"),
#     "g": ((3, 1), (3, 2), "down"),
#     "h": ((3, 1), (4, 1), "right"),
#     "i": ((4, 0), (4, 1), "down"),
#     "j": ((3, 0), (4, 0), "left"),
#     "k": ((2, 0), (3, 0), "left"),
#     "l": ((2, 0), (2, 1), "up"),
#     "m": ((1, 1), (2, 1), "left"),
#     "n": ((0, 1), (1, 1), "left"),
# }
# connections = {
#     "a": "j",
#     "b": "i",
#     "c": "f",
#     "d": "e",
#     "e": "d",
#     "f": "c",
#     "g": "h",
#     "h": "g",
#     "i": "b",
#     "j": "a",
#     "k": "n",
#     "l": "m",
#     "m": "l",
#     "n": "k",
# }
#
# borders = (((1, 0), (2, 1), (3, 0), (5, 0)),
#            ((4, 2), (2, 2), (0, 2), (5, 3)),
#            ((1, 2), (5, 2), (3, 2), (2, 3)),
#            ((4, 0), (5, 1), (0, 0), (2, 0)),
#            ((1, 3), (4, 1), (3, 1), (0, 3)),
#            ((4, 3), (1, 1), (0, 1), (3, 3)))
#
# for side, info in sides.items():
#     print("=======", side, info, "=========")
#     start, end, dir = info
#     start_row, start_col = start
#     end_row, end_col = end
#     row_diff, col_diff = end_row - start_row, end_col - start_col
#
#     to_start, to_end, to_dir = sides[connections[side]]
#     print(to_start, to_end, to_dir)
#     to_start_row, to_start_col = to_start
#     to_end_row, to_end_col = to_end
#     to_row_diff, to_col_diff = to_end_row - to_start_row, to_end_col - to_start_col
#     print(row_diff, col_diff)
#     print(to_row_diff, to_col_diff)
#     for i in range(50):
#         from_row, from_col = 50 * start_row + i * row_diff, 50 * start_col + i * col_diff
#         to_row = 50 * to_start_row + i * to_row_diff
#         to_col = 50 * to_end_col + i * to_col_diff
#         print(from_row, from_col, to_row, to_col)
#         setattr(tiles[(from_row, from_col)], dir, tiles[(to_row, to_col)])

# fugg it :D:D:D:D:D:D
for i in range(50):
    ### x <-> y
    # a <-> j
    x = (0, 50 + i)
    y = (150 + i, 0)
    setattr(tiles[x], "up", tiles[y])
    setattr(tiles[y], "left", tiles[x])
    # b <-> i
    x = (0, 100 + i)
    y = (199, 0 + i)
    setattr(tiles[x], "up", tiles[y])
    setattr(tiles[y], "down", tiles[x])
    # c <-> f
    x = (0 + i, 149)
    y = (149 - i, 99)
    setattr(tiles[x], "right", tiles[y])
    setattr(tiles[y], "right", tiles[x])
    # d <-> e
    x = (49, 100 + i)
    y = (50 + i, 99)
    setattr(tiles[x], "down", tiles[y])
    setattr(tiles[y], "right", tiles[x])
    # g <-> h
    x = (149, 50 + i)
    y = (150 + i, 49)
    setattr(tiles[x], "down", tiles[y])
    setattr(tiles[y], "right", tiles[x])
    # k <-> n
    x = (100 + i, 0)
    y = (49 - i, 50)
    setattr(tiles[x], "left", tiles[y])
    setattr(tiles[y], "left", tiles[x])
    # l <-> m
    x = (100, 0 + i)
    y = (50 + i, 50)
    setattr(tiles[x], "up", tiles[y])
    setattr(tiles[y], "left", tiles[x])

# off-by-one error somewhere after I tried to make it a general solution (but I gave up)
# can't be bothered to fix it again

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
        if new_pos is None:
            print(turn, step, dir, pos)
            break
        if new_pos.val == Tile.SOLID:
            break
        pos = new_pos

dir_score = {"right": 0, "down": 1, "left": 2, "up": 3}
print(pos.row, pos.col, dir)
print("gold:", (pos.row + 1) * 1000 + (pos.col + 1) * 4 + dir_score[dir])
