# with open("input.txt", "r") as f:
#     data = f.read()
#
# header, instructions = data.split("\n\n")
# header = header.splitlines()[:-1]
#
# stacks = [[] for i in range(9)]
# for line in header:
#     for i in range(9):
#         elem = line[1 + i*4]
#         if elem != " ":
#             stacks[i].append(elem)
#
# stacks = [list(reversed(stack)) for stack in stacks]


#with open("input.txt", "r") as f:
with open("input.txt", "r") as f:
    lines = f.read().splitlines()

stacks = {}

input = """PDQRVBHF
VWQZDL
CPRGQZLH
BVJFHDR
CLWZ
MVGTNPRJ
SBMVLRJ
JPD
VWNCD"""

# input = """NZ
# DCM
# P"""

count = 9
input = input.splitlines()

for i in range(1, count+1):
    stacks[i] = list(reversed(list(input[i-1])))

for line in lines:
    num = int(line[line.find("move ")+5: line.find(" from")])
    fr = int(line[line.find("from ")+5: line.find(" to")])
    to = int(line[line.find("to ")+3:])

    print(stacks)
    print(num, fr, to)
    for i in range(num):
        print(i)
        elem = stacks[fr].pop()
        stacks[to].append(elem)


print(stacks)
for i in range(1, count+1):
    print(stacks[i].pop())

