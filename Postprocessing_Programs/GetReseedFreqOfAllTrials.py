#!/usr/bin/python

import os, sys
import numpy as np
import scipy.stats

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    ci = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, ci

steps_of_reseed = []
trials_checked = 0
path = os.getcwd()
for root, dirs, files in os.walk(path, topdown=True):
	dirs.reverse()
	for d in dirs:
		if d.startswith('Trial') and d.replace('Trial', '').isdigit():
			trials_checked += 1
			step = 0
			curr_trial_reseeded = False
			step_at_reseed = []
			f = open(root + "/" + d + "/log.txt", "r")
			for line in f:
				if line.rstrip() == "RESEED":
					if curr_trial_reseeded:
						steps_of_reseed.append(step - step_at_reseed[-1])
						step_at_reseed.append(step)
					else:
						steps_of_reseed.append(step)
						step_at_reseed.append(step)
						curr_trial_reseeded = True
				elif line.startswith("step"):
					try:
						step = int(line.split()[1].replace(',', ''))
					except ValueError:
						print('ValueError thrown.')
				else:
					#Throw error?
					pass
			###########
			sys.stdout.write("\r                                                                  ")
			sys.stdout.flush()
			sys.stdout.write("\rChecked " + str(d) + ".")
			sys.stdout.flush()
			###########	
			f.close()
		
	break

print(mean_confidence_interval(steps_of_reseed))
