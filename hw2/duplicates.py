import sys
from os import walk, path
from hashlib import sha1 as hasher
from collections import defaultdict


def hash_file(filename):
    f = open(filename, mode="rb")
    hash = hasher()
    while True:
        chunk = f.read(2 ** 15)
        if not chunk:
            break
        hash.update(chunk)
    return hash.hexdigest()


def main():
    if len(sys.argv) != 2:
        print('usage: ./duplicates.py top_dir')
        sys.exit(1)

    top_dir = sys.argv[1]
    hash_map = defaultdict(list)
    for dir_name, _, files in walk(top_dir):
        for file in files:
            filename = path.join(dir_name, file)
            hash = hash_file(filename)
            hash_map[hash].append(filename)

    for files in hash_map.values():
        if len(files) > 1:
            print(':'.join(files))

if __name__ == '__main__':
    main()
