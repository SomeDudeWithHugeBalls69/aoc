import copy
from collections import defaultdict

with open("input.txt", "r") as f:
    lines = f.read().splitlines()


# doubly linked list of numbers
class Number:
    def __init__(self, id, value, next_number, prev_number):
        self.value = value
        self.id = id
        self.next_number = next_number
        self.prev_number = prev_number

    def __str__(self):
        return "Number{id=" + str(self.id) + "; value=" + str(self.value) + "; next_id=" + str(self.next_number.id) + "; prev_id=" + str(self.prev_number.id) + "}"


def print_numbers(zero_num):
    print("0", end=" ")
    num = zero_num.next_number
    while num.value != 0:
        print(num.value, end=" ")
        num = num.next_number
    print()


def solve(encryption_key=1, mix_count=1):
    numbers = []  # id -> number
    values = list(map(lambda a: encryption_key * int(a), lines))
    zero_number = None

    for i, value in enumerate(values):
        number = Number(i, value, None, None)
        numbers.append(number)
        if value == 0:
            zero_number = number

    for i in range(0, len(numbers)):
        numbers[i].prev_number = numbers[i-1]
        numbers[i].next_number = numbers[(i+1) % len(numbers)]

    # mixing
    for _ in range(mix_count):
        for number in numbers:
            # unlink number from linked list
            next_number = number.next_number
            prev_number = number.prev_number
            prev_number.next_number = next_number
            next_number.prev_number = prev_number

            # traverse 'step' times
            steps = number.value % (len(numbers) - 1)
            for _ in range(steps):
                next_number = next_number.next_number
            prev_number = next_number.prev_number

            # insert number
            number.next_number = next_number
            number.prev_number = prev_number
            next_number.prev_number = number
            prev_number.next_number = number

    result = 0
    num = zero_number
    for _ in range(1000):
        num = num.next_number
    result += num.value
    for _ in range(1000):
        num = num.next_number
    result += num.value
    for _ in range(1000):
        num = num.next_number
    result += num.value

    return result


print("silver:", solve())
print("gold:", solve(811589153, 10))


