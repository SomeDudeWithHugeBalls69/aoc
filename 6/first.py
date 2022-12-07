from collections import deque

with open("input.txt", "r") as f:
    line = f.read()

q = deque()

for i, c in enumerate(line):
    if len(q) >= 4:
        oldest = q.popleft()
    q.append(c)
    if len(set(q)) == 4:
        print(i+1)
        break

