import copy

chamber_width = 7

with open("input.txt", "r") as f:
    data = f.read()

movements = list(data)

rocks = [
"####",
""".#.
###
.#.""",
"""..#
..#
###""",
"""#
#
#
#""",
"""##
##""",
]

# def draw_board(board):
#     print()
#     for x in range(10, -1, -1):
#         print("|", end="")
#         for y in range(chamber_width):
#             elem = "#" if (x, y) in board else "."
#             print(elem, end="")
#         print("|")
#     print("+", "-"*chamber_width, "+", sep="")


# convert rocks to coord offset based on left-bottom corner
rock_offsets = []
for rock_id, rock in enumerate(rocks):
    coords = set()
    for x, line in enumerate(reversed(rock.splitlines())):
        for y, sign in enumerate(line):
            if sign == "#":
                coords.add((x, y))
    rock_offsets.append(coords)


# 1x direction + 1x down if possible
# returns (new_rock_coords, isStillFalling)
def move_rock(board, rock_coords, direction):
    new_pos = set()
    # move direction
    vert_offset = -1 if direction == "<" else 1
    for x, y in rock_coords:
        new_pos.add((x, y + vert_offset))

    # check for collisions
    has_collision = any(not (0 <= y < chamber_width)
                        or (x, y) in board for x, y in new_pos)
    if has_collision:
        new_pos = rock_coords

    # move down
    final_pos = set()
    for x, y in new_pos:
        final_pos.add((x - 1, y))

    # check for collisions
    has_collision = any(not (0 <= x)
                        or (x, y) in board for x, y in final_pos)
    if has_collision:
        return new_pos, False
    return final_pos, True


# boord[x][y]:
#
# ^ x
# |
# |.......|
# |.......|
# +-----------> y

def solve(iter_count):
    tower_top = 0
    board = set()
    move_i = 0
    for rock_i in range(iter_count):
        rock_start = (tower_top + 3, 2)
        rock_coords = set([(rock_start[0] + coord[0], rock_start[1] + coord[1])
                                  for coord in rock_offsets[rock_i % len(rocks)]])

        while True:
            direction = movements[move_i % len(movements)]
            rock_coords, isStillMoving = move_rock(board, rock_coords, direction)
            move_i += 1
            if not isStillMoving:
                max_x = 0
                for x, y in rock_coords:
                    if max_x < x + 1:
                        max_x = x + 1
                    board.add((x, y))
                tower_top = max(tower_top, max_x)
                break
        #draw_board(board)

    return tower_top


print("silver:", solve(2022))
#print("gold:", solve(1000000000000))