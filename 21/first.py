with open("input.txt", "r") as f:
    lines = f.read().splitlines()


monkeys = {}

for line in lines:
    monkey, contents = line.split(": ")
    if " " in contents:  # calculation
        monkeys[monkey] = contents.split(" ")
    else:  # number
        monkeys[monkey] = int(contents)


def resolve(monkey):
    content = monkeys[monkey]
    if isinstance(content, int):
        return content
    else:
        monkey1, operation, monkey2 = content
        val1 = resolve(monkey1)
        val2 = resolve(monkey2)
        return eval(str(val1) + operation + str(val2))

print(int(resolve("root")))