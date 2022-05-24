#!/usr/bin/env python3

import os, sys


rounding = None
print("Please input the rounding to use: ", end='')
while rounding is None:
	try:
		rounding = int(input())
	except ValueError:
		rounding = None
		print("Please input an integer value: ", end='')

target_energy = None
print("Please input the target energy to search for: ", end='')
while target_energy is None:
	try:
		target_energy = float(input())
	except ValueError:
		target_energy = None
		print("Please input a numerical value: ", end='')



t = []
status = []

for roots, dirs, files in os.walk(os.getcwd()):
	dirs.sort()
	for d in dirs:
		if not d.startswith("Trial"): continue
		sys.stdout.write("\r%s        " % d)
		sys.stdout.flush()
		log = open("%s/log.txt" % d)
		n_reseeds = 0
		target_found = False
		for line in log:
			if line.startswith("RESEED"):
				n_reseeds += 1
				continue
			e = float(line.split()[3][:-1])
			step = int(line.split()[1][:-1])
			if round(e, rounding) == round(target_energy, rounding):
				target_found = True
				break
		t.append(step + n_reseeds)
		status.append(1 if target_found else 0)
		log.close()
	break

print()
resultsfile = open("_CensoredData_%f" % -target_energy)
t, status = zip(*sorted(zip(t, status)))
for i in range(len(t)):
	print("%d\t%d" % (t[i], status[i]))
	resultsfile.write("%d\t%d" % (t[i], status[i]))

resultsfile.close()




