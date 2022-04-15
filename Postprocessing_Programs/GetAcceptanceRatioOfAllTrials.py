#!/usr/bin/env python3

import os, sys
import numpy as np
import scipy.stats

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    ci = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, ci



trials_checked = 0
steps = 0
accepted = 0
path = os.getcwd()
for root, dirs, files in os.walk(path, topdown=True):
	dirs.reverse()
	for d in dirs:
		if d.startswith('Trial') and d.replace('Trial', '').isdigit():
			trials_checked += 1
			f = open(root + "/" + d + "/log.txt", "r")
			for line in f:
				if line == "RESEED":
					pass
				elif 'True' in line:
					accepted += 1
					steps += 1
				else:
					steps += 1


			###########
			sys.stdout.write("\r                                                                  ")
			sys.stdout.flush()
			sys.stdout.write("\rChecked " + str(d) + ".")
			sys.stdout.flush()
			###########	
			f.close()
		
	break

print('\n')
print(accepted)
print(steps)
print(accepted/steps)
