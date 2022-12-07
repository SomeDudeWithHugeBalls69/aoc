
prio = {}
for i in range(1, 27):
    prio[chr(96 + i)] = i
    prio[chr(64 + i)] = i + 26

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

prio_sum = 0
for i in range(0, len(lines), 3):
    set1, set2, set3 = set(lines[i]), set(lines[i+1]), set(lines[i+2])
    elem = set1.intersection(set2).intersection(set3).pop()
    prio_sum += prio[elem]

print(prio_sum)