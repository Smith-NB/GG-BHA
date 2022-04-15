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
path = os.getcwd()
c = []
for root, dirs, files in os.walk(path, topdown=True):
	dirs.reverse()
	for d in dirs:
		if d.startswith('Trial') and d.replace('Trial', '').isdigit():
			trials_checked += 1
			logfile = None
			for item in os.listdir(d):
				if item.startswith('arrayJob_'):
					logfile = item
			if logfile is not None:
				f = open(root + "/" + d + "/" + logfile, "r")
			else:
				continue
			for line in f:
				#print(line.startswith('Chance'))
				if line.startswith('Attempting step'):
					steps += 1
				elif line.startswith('Chance'):
					c.append(float(line.split()[4]))


			###########
			sys.stdout.write("\r                                                                  ")
			sys.stdout.flush()
			sys.stdout.write("\rChecked " + str(d) + ".")
			sys.stdout.flush()
			###########	
			f.close()
		
	break

print('\n')
print(mean_confidence_interval(c))
print((steps-len(c))/steps)
