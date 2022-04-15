#!/usr/bin/env python3

import os, sys
path = os.getcwd()
for item in os.listdir(path):
	if item.startswith('arrayJob_') and item.endswith('.out'):
		file = open(item)
		break

print("Hop to find: ")
hop_to_find = int(input())
a = 0
for line in file:
	if line.startswith("Attempting step " + str(hop_to_find)):
		break
	elif line.startswith("The current step has been accepted."):
		a += 1
print(a)