#!/usr/bin/env python3

import os, sys
import numpy as np
import scipy.stats

def mean_confidence_interval(data, confidence=0.95):
	a = 1.0 * np.array(data)
	n = len(a)
	m, se = np.mean(a), scipy.stats.sem(a)
	ci = se * scipy.stats.t.ppf((1 + confidence) / 2., n-2)
	return m, ci

def linear_regression_confidene_interval(data, N0, confidence=0.95):
	#If trials are all complete
	if len(data) == N0:
		x = data[:-1] #discount final trial, as N(t) == 0 and ln(N(t)) == ln(0) == UNDEFINED
	else:
		x = data
	y = [] #N(t), i.e. number of trials remaining
	for i in range(len(x)):
		y.append(np.log(N0-i-1))
	lin_reg = scipy.stats.linregress(x, y)
	ci_lambda = lin_reg.stderr * scipy.stats.t.ppf((1 + confidence) / 2., len(x)-2)
	ci_rel = ci_lambda/lin_reg.slope

	tau = -1/lin_reg.slope
	ci_tau = -tau * ci_rel
	return tau, ci_tau

print("Please input energy rounding (dp): ", end='')
dp_rounding = None
while dp_rounding is None:
	try: 
		dp_rounding = int(input())
	except ValueError:
		print("Please use a integer value: ", end='')
		dp_rounding = None

print("Please input target energies to look for\n(comma delimted or leave blank for LES): ", end='')
target_energies = None
while target_energies is None:
	target_energies = input().split(',')
	try:
		if target_energies == ['']:
			target_energies = []
		else:
			for i in range(len(target_energies)):
				target_energies[i] = round(float(target_energies[i]), dp_rounding)

	except ValueError:
		print("Please input only numerical values seperated solely by commas, or no input:")
		target_energies = None

if len(target_energies) == 0:
	target_string = "LES"
else:
	target_string = ""
	for i in range(len(target_energies)):
		target_string += str(target_energies[i])

fname = "_GetMeanLifetimeOfAllTrialsOutput_targets_%s.txt" % target_string
f = open(fname, "w")
num_mins = []
last_target_found = []
trials = []
for roots, dirs, files in os.walk(os.getcwd()):
	dirs.sort()
	for d in dirs:
		if not d.startswith("Trial"): continue
		
		sys.stdout.write("\r                   ")
		sys.stdout.flush()
		sys.stdout.write("\rParsing %s" % d)
		sys.stdout.flush()

		os.chdir(d)
		log = open("log.txt", "r")
		e_min = float('inf')
		e_min_step = 0
		reseed_count = 0
		target_found_steps = []
		for i in range(len(target_energies)):
			target_found_steps.append(False)
		for line in log:
			if "RESEED" in line: 
				reseed_count += 1
				continue
			e = round(float(line.split()[3].strip().replace(',', '')), dp_rounding)
			for i in range(len(target_energies)):
				if e == target_energies[i] and not target_found_steps[i]:
					target_found_steps[i] = int(line.split()[1].strip().replace(',', '')) + reseed_count


		m = 0
		for i in range(1, len(target_found_steps)):
			if target_found_steps[i] < target_found_steps[m]:
				m = i
		last_target_found.append(min(m))
		num_mins.append(target_found_steps[m])
		trials.append(d)
		log.close()
		os.chdir('..')

	break
print()
last_target_found, num_mins, trials = (list(x) for x in zip(*sorted(zip(last_target_found, num_mins, trials))))
overall_LES = last_target_found[0]
overall_LES_num_mins = []
for i in range(len(num_mins)):
	#print("%s %d %f" % (trials[i], num_mins[i], last_target_found[i]))
	if last_target_found[i] == overall_LES:
		overall_LES_num_mins.append(num_mins[i])

mean, mean_ci = mean_confidence_interval(overall_LES_num_mins)
tau, tau_ci = linear_regression_confidene_interval(overall_LES_num_mins, len(trials))
alt_tau, alt_tau_ci = linear_regression_confidene_interval(overall_LES_num_mins[:int(-len(overall_LES_num_mins)*0.1)], len(trials))

f.write("Trial\tNo. mins\tLES Energy\n")
for t, n, e in zip(trials, num_mins, last_target_found):
	f.write("%9s\t%8d\t%6.2f\n" % (t, n, e))
f.write("------------------------------------------------------\n")
f.write("------------------------------------------------------\n")
f.write("Trials that have not completed yet:")
for i in range(len(overall_LES_num_mins), len(trials)):
	f.write("%s," % trials[i].replace("Trial", ""))
f.write("\n------------------------------------------------------\n")
f.write("------------------------------------------------------\n")
f.write("Overall Details\n")
f.write("LES: %.2f energy units\n" % overall_LES)
f.write("No. of trials that discovered this LES: %d of %d\n" % (len(overall_LES_num_mins), len(trials)))
f.write("Mean no. of mins needed to find this LES of the %d successful trials: %.1f +- %.1f\n" % (len(overall_LES_num_mins), round(mean, 1), round(mean_ci, 1)))
f.write("Mean lifetime of %d successful trials: %.1f +- %.1f\n" % (len(overall_LES_num_mins), round(tau, 1), round(tau_ci, 1)))
f.write("Mean lifetime of %d successful trials: %.1f +- %.1f (calculated excluding final 10 %% of completed trials)\n" % (len(overall_LES_num_mins), round(alt_tau, 1), round(alt_tau_ci, 1)))
f.write("------------------------------------------------------\n")
f.write("------------------------------------------------------\n")
f.close()
f = open(fname, "r")
for line in f:
	print(line, end='')
