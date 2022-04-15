#!/usr/bin/env python3

import os, sys
import matplotlib.pyplot as plt

curr_step = -1
piecewise_accept_counter = 0
E_cont = 0
SCM_cont = 0
accepted = 0
rejected = 0
total_steps = 0
#conts = open("conts.txt", "w")
conts = [[], [], [], []]
for roots, dirs, files in os.walk(os.getcwd()):
	dirs.sort()
	for d in dirs:
		if d.startswith("Trial"):
			os.chdir(d)
			logfilename = None
			for item in os.listdir():
				if item.startswith("arrayJob_") and item.endswith(".out"):
					logfilename = item
			logfile = open(logfilename, "r")
			move_to_next_step = True
			curr_E = float('inf')
			last_E = float('inf')
			for line in logfile:
				if line.startswith("c_E"):
					c_E = float(line.strip().split()[1])
				if line.startswith("c_SCM"):
					c_SCM = float(line.strip().split()[1])
				if move_to_next_step:
					if line.startswith("Attempting step "):
						move_to_next_step = False
						curr_step = int(line.strip().split()[2][:-1])
						total_steps += 1
					else:
						continue
				elif line.startswith("Generated new cluster, E = "):
					last_E = float(line.strip().split()[5])
					if last_E < curr_E:
						curr_E = last_E
						piecewise_accept_counter += 1
						move_to_next_step = True
				elif line.startswith("E_cont = "):
					#conts.write("E: %f " % float(line.strip().split()[2]))
					try:
						conts[0].append(float(line.strip().split()[2]))#*(1/c_E))
					except ZeroDivisionError:
						conts[0].append(float(line.strip().split()[2]))
					E_cont += float(line.strip().split()[2])
				elif line.startswith("SCM_cont = "):
					#conts.write("SCM: %f\n" % float(line.strip().split()[2]))
					conts[1].append(float(line.strip().split()[2]))#*(1/c_SCM))
					SCM_cont += float(line.strip().split()[2])
				elif line.startswith("Chance to accept = "):
					conts[2].append(float(line.strip().split()[4]))
					if conts[2][-1] > 0.01:
						conts[3].append(conts[2][-1])
				elif line.startswith("The current step has been "):
					move_to_next_step = True
					if line.strip().endswith("accepted."):
						curr_E = last_E
						accepted += 1
					elif line.strip().endswith("rejected."):
						rejected += 1
		os.chdir('..')
		"""
		sys.stdout.write("\r                         ")
		sys.stdout.flush()
		sys.stdout.write("\r%s" % d)
		sys.stdout.flush()
		"""
"""
print()
print("%d steps completed" % total_steps)
print("%d steps piecewise accepted" % piecewise_accept_counter)
print(E_cont / (total_steps - piecewise_accept_counter))
print(SCM_cont / (total_steps - piecewise_accept_counter))
print(str(accepted) + " " + str(rejected))
"""

n_bins = 50
bin_dims = []
for i in range(n_bins+1):
	bin_dims.append(round(i*1/n_bins, 2))
# Generate a normal distribution, center at x=0 and y=5
fig, axs = plt.subplots(1, 3, sharey=True, tight_layout=True, figsize=(12,4))
plt.setp(axs, ylim=[0, 1400000])
# We can set the number of bins with the `bins` kwarg
axs[0].hist(conts[0], bins=bin_dims)
axs[0].set_xlabel("Energy Contribution")
axs[0].set_xlim([0,1])
axs[1].hist(conts[1], bins=bin_dims)
axs[1].set_xlabel("Structure Contribution")
axs[1].set_xlim([0,1])
axs[2].hist(conts[2], bins=bin_dims)
axs[2].set_xlabel("Chance to accept")
axs[2].set_xlim([0,1])
"""
fig, axs = plt.subplots(1, 1, sharey=True,  tight_layout=True, figsize=(4,4))
plt.setp(axs, ylim=[0, 500000])

axs.hist(conts[3], bins=bin_dims)
axs.set_xlim([0,1])
"""
#plt.show()
plt.savefig("chance_to_accept_hist_cSCM" + str(c_SCM) + ".png", dpi=200, bbox_inches='tight')
