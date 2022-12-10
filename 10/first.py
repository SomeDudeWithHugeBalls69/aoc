with open("input.txt", "r") as f:
    lines = f.read().splitlines()

# X is cycle[-1]
cycle = [1]

def addx(V):
    X = cycle[-1]
    cycle.append(X)
    cycle.append(X+V)

def noop():
    X = cycle[-1]
    cycle.append(X)

for line in lines:
    if line.startswith("noop"):
        noop()
    elif line.startswith("addx"):
        addx(int(line.split(" ")[1]))

print("silver:", sum(([i * cycle[i-1] for i in (20, 60, 100, 140, 180, 220)])))

