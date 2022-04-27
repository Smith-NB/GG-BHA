#!/usr/bin/env python3

import os, sys
import numpy as np
from pandas import DataFrame
import scipy.stats

def mean_confidence_interval(datum, confidence=0.95):
	a = 1.0 * np.array(datum)
	n = len(a)
	m, se = np.mean(a), scipy.stats.sem(a)
	ci = se * scipy.stats.t.ppf((1 + confidence) / 2., n-2)
	return m, ci

def linear_regression_confidene_interval(datum, N0, confidence=0.95):
	#If trials are all complete
	if len(datum) == N0:
		x = datum[:-1] #discount final trial, as N(t) == 0 and ln(N(t)) == ln(0) == UNDEFINED
	else:
		x = datum
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
data = {'trial': [], 'last_encounter_time': []}
target_found_steps = []
for target_energy in target_energies:
	data[target_energy] = []

for roots, dirs, files in os.walk(os.getcwd()):
	dirs.sort()
	for d in dirs:
		if not d.startswith("Trial"): continue
		
		sys.stdout.write("\r                   ")
		sys.stdout.flush()
		sys.stdout.write("\rParsing %s" % d)
		sys.stdout.flush()

		data['trial'].append(d)
		for target_energy in target_energies:
			data[target_energy].append(False)

		log = open("%s/log.txt" % d, "r")
		n_reseeds = 0
		for line in log:
			if "RESEED" in line: 
				n_reseeds += 1
				continue
			e = round(float(line.strip().split()[3][:-1]), dp_rounding)
			for target_energy in target_energies:
				if e == target_energy and data[target_energy][-1] != False:
					data[target_energy][-1] = int(line.strip().split()[1][:-1]) + n_reseeds

		log.close()
		last_encounter_time = 0
		for target_energy in target_energies:
			if data[target_energy][-1] == False:
				last_encounter_time = float('nan')
			elif data[target_energy][-1] > last_encounter_time:
				last_encounter_time = data[target_energy][-1]
		data['last_encounter_time'].append(last_encounter_time)

	break

for target_energy in target_energies:


	"""last_target_found, num_mins, trials = (list(x) for x in zip(*sorted(zip(last_target_found, num_mins, trials))))
				overall_LES = last_target_found[0]
				overall_LES_num_mins = []
				for i in range(len(num_mins)):
					#print("%s %d %f" % (trials[i], num_mins[i], last_target_found[i]))
					if last_target_found[i] == overall_LES:
						overall_LES_num_mins.append(num_mins[i])"""
	num_mins = data[target_energy]
	mean, mean_ci = mean_confidence_interval(num_mins)
	tau, tau_ci = linear_regression_confidene_interval(num_mins, len(data['trial']))
	alt_tau, alt_tau_ci = linear_regression_confidene_interval(num_mins[:int(-len(num_mins)*0.1)], len(data['trial']))

	"""
	f.write("Trial\tNo. mins\tLES Energy\n")
	for t, n, e in zip(trials, num_mins, last_target_found):
		f.write("%9s\t%8d\t%6.2f\n" % (t, n, e))
	f.write("------------------------------------------------------\n")
	f.write("------------------------------------------------------\n")
	f.write("Trials that have not completed yet:")
	for i in range(len(num_mins), len(trials)):
		f.write("%s," % trials[i].replace("Trial", ""))
	"""
	f.write("\n------------------------------------------------------\n")
	f.write("------------------------------------------------------\n")
	f.write("Overall Details\n")
	f.write("Target: %f\n" % target_energy)
	f.write("No. of trials that discovered this LES: %d of %d\n" % (len(num_mins), len(data['trial'])))
	f.write("Mean no. of mins needed to find this LES of the %d successful trials: %.1f +- %.1f\n" % (len(num_mins), round(mean, 1), round(mean_ci, 1)))
	f.write("Mean lifetime of %d successful trials: %.1f +- %.1f\n" % (len(num_mins), round(tau, 1), round(tau_ci, 1)))
	f.write("Mean lifetime of %d successful trials: %.1f +- %.1f (calculated excluding final 10 %% of completed trials)\n" % (len(overall_LES_num_mins), round(alt_tau, 1), round(alt_tau_ci, 1)))
	f.write("------------------------------------------------------\n")
	f.write("------------------------------------------------------\n")
f.close()
f = open(fname, "r")
for line in f:
	print(line, end='')
