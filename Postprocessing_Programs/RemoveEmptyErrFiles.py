#!/usr/bin/env python3

import os, sys

for roots, dirs, files in os.walk(os.getcwd()):
	for f in files:
		if f.startswith("arrayJob_") and f.endswith(".err"):
			print(f)
		