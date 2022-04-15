#!/usr/bin/env python3

import os, sys
import numpy as np

e = [-173.25, -173.13, -172.96, -172.88]
hops_to_ico = 0
for roots, dirs, files in os.walk(os.getcwd()):
	dirs.sort()
	for d in dirs:
		if not d.startswith("Trial"): continue

		os.chdir(d)
		sys.stdout.write("\r                 ")
		sys.stdout.flush()
		sys.stdout.write("\r%s" % d)
		sys.stdout.flush()
		log = open("log.txt", "r")
		curr_E = float(log.readline().strip().split()[3][:-1])
		for line in log:
			if "RESEED" in line: continue
			cand_E = float(line.strip().split()[3][:-1])
			if "accepted True" in line: 
				if round(cand_E, 2) in e and round(cand_E, 2) != round(curr_E, 2):
					hops_to_ico += 1
				curr_E = cand_E
		os.chdir("..")
print()
print(hops_to_ico)
