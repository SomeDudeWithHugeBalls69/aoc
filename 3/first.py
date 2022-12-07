
prio = {}
for i in range(1, 27):
    prio[chr(96 + i)] = i
    prio[chr(64 + i)] = i + 26

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

prio_sum = 0
for line in lines:
    set1, set2 = set(line[:len(line)//2]), set(line[len(line)//2:])
    elem = set1.intersection(set2).pop()
    prio_sum += prio[elem]

print(prio_sum)