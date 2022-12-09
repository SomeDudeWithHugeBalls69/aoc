with open("input.txt", "r") as f:
    lines = f.read().splitlines()

trees = [list(map(int, list(line))) for line in lines]

### part1
def is_visible(x, y):
    height = trees[x][y]
    left = trees[x][:y]
    right = trees[x][y+1:]
    top = [trees[a][y] for a in range(x)]
    bottom = [trees[a][y] for a in range(x+1, len(trees[0]))]
    if max(left) < height or max(right) < height or max(top) < height or max(bottom) < height:
        return True
    return False

def count_visible():
    visible = 0
    for i in range(1, len(trees)-1):
        for j in range(1, len(trees[0])-1):
            if is_visible(i, j):
                visible += 1
    return visible + 2*len(trees) + 2*len(trees[0]) - 4

### part 2
def count_dist(trees, height):
    distance = 0
    for tree in trees:
        distance += 1
        if tree >= height:
            break
    return distance

def scenic_score(x, y):
    height = trees[x][y]
    left = trees[x][:y]
    right = trees[x][y + 1:]
    top = [trees[a][y] for a in range(x)]
    bottom = [trees[a][y] for a in range(x + 1, len(trees[0]))]
    return (count_dist(right, height)
            * count_dist(reversed(left), height)
            * count_dist(bottom, height)
            * count_dist(reversed(top), height))

print("silver:", count_visible())
print("gold:", max([scenic_score(a, b) for a in range(len(trees)) for b in range(len(trees[0]))]))
