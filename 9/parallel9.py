from queue import Queue
from threading import Thread
import sys

# $ time pypy 9.py input-2022-09-bb-100000.txt => 0m8.091s
# $ time pypy parallel9.py input-2022-09-bb-100000.txt => 2m20.572s
# :)

def is_close(x1, y1, x2, y2):
    return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1

def sign(a):
    return 0 if a == 0 else 1 if a > 0 else -1

class Knot(Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True
        self.queue = Queue()
        self.child_knot = None
        self.pos = (0, 0)

    def _follow(self, parent_pos):
        if not is_close(*parent_pos, *self.pos):
            hx, hy = parent_pos
            tx, ty = self.pos
            self.pos = (tx + sign(hx - tx), ty + sign(hy - ty))
            self.child_knot.queue.put(self.pos)

    def run(self):
        parent_pos = self.queue.get()
        while parent_pos:
            self._follow(parent_pos)
            self.queue.task_done()
            parent_pos = self.queue.get()
        # propagate the exit token (=None)
        self.child_knot.queue.put(parent_pos)

    def start_follow(self):
        self.start()


filename = "input.txt" if len(sys.argv) < 2 else sys.argv[1]
with open(filename, "r") as f:
    lines = f.read().splitlines()

directions = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}



def solve(rope_len):
    # init knots
    head = (0, 0)
    knots = [Knot() for _ in range(rope_len-1)]
    tail_path_collector = Knot()
    # wire up knots and start them
    for i in range(rope_len-2):
        knots[i].child_knot = knots[i+1]
        knots[i].start_follow()
    knots[-1].child_knot = tail_path_collector
    knots[-1].start_follow()

    # move head
    for line in lines:
        direction, steps = line.split(" ")
        diff = directions[direction]
        for i in range(int(steps)):
            # update head
            head = (head[0] + diff[0], head[1] + diff[1])
            # start update chain through knots
            knots[0].queue.put(head)

    # put exit token
    knots[0].queue.put(None)

    # gather tail movements
    tail_path = {(0, 0)}
    for coord in iter(tail_path_collector.queue.get, None):
        tail_path.add(coord)

    return len(tail_path)


print("silver:", solve(2))
print("gold:", solve(10))
