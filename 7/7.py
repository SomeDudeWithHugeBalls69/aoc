class Directory:
    def __init__(self, superdir, files, subdirs):
        self.superdir = superdir
        self.files = files
        self.subdirs = subdirs
        self.size = None


### parse file
with open("input.txt", "r") as f:
    lines = f.read().splitlines()

root = Directory(None, {}, {})
cur_dir = root
for line in lines[1:]:
    if line.startswith("$"):  # is a command
        if line.startswith("$ ls"):
            continue
        elif line.startswith("$ cd"):
            nextdir = line[5:]
            if nextdir == "..":
                cur_dir = cur_dir.superdir
            else:
                cur_dir = cur_dir.subdirs[nextdir]
    else:  # `ls` output
        a, b = line.split(" ")
        if a == "dir":  # dir dir_name
            if b not in cur_dir.subdirs:
                cur_dir.subdirs[b] = Directory(cur_dir, {}, {})
        else:  # 29116 filename
            cur_dir.files[b] = int(a)


### calc directory size
def calc_size(dir):
    size = 0
    for file_size in dir.files.values():
        size += file_size
    for subdir in dir.subdirs.values():
        size += calc_size(subdir)
    dir.size = size
    return size


def get_sizes(dir):
    for subdir in dir.subdirs.values():
        yield from get_sizes(subdir)
    yield dir.size

calc_size(root)
sizes = list(get_sizes(root))
print("part1: " + str( sum([s for s in sizes if s <= 100000])) )

### part 2
total_disk_space = 70000000
target_unused = 30000000
total_unused = total_disk_space - root.size
to_delete = target_unused - total_unused

print("part2: " + str( min([s for s in sizes if s >= to_delete]) ))
