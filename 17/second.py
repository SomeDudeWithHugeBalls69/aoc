import copy
import math

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

# convert rocks to coord offset based on left-bottom corner
rock_offsets = []
for rock in rocks:
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

def solve1(iter_count):
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

    return tower_top


# find a cycle
def solve2(iter_count):
    cycle_start = None
    state_cache = set()

    board = set()
    contour_size = 23  # size of the top to save as state
    tower_top = 0  # highest block+1
    move_i = 0  # current vertical direction index
    i = 0  # stone index
    while i < iter_count:
        rock_id = i % len(rocks)
        rock_start = (tower_top + 3, 2)
        rock_coords = set([(rock_start[0] + coord[0], rock_start[1] + coord[1])
                                  for coord in rock_offsets[rock_id]])

        # move until rock landed
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

        # detect a cycle based on rock_id, movement_id and top-part of the tower
        upper_layer = tuple([(x, y) in board for x in range(tower_top - contour_size, tower_top) for y in range(chamber_width)])
        state = (rock_id, move_i % len(movements), upper_layer)

        if cycle_start is None:
            if state in state_cache:
                cycle_start = {"tower_top": tower_top, "i": i, "state": state}
            else:
                state_cache.add(state)
        else:
            if state == cycle_start["state"]:
                # found the cycle, now skip them N times and rebuild the upper_layer below tower_top
                # if done correctly, this block shouldn't trigger again
                tower_top_diff = tower_top - cycle_start["tower_top"]
                i_diff = i - cycle_start["i"]
                times_to_skip = math.floor((iter_count - i) / i_diff)

                # skip close to the end
                i += times_to_skip * i_diff
                tower_top += times_to_skip * tower_top_diff

                # rebuild upper_layer at the top again
                _, _, upper_layer = cycle_start["state"]
                upper_layer = tuple(upper_layer[i:i + chamber_width] for i in range(0, len(upper_layer), chamber_width))
                for x, row in enumerate(upper_layer):
                    for y, has_block in enumerate(upper_layer[x]):
                        if has_block:
                            board.add((tower_top - contour_size + x, y))
        i += 1
    return tower_top


print("silver:", solve1(2022))
print("gold:", solve2(1000000000000))