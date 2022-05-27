"""

This script is for quickly converting some of the java bytes into python byte arrays

"""


import re


temp = """

"""
source = """
           code[0] = 126;
            code[1] = 5;
            code[2] = 3;
            code[3] = model;
            code[4] = 4;
            code[5] = 255;
            code[6] = 255;
            code[8] = 239;

"""

data = [None] * 100

for lineno, line in enumerate(source.strip().split('\n')):
    if line.strip() == '':
        continue

    match = re.match(r'\s*code\w*\[(\d+)\] = (.*);$', line)
    if not match:
        print(f"{lineno:3d}: Badline {line}")
        continue

    data[int(match.group(1))] = match.group(2)

while len(data) and data[-1] is None:
    del data[-1]

for i in range(len(data)):
    if data[i] is None:
        data[i] = "0"

print(f"bytes([{', '.join(data)}])")
