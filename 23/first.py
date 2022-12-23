from collections import defaultdict

with open("input.txt", "r") as f:
#with open("example.txt", "r") as f:
#with open("small_example.txt", "r") as f:
    lines = f.read().splitlines()

ELF = 1
EMPTY = 0

board = defaultdict(lambda: EMPTY)


for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == "#":
            board[(i, j)] = ELF


def print_board():
    min_x = min([x for x, y in board])
    max_x = max([x for x, y in board])
    min_y = min([y for x, y in board])
    max_y = max([y for x, y in board])
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if board[(x, y)] == ELF:
                print("#", end="")
            else:
                print(".", end="")
        print()

#print_board()

def elf_is_in_north(x, y):
    return ELF in (board[(x-1, y)], board[(x-1, y-1)], board[(x-1, y+1)])

def elf_is_in_south(x, y):
    return ELF in (board[(x+1, y)], board[(x+1, y-1)], board[(x+1, y+1)])

def elf_is_in_west(x, y):
    return ELF in (board[(x, y-1)], board[(x+1, y-1)], board[(x-1, y-1)])

def elf_is_in_east(x, y):
    return ELF in (board[(x, y+1)], board[(x-1, y+1)], board[(x+1, y+1)])

def elf_is_in_neighborhood(x, y):
    return elf_is_in_north(x, y) or elf_is_in_south(x, y) or elf_is_in_west(x, y) or elf_is_in_east(x, y)

direction_checks = [
    ("N", elf_is_in_north, -1, 0),
    ("S", elf_is_in_south, 1, 0),
    ("W", elf_is_in_west, 0, -1),
    ("E", elf_is_in_east, 0, 1),
]

def do_round():
    # (elf_x, elf_y) -> proposed direction
    proposals = {}
    # first half
    for xy, val in list(board.items()):
        if val != ELF:
            continue
        x, y = xy
        if not elf_is_in_neighborhood(x, y):
            continue
        for direction, elf_check, x_offset, y_offset in direction_checks:
            if not elf_check(x, y):
                proposals[(x, y)] = (x + x_offset, y + y_offset)
                break

    #print("before proposals=", proposals)
    # second half
    counts = defaultdict(lambda: 0)
    for start_pos, end_pos in proposals.items():
        counts[end_pos] += 1

    for start_pos, end_pos in list(proposals.items()):
        if counts[end_pos] > 1:
            del proposals[start_pos]

    # print("counts=", counts)
    # print("after proposals=", proposals)

    for from_xy, to_xy in proposals.items():
        board[from_xy] = EMPTY
        board[to_xy] = ELF

    # rotate directions
    direction_checks.append(direction_checks.pop(0))


for _ in range(10):
    do_round()

elf_xs = [x for x, y in board if board[(x, y)] == ELF]
elf_ys = [y for x, y in board if board[(x, y)] == ELF]
count = 0
for x in range(min(elf_xs), max(elf_xs)+1):
    for y in range(min(elf_ys), max(elf_ys)+1):
        if board[(x, y)] == EMPTY:
            count += 1

print("silver:", count)


