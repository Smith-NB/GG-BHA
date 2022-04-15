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

"""
print("Minimum similarity to GM: ")
try:
	min_sim = float(input())
except ValueError:
	print("ValueError: Must input an int or float")
	sys.exit(2)
"""
trials_checked = 0
total_hop_count = 0
path = os.getcwd()
for i in range(50, 95, 5):
	min_sim = i
	hops_into_GM_well = 0
	for root, dirs, files in os.walk(path, topdown=True):
		dirs.sort()
		#dirs.reverse()
		for d in dirs:
			if d.startswith('Trial') and d.replace('Trial', '').isdigit() and int(d.replace('Trial', '')) > 0 and int(d.replace('Trial', '')) <= 100:
				trials_checked += 1
				if os.path.exists(root + "/" + d + "/sim_to_GM.txt"):
					f = open(root + "/" + d + "/sim_to_GM.txt", "r")
					at_GM_well = False
					for line in f:
						if float(line.rstrip()) >= min_sim and at_GM_well:
							pass
						elif float(line.rstrip()) >= min_sim:
							at_GM_well = True
							hops_into_GM_well += 1
						elif at_GM_well:
							at_GM_well = False
						total_hop_count += 1
					f.close()
				else:
					pass

				###########
				sys.stdout.write("\r                                                                  ")
				sys.stdout.flush()
				sys.stdout.write("\rChecked " + str(d) + ".")
				sys.stdout.flush()
				###########	
				
			
		break

	#print("\nThis program is set to only check the first 100 trials.")
	print()
	print(min_sim)
	print(hops_into_GM_well/100)
	print(hops_into_GM_well/total_hop_count)
	print('\n')
