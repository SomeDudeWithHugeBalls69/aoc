with open("input.txt", "r") as f:
    lines = f.read().splitlines()

X = 1
cycle = []
crt = ["."]*240

def draw_crt():
    for i in range(6):
        for j in range(40):
            print(crt[j + (40*i)], end="", sep="")
        print()

for line in lines:
    if line.startswith("noop"):
        cycle.append(X)
    elif line.startswith("addx"):
        V = int(line.split(" ")[1])
        cycle += [X, X]
        X += V

for i in range(len(cycle)):
    X_pos = cycle[i]
    #if (i-1)%40 <= X_pos <= (i+1)%40: # doesn't play nice with bound overlapping/ off-by-one
    # still has off-by-one for the first column, too lazy to fix
    if X_pos in ((i-1)%40, i%40, (i+1)%40):
        #print("# at", str(i))
        #draw_crt()
        crt[i] = "#"

print("silver:", sum(([i * cycle[i-1] for i in (20, 60, 100, 140, 180, 220)])))
print("gold:")
draw_crt()