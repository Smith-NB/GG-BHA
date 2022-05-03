#!/usr/bin/env python3

import os, sys

count = 0
for root, dirs, files in os.walk(os.getcwd()):
	for f in files:
		if f.startswith("arrayJob_") and f.endswith(".err"):
			fpath = os.path.join(root, f)
			if os.stat(fpath).st_size == 0:
				print(fpath)
				count += 1

print(count)
