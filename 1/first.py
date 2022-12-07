#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open("input_first.txt", "r") as f:
    lines = f.read().splitlines()

max_val = -1
cur_sum = 0
for line in lines:
    if line == "":
        if max_val < cur_sum:
            max_val = cur_sum
        cur_sum = 0
    else:
        cur_sum += int(line)

print(max_val) # 71502
