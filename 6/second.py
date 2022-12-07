from collections import deque

with open("input.txt", "r") as f:
    line = f.read()
q = deque()

for i, c in enumerate(line):
    if len(q) >= 14:
        q.popleft()
    q.append(c)
    if len(set(q)) == 14:
        print(i+1)
        break


##### polished #####
# l: length of unique marker to find
def solve(l):
    for i in range(l, len(line)):
        if len(set(line[i-l:i])) == l:
            return i

print("gold:",  solve(4))
print("silver", solve(14))