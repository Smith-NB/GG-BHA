#!/usr/bin/env python3

import os, sys
import numpy as np


num_hops = 0
num_incompletetrials = 0
for roots, dirs, files in os.walk(os.getcwd()):
	dirs.sort()
	for d in dirs:
		if d.startswith("Trial"):
			os.chdir(d)

			if not os.path.exists('bha_running.lock'): 
				os.chdir('..')
			else:
				num_incompletetrials += 1
				num_hops += sum(1 for line in open('log.txt'))
				os.chdir('..')

		sys.stdout.write("\r                                                                  ")
		sys.stdout.flush()
		sys.stdout.write("\rChecked " + str(d) + ".")
		sys.stdout.flush()
	break

t = num_hops/num_incompletetrials

halflife = t/(np.log10(num_incompletetrials/100)/np.log10(0.5))
meanlifetime = halflife/np.log(2)
print()
print("halflife: %f" % halflife)
print("meanlifetime: %f" % meanlifetime)