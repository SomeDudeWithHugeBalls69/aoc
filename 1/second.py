#!/usr/bin/env python3
# -*- coding: utf-8 -*-

with open("input_first.txt", "r") as f:
    lines = f.read().splitlines()

calories = []

cur_sum = 0
for line in lines:
    if line == "":
        calories.append(cur_sum)
        cur_sum = 0
    else:
        cur_sum += int(line)

print(sum(sorted(calories)[-3:])) # 208191
