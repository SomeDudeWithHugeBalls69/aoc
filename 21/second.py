import numpy as np
from scipy.optimize import minimize

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

monkeys = {}

for line in lines:
    monkey, contents = line.split(": ")
    if " " in contents:  # calculation
        monkeys[monkey] = contents.split(" ")
    else:  # number
        monkeys[monkey] = int(contents)


def resolve(monkey, humn_val):
    content = monkeys[monkey]
    if isinstance(content, int):
        if monkey == "humn":
            return humn_val
        return content
    else:
        monkey1, operation, monkey2 = content
        val1 = resolve(monkey1, humn_val)
        val2 = resolve(monkey2, humn_val)
        if monkey == "root":
            return val1, val2
        else:
            return eval(str(val1) + operation + str(val2))


def func(humn_val):
    humn_val, tar_val = resolve("root", humn_val[0])
    return abs(humn_val - tar_val)

print("silver:", int(sum(resolve("root", monkeys["humn"]))))
result = minimize(func, np.array([5]), method="Powell", tol=1e-7)
print("gold:", int(result.x))

