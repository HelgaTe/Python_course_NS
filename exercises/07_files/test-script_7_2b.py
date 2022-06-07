#!/usr/bin/env python3

ignore = ["duplex", "alias", "configuration"]

# переменная f ссылается на реальный файл

from sys import argv

in_file = argv[1]
out_file = argv[2]

with open (in_file) as src, open(out_file, 'w') as dest:
    for line in src:
            words=line.split()
            intersect=set(words)&set(ignore)
            if not line.startswith('!') and not intersect:
                dest.write(line)
