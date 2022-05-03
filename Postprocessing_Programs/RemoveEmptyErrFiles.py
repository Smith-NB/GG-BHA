#!/usr/bin/env python3

import os, sys

count = 0
for root, dirs, files in os.walk(os.getcwd()):
	for f in files:
		if f.startswith("arrayJob_") and f.endswith(".err"):
			print(os.path.join(root, f))
			print(os.path.join(dirs, f))
			count += 1

print(count)
