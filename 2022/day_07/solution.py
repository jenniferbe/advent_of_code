"""
--- Day 7: No Space Left On Device ---

You can hear birds chirping and raindrops hitting leaves as the expedition proceeds.
Occasionally, you can even hear much louder sounds in the distance; how big do the
animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication
system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device

Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting
terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k

The filesystem consists of a tree of files (plain data) and directories (which can
contain other directories or files). The outermost directory is called /. You can
navigate around the filesystem, moving into or out of directories and listing the
contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed, very
much like some modern computers:

    cd means change directory. This changes which directory is the current
    directory, but the specific result depends on the argument:
        cd x moves in one level: it looks in the current directory for the directory
            named x and makes it the current directory.
        cd .. moves out one level: it finds the directory that contains the current
            directory, then makes that directory the current directory.
        cd / switches the current directory to the outermost directory, /.
    ls means list. It prints out all of the files and directories immediately
    contained by the current directory:
        123 abc means that the current directory contains a file named abc with size 123.
        dir xyz means that the current directory contains a directory named xyz.

Given the commands and output in the example above, you can determine that the
filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)

Here, there are four directories: / (the outermost directory), a and d (which are in
/), and e (which is in a). These directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that
are good candidates for deletion. To do this, you need to determine the total size
of each directory. The total size of a directory is the sum of the sizes of the
files it contains, directly or indirectly. (Directories themselves do not count as
having any intrinsic size.)

The total sizes of the directories above can be found as follows:

    The total size of directory e is 584 because it contains a single file i of size
        584 and no other directories.
    The directory a has total size 94853 because it contains files f (size 29116),
        g (size 2557), and h.lst (size 62596), plus file i indirectly (a contains e
        which contains i).
    Directory d has total size 24933642.
    As the outermost directory, / contains every file. Its total size is 48381165,
        the sum of the size of every file.

To begin, find all of the directories with a total size of at most 100000, then
calculate the sum of their total sizes. In the example above, these directories are
a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this example,
this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum of
the total sizes of those directories?

Solution: 1325919
"""

input_file = "input.txt"

class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def get_size(self):
        return self.size

    def is_folder(self):
        return False

    def __str__(self):
        return "File " + self.name + str(self.size)

class Folder:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = {}
        self.size = None

    def add_child(self, child):
        self.children[child.name] = child

    def get_size(self):
        if self.size == None:
            size = 0
            for child in self.children.values():
                size += child.get_size()
                self.size = size
        return self.size

    def is_folder(self):
        return True

    def __str__(self):
        return "Folder " + self.name + " " + str(self.get_size())

    def __repr__(self):
        return "Folder " + self.name + " " + str(self.get_size())

def build_file(name, size):
    return File(name, size)


def build_folder(name, parent):
    return Folder(name, parent)

def build_directory(f):
    line = f.readline().strip().split(" ")
    curr = build_folder(line[1], None)

    line = f.readline().strip().split(" ")
    while (line):
        if (line[0] == "$"):
            if (line[1] == "cd"):
                if (line[2] == ".."):
                    curr = curr.parent
                else:
                    curr = curr.children[line[2]]
        elif (line[0] == "dir"):
            curr.add_child(build_folder(line[1], curr))
        elif (line[0] == ""):
            break
        else:
            curr.add_child(build_file(line[1], int(line[0])))

        line = f.readline().strip().split(" ")

    while (curr.parent != None):
        curr = curr.parent
    return curr

def get_totals(root):
    total = 0

    size = root.get_size()
    if (size <= 100000):
        total += size

    for child in root.children.values():
        if child.is_folder():
            total += get_totals(child)
    return total


def get_directories_total(input_file):
    f = open(input_file, "r")
    root = build_directory(f)
    
    totals = 0
    for child in root.children.values():
        if child.is_folder():
            child_totals = get_totals(child)
            totals += child_totals
    return totals
print("Totals: {}".format(get_directories_total(input_file)))

"""
Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000. To run the update, you
need unused space of at least 30000000. You need to find a directory you can delete
that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the total
amount of used space) is 48381165; this means that the size of the unused space must
currently be 21618835, which isn't quite the 30000000 required by the update.
Therefore, the update still requires a directory with total size of at least 8381165
to be deleted before it can run.

To achieve this, you have the following options:

    Delete directory e, which would increase unused space by 584.
    Delete directory a, which would increase unused space by 94853.
    Delete directory d, which would increase unused space by 24933642.
    Delete directory /, which would increase unused space by 48381165.

Directories e and a are both too small; deleting them would not free up enough space.
However, directories d and / are both big enough! Between these, choose the smallest:
d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the
filesystem to run the update. What is the total size of that directory?

Solution: 2050735
"""

def get_smallest_folder_size(root):
    size = root.get_size()
    return size - 40000000

def get_folders(folders, root, min_size):
    size = root.get_size()
    if (size > min_size):
        folders.append(root)

    for child in root.children.values():
        if child.is_folder():
            get_folders(folders, child, min_size)
    return folders

def get_smallest_folder_to_delete(input_file):
    f = open(input_file, "r")
    root = build_directory(f)

    min_size = get_smallest_folder_size(root)
    
    folders = []
    for child in root.children.values():
        if child.is_folder():
            get_folders(folders, child, min_size)
    folders.sort(key= lambda x: x.get_size())
    return folders[0]
print("Totals: {}".format(get_smallest_folder_to_delete(input_file)))
