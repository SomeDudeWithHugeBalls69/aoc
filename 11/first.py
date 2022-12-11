with open("input.txt", "r") as f:
    data = f.read()

class Monkey:
    def __init__(self, config_string):
        self.id = int(config_string[7:config_string.find(":")])
        rest = [line[line.find(":")+2:] for line in config_string.splitlines()[1:]]
        self.items = list(map(int, rest[0].split(", ")))
        self.operation = lambda old: eval(rest[1][rest[1].find("=")+2:])
        self.divisible_by_test = int(rest[2][rest[2].find("y") + 2:])
        self.on_true_monkey_target = int(rest[3][rest[3].find("y") + 2:])
        self.on_false_monkey_target = int(rest[4][rest[4].find("y") + 2:])
        self.inspect_count = 0

    def do_round(self):
        while self.items:
            self.inspect_count += 1
            item = self.items.pop(0)
            item = self.operation(item) // 3
            if item % self.divisible_by_test == 0:
                #print("is divisible =>", self.id, "throws", item, "to", self.onTrueMonkeyTarget)
                monkeys[self.on_true_monkey_target].items.append(item)
            else:
                #print("not divisible =>", self.id, "throws", item, "to", self.onFalseMonkeyTarget)
                monkeys[self.on_false_monkey_target].items.append(item)

def print_monkey_items():
    for k, v in monkeys.items():
        print(k, v.items)

monkeys = {}  # id -> Monkey()
monkey_count = -1
data = data.split("\n\n")
for monkey_config in data:
    monkey = Monkey(monkey_config)
    monkeys[monkey.id] = monkey

monkey_count = max(monkeys.keys()) + 1

for i in range(20):
    for id in range(monkey_count):
        monkeys[id].do_round()

#print_monkey_items()

#inspect_counts = {id: monkey.inspect_count for id, monkey in monkeys.items()}
inspect_counts = [monkey.inspect_count for monkey in monkeys.values()]

print("silver:", (lambda a, b: a * b)(*sorted(inspect_counts)[-2:]))