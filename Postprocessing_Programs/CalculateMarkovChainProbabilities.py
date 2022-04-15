#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import re as regex
from matplotlib import cm
import os, sys, getopt
from ase.io import read
from BHA.T_SCM_Methods import get_CNA_profile, get_CNA_similarity
from Postprocessing_Programs.ClusterStructures import get_structure
from asap3.Internal.BuiltinPotentials import LennardJones
from itertools import zip_longest
#Energy and similarity boundries for the regions of the PES
def get_region_LJ38(s, e):
	if s == 100:
		return 0
	elif s >= 80 and e < -170.5:
		return 6
	elif s >= 80 and e >= -170.5:
		return 5# if e < -167 else 10
	elif s >= 60 and s < 80:
		return 4# if e < -167 else 9
	elif s >= 40 and s < 60:
		return 3# if e < -167 else 8
	elif s < 40 and e >= -172.80:
		return 2# if e < -167 else 7
	elif s < 40 and e < -172.80:
		return 1

def get_region_LJ75(s, e):
	if s == 100:
		return 0
	elif s >= 85:
		return 11 if e >= -393.5 else 12
	elif s >= 62.5 and s < 85:
		return 9 if e > -385 else 10
	elif s >= 55 and s < 62.5:
		return 7 if e > -385 else 8
	elif s >= 45 and s < 55:
		return 5 if e > -385 else 6
	elif s >= 27.5 and s < 45 :
		return 3 if e > -385 else 4
	elif e < 27.5:
		return 1 if e > -385 else 2


def get_region_LJ98(s, e):
	if s == 100:
		return 0
	elif s >= 93:
		return 11 if e > -540 else 12
	elif s >= 80:
		return 10
	elif s >= 65 and s < 80:
		return 8 if e > -528 else 9
	elif s >= 55 and s < 65:
		return 6 if e > -528 else 7
	elif s >= 45 and s < 55:
		return 4 if e > -528 else 5
	elif s >= 27.5 and s < 45:
		return 2 if e > -528 else 3
	else:
		return 1

def get_region_LJ98_improved(sGM, s2, e):
	crude_region = get_region_LJ98(sGM, e)
	if crude_region == 7:
		if s2 > 42.5: 
			return 7
		elif s2 < 29:
			return 5
		else: 
			return 9
	elif crude_region == 5:
		if s2  < 45:
			return 5
		else:
			return 3
	elif crude_region == 9:
		if s2 < 42.5:
			return 9
		else:
			return 7
	else:
		return crude_region

n_regions = None
#Get user input for energy cont.
print("Get deformation or MetC values (def/MetC):", end='')
mode = None
while mode is None:
	try:
		mode = input()
		if mode != "def" and mode != "MetC":
			raise ValueError("Value must be 'def' or 'MetC'.")
	except ValueError:
		mode = None
		print("Please input either 'def' or 'MetC'.")
if mode == "def":
	similarity_ref = "self"
if mode == "MetC":
	print("Input the temperature (kT): ", end='')
	kT = None
	while kT is None:
		try:
			kT = float(input())
			if kT == 0:
				raise ValueError("Value cannot be 0")
		except ValueError:
			kT = None
			print("Please input a non-zero numerical value.")

	print("Input the energy contribution (c_E): ", end='')
	c_E = None
	while c_E is None:
		try:
			c_E = float(input())
			if c_E > 1 or c_E < 0:
				raise ValueError("Value is not between 0-1.")
		except ValueError:
			c_E = None
			print("Please input a decimal value between 0.0 and 1.0 (incl.).")



	#Get user input for strurctural similarity cont.
	print("Input the structure contribution (c_SCM): ", end='')
	c_SCM = None
	while c_SCM is None:
		try:
			c_SCM = float(input())
			if c_SCM > 1 or c_SCM < 0:
				raise ValueError("Value is not between 0-1.")
		except ValueError:
			c_SCM = None
			print("Please input a decimal value between 0.0 and 1.0 (incl.).")

#Get user input for the cluster being studied
print("Input the cluster formula (LJ38/LJ75/LJ98/(+)): ", end='')
formula = None
while formula is None:
	try:
		formula = input()
		if formula != "LJ38" and formula != "LJ75" and formula != "LJ98" and formula != "LJ98+":
			raise ValueError("Must use LJ38, LJ75 or LJ98.")
	except ValueError:
		formula = None
		print("Must use LJ38, LJ75 or LJ98 (case sensitive).")
	if formula == "LJ38": 
		n_regions = 7
		get_region = get_region_LJ38
	elif formula == "LJ75": 
		n_regions = 13
		get_region = get_region_LJ75
	elif formula == "LJ98":
		n_regions = 13
		get_region = get_region_LJ98
	elif formula == "LJ98+":
		n_regions = 13
		get_region = get_region_LJ98_improved
ref_name = None
if formula.endswith('+'):
	valid_ref_names = ['FCC1', 'FCC2']
	print("Please input the reference structure name: ", end='')
	while ref_name is None:
		try:
			ref_name = input()
			if not ref_name in valid_ref_names:
				raise ValueError("2nd reference structure must be in list: " + str(valid_ref_names))
		except ValueError:
			ref_name = None
			print("2nd reference structure must be in list: " + str(valid_ref_names))
	ref = None
	if ref_name == "FCC1":
		ref = get_structure(formula.replace('+','') + "_FCCs")[0]
	elif ref_name == "FCC2":
		ref = get_structure(formula.replace('+','') + "_FCCs")[1]
	ref.cna = get_CNA_profile((ref, [1.3549]))
#Get user input for the reference used for similarity (self, or a population).
if mode == "MetC":
	print("What is the reference for structural similarity (self/pop): ", end='')
	similarity_ref = None
	while similarity_ref is None:
		try:
			similarity_ref = input()
			if similarity_ref != "self" and similarity_ref != "pop":
				raise ValueError("Must use self or pop.")
		except ValueError:
			similarity_ref = None
			print("Must use self or a_priori_pop_" + formula + ".")

	if similarity_ref == "pop":
		similarity_ref = "a_priori_pop_" + formula
		add_or_sub = None
		print("Additive or subractive popoulation MetC? (+/-): ", end='')
		while add_or_sub is None:
			try:
				add_or_sub = input()
				if add_or_sub != '+' and add_or_sub != '-':
					raise ValueError("Must input '+' or '-'.")
			except:
				print("Must input '+' or '-'.")
	else:
		add_or_sub = '+'

#setup
alpha = 1
hops_to_region = []
for i in range(n_regions):
	hops_to_region.append([])
	for j in range(n_regions):
		if mode == "MetC":
			hops_to_region[i].append([])
		elif mode == "def":
			hops_to_region[i].append(0)

#Special case for LJ38
dirs_to_check = None
"""
if os.path.exists("dirs_to_check.txt"):
	dirs_to_check_file = open("dirs_to_check.txt")
	dirs_to_check = []
	for line in dirs_to_check_file:
		dirs_to_check.append(line.rstrip())
"""
GM = get_structure(formula.replace('+', '') + "_GM")
GM.cna = get_CNA_profile((GM, [1.3549]))
pattern = regex.compile("\d+\.\d[_]\d+\.\d+")
for roots, dirs, files in os.walk(os.getcwd()):
	dirs.sort()
	for d in dirs:

		#If the dir name is not correctly formatted, skip it.
		if not pattern.match(d): continue

		#Special case for LJ38
		if dirs_to_check is not None and d not in dirs_to_check:
			continue

		#change working dir to next seed cluster
		os.chdir(d)
		sys.stdout.write("\r                                                  ")
		sys.stdout.flush()
		sys.stdout.write("\r%s" % d)
		sys.stdout.flush()
		cluster_file = None
		#find xyz file of seed cluster
		for item in os.listdir(os.getcwd()):
			if item.endswith(".xyz"):
				cluster_file = item
				break
		
		#for debugging
		if cluster_file is None: print(d)

		#read the seed cluster file and get energy, similiarity to GM
		if os.path.exists(cluster_file):
			cluster = read(cluster_file)
			elements = [10]; sigma = [1]; epsilon = [1]; rCut = 1000;
			lj_calc = LennardJones(elements, epsilon, sigma, rCut=rCut, modified=True)
			cluster.set_calculator(lj_calc)
			marked_energy = cluster.get_potential_energy()
			marked_CNA = get_CNA_profile((cluster, [1.3549]))
			marked_sim = get_CNA_similarity(marked_CNA, GM.cna)
			if formula.endswith('+'):
				marked_refsim = get_CNA_similarity(marked_CNA, ref.cna)
		path = os.getcwd()
		sims_GM = []
		sims = []
		energies = []
		sims_ref = []

		if os.path.exists("sim_to_GM.txt"):
			sim_file = open("sim_to_GM.txt")
			for line in sim_file:
				sims_GM.append(float(line.rstrip()))
			sim_file.close()
		else:
			print(d)
		
		if ref_name is None:
			pass
		elif ref_name == "FCC1" and os.path.exists("sim_to_Oh.txt"):
			simref_file = open("sim_to_Oh.txt")
			for line in simref_file:
				sims_ref.append(float(line.rstrip()))
			sim_file.close()
		else:
			print(d); exit()

		if os.path.exists("SS_log.txt"):
			log_file = open("SS_log.txt")
			if similarity_ref == "self":
				for line in log_file:
					energies.append(float(line.rstrip().split()[3][:-1]))
					sims.append(float(line.rstrip().split()[5]))
			else:
				for line in log_file:
					energies.append(float(line.rstrip().split()[3][:-1]))
		else:
			print(d)

		if similarity_ref == "a_priori_pop_" + formula:
			sim_to_pop_file = open("sim_to_a_priori.txt")
			for line in sim_to_pop_file:
				sims.append(float(line.rstrip()))
			sim_to_pop_file.close()

		combined = []
		frequencies = []
		reg_c = []
		colours = ["#FF0000", "#660099", "#006699", "#006600", "#800000", "#FF9900", "#3333CC",
				"#009999", "#009900", "#000000", "#99FF00"]
		marked_region = get_region(marked_sim, marked_refsim, marked_energy) if formula.endswith('+') else get_region(marked_sim, marked_energy)
		
		if mode == "MetC":
			for s, s_GM, s_ref, e in zip_longest(sims, sims_GM, sims_ref, energies):
				curr_region = get_region(s_GM, s_ref, e) if formula.endswith('+') else get_region(s_GM, e)
				if e <= marked_energy:
					prob = 1
				else:
					E_cont = np.exp((marked_energy - e) / kT) * c_E - 0.1
					if add_or_sub == '+':
						SCM_cont = (1-s/100) * c_SCM
					elif add_or_sub == '-':
						SCM_cont = -1 * s/100 * c_SCM
						#print(SCM_cont)
					prob = E_cont + SCM_cont
					if prob < 0: 
						prob = 0

				hops_to_region[marked_region][curr_region].append(prob)
		elif mode == "def":
			for s, s_GM, s_ref, e in zip_longest(sims, sims_GM, sims_ref, energies):	
				curr_region = get_region(s_GM, s_ref, e) if formula.endswith('+') else get_region(s_GM, e)
				hops_to_region[marked_region][curr_region] += 1		
			#ifelse is redundant but am too scared to remove
			"""
			if round(s_GM, 1) == round(marked_sim, 1) and round(e, 1) == round(marked_energy,1):
				#continue
				hops_to_region[marked_region][curr_region].append(prob)
			else:
				hops_to_region[marked_region][curr_region].append(prob)
			"""

		os.chdir('..')
		"""
		entry = [s, round(e, 1)]
		combined.append(entry)
		if entry == (marked_sim, round(marked_energy, 1)) or combined.count(entry) < 5:
			frequencies.append(1)
		elif combined.count(entry) >= 5:
			frequencies.append(2)
		"""

	break

print()
for i in range(n_regions):
	print("\t%5d" % i, end='')
print("\n-------------------------------------------------------------------------------------------------------")
if mode == "MetC":
	for i in range(n_regions):
		region_sum = 0
		region_len = 0
		print("%4d:\t" % i, end='')
		for j in range(n_regions):
			try:
				print("%4.1f\t" % ((sum(hops_to_region[i][j])/len(hops_to_region[i][j]))*100), end='')
			except ZeroDivisionError:
				print("%4.1f\t" % 0, end='')
			region_sum += sum(hops_to_region[i][j])
			region_len += len(hops_to_region[i][j])
		print("%1.4f" % ((region_sum/region_len)))
elif mode == "def":
	for i in range(n_regions):
		print("%4d:\t" % i, end='')
		for j in range(n_regions):
			print("%4.1f\t" % (hops_to_region[i][j]/sum(hops_to_region[i])*100), end='')
		print()

			

