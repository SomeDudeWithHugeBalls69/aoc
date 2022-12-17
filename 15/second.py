from multiprocessing import Pool

with open("input.txt", "r") as f:
    lines = f.read().splitlines()

closest = {}
sensors = set()

for line in lines:
    # too lazy for regex
    _, sx, _, sy, _, bx, _, by = line\
        .replace("y=", ":")\
        .replace("x=", ":")\
        .replace(",", ":")\
        .split(":")
    sx, sy, bx, by = map(int, (sx, sy, bx, by))
    sensors.add((sx, sy))
    closest[(sx, sy)] = (bx, by)


def distance(x1, y1, x2, y2):
    return abs(x1-x2) + abs(y1-y2)


def is_close_to_known_beacon(x, y):
    if not (0 <= x <= limit and 0 <= y <= limit):
        return True
    for sensor in sensors:
        if distance(x, y, *sensor) <= distance(*sensor, *closest[sensor]):
            return True
    return False


def check_rhombus_edge(sensor):
    xs, ys = sensor
    xb, yb = closest[sx, sy]
    d = distance(xs, ys, xb, yb)

    # rhombus edge points
    left = xs - d - 1
    top = ys - d - 1
    right = xs + d + 1
    bottom = ys + d + 1
    for i in range(xs - left + 1):
        # left-top edge
        if not is_close_to_known_beacon(left + i, ys - i):
            return left + i, ys - i
        # left-bottom edge
        if not is_close_to_known_beacon(left + i, ys + i):
            return left + i, ys + i

    for i in range(right - xs + 1):
        # right-top edge
        if not is_close_to_known_beacon(xs + i, top + i):
            return xs + i, top + i
        # right-bottom edge
        if not is_close_to_known_beacon(xs + i, bottom - i):
            return xs + i, bottom - i
    print("finished scanning sensor", sensor)


def part2():
    with Pool(13) as p:
        results = p.imap_unordered(check_rhombus_edge, list(sensors))
        p.close()
        # stop early if result found
        coords = None
        for result in results:
            if result:
                coords = result
                p.terminate()
                break
        p.join()
        return coords


limit = 4000000
x, y = part2()
print("gold:", x * 4000000 + y)
