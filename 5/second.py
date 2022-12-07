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



with open("input.txt", "r") as f:
    lines = f.read().splitlines()

input = """PDQRVBHF
VWQZDL
CPRGQZLH
BVJFHDR
CLWZ
MVGTNPRJ
SBMVLRJ
JPD
VWNCD"""
input = input.splitlines()

stacks = {}
for i in range(9):
    stacks[i] = list(reversed(input[i]))

# manually deleted header in input.txt
for line in lines:
    num = int(line[line.find("move ")+5: line.find(" from")])
    fr = int(line[line.find("from ")+5: line.find(" to")])-1
    to = int(line[line.find("to ")+3:])-1

    temp = []
    for i in range(num):
        elem = stacks[fr].pop()
        temp.append(elem)
    for i in range(num):
        stacks[to].append(temp.pop())

for i in range(9):
    print(stacks[i].pop())

