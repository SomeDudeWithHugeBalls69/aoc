with open("input.txt", "r") as f:
    data = f.read()

pairs = [pair.split("\n") for pair in data.split("\n\n")]

def compare(left, right):
    left_is_int = isinstance(left, int)
    right_is_int = isinstance(right, int)
    if left_is_int and right_is_int:
        return -1 if left < right else 0 if left == right else 1
    elif not left_is_int and not right_is_int:  # both values are lists
        for i in range(min(len(left), len(right))):
            res = compare(left[i], right[i])
            if res != 0:
                return res
        return compare(len(left), len(right))
    else:  # exactly one value is an integer
        left = [left] if left_is_int else left
        right = [right] if right_is_int else right
        return compare(left, right)

def is_in_right_order(pairs):
    for pair in pairs:
        left = eval(pair[0])
        right = eval(pair[1])
        yield compare(left, right)

silver = list(is_in_right_order(pairs))
silver = [i+1 for i in range(len(silver)) if silver[i] == -1]
print("silver:", sum(silver))