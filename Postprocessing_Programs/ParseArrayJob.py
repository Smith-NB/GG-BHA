#!/usr/bin/env python3

import os, sys
import numpy as np
import scipy.stats

path = os.getcwd()
for item in os.listdir(path):
	if item.startswith('arrayJob_') and item.endswith('.out'):
		file = open(item)
		break
log = open('log.txt', 'r')

step = 0
curr_E = float(log.readline().split()[3][:-1])
new_E = None
sim = None
prob = None

step_arr = []
curr_E_arr = []
new_E_arr = []
sim_arr = []
prob_arr = []

for line in file:
	if line.startswith('Attempting step 0'):
		pass
	elif line.startswith('Attempting step '):
		step_arr.append(step)
		step = int(line.rstrip().split()[2][:-1])
		curr_E_arr.append(curr_E)
		new_E_arr.append(new_E)
		new_E = None
		sim_arr.append(sim)
		sim = None
		prob = 100 if prob is None else prob
		prob_arr.append(prob)
		prob = None
	elif line.startswith('Generated new cluster, E = '):
		new_E = float(line.rstrip().split()[5][:-4])
	elif line.startswith('similarity = '):
		sim = float(line.rstrip().split()[2][:-2])
	elif line.startswith('Chance to accept = '):
		prob = float(line.rstrip().split()[4])*100
	elif line.rstrip().endswith('accepted.'):
		curr_E = new_E

np.savetxt("curr_E.txt", curr_E_arr, fmt="%f")
np.savetxt("step.txt", step_arr, fmt="%d")
try:
	np.savetxt("sim.txt", sim_arr, fmt="%f")
except TypeError:
	print("sims failed")
np.savetxt("new_E.txt", new_E_arr, fmt="%f")
np.savetxt("prob.txt", prob_arr, fmt="%f")
log.close()
file.close()



