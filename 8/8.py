with open("input.txt", "r") as f:
    lines = f.read().splitlines()

trees = [list(map(int, list(line))) for line in lines]


def is_visible(x, y):
    height = trees[x][y]
    left = trees[x][:y]
    right = trees[x][y+1:]
    top = [trees[a][y] for a in range(x)]
    bottom = [trees[a][y] for a in range(x+1, len(trees[0]))]
    if max(left) < height or max(right) < height or max(top) < height or max(bottom) < height:
        return True
    return False


def scenic_score(x, y):
    height = trees[x][y]
    left = trees[x][:y]
    right = trees[x][y + 1:]
    top = [trees[a][y] for a in range(x)]
    bottom = [trees[a][y] for a in range(x + 1, len(trees[0]))]
    left_dist = 0
    for tree in reversed(left):
        left_dist += 1
        if tree >= height:
            break
    right_dist = 0
    for tree in right:
        right_dist += 1
        if tree >= height:
            break
    top_dist = 0
    for tree in reversed(top):
        top_dist += 1
        if tree >= height:
            break
    bottom_dist = 0
    for tree in bottom:
        bottom_dist += 1
        if tree >= height:
            break

    return left_dist * right_dist * top_dist * bottom_dist


visible_count = 0
for i in range(1, len(trees)-1):
    for j in range(1, len(trees[0])-1):
        if is_visible(i, j):
            visible_count += 1

visible_count += 2*len(trees) + 2*len(trees[0]) - 4
print("silver:", visible_count)
print("gold:", max([scenic_score(a, b) for a in range(len(trees)) for b in range(len(trees[0]))]))