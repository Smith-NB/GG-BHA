#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import os, sys, getopt
from ase.io import read
from BHA.T_SCM_Methods import get_CNA_profile, get_CNA_similarity
from Postprocessing_Programs.ClusterStructures import get_structure
from asap3.Internal.BuiltinPotentials import LennardJones


for roots, dirs, files in os.walk(os.getcwd()):
	for d in dirs:
		print("Moving to " + d)
		os.chdir(d)

		cluster_file = None
		for item in os.listdir(os.getcwd()):
			if item.endswith(".xyz"):
				cluster_file = item
				break
		if os.path.exists(cluster_file):
			cluster = read(cluster_file)
			elements = [10]; sigma = [1]; epsilon = [1]; rCut = 1000;
			lj_calc = LennardJones(elements, epsilon, sigma, rCut=rCut, modified=True)
			cluster.set_calculator(lj_calc)
			marked_energy = cluster.get_potential_energy()
			GM = get_structure("LJ38_GM")
			marked_sim = get_CNA_similarity(get_CNA_profile((cluster, [1.3549])), get_CNA_profile((GM, [1.3549])))

		path = os.getcwd()
		sims = []
		energies = []
		if os.path.exists("sim_to_GM.txt"):
			sim_file = open("sim_to_GM.txt")
			for line in sim_file:
				sims.append(float(line.rstrip()))
			sim_file.close()

		if os.path.exists("SS_log.txt"):
			log_file = open("SS_log.txt")
			for line in log_file:
				energies.append(float(line.rstrip().split()[3][:-1]))

		combined = []
		frequencies = []
		for s, e in zip(sims, energies):
			entry = [s, round(e, 1)]
			combined.append(entry)
			if entry == (marked_sim, round(marked_energy, 1)) or combined.count(entry) < 5:
				frequencies.append(1)
			elif combined.count(entry) >= 5:
				frequencies.append(2)
			

		name = cluster_file[:-4] + "_plot.png"
		plt.scatter(sims, energies, s=10, c = frequencies, cmap='bwr')
		plt.xlabel("Similarity (%)")
		plt.ylabel("Energy")
		plt.ylim([-174, -162])
		plt.xlim([0, 100])
		plt.scatter(marked_sim, marked_energy, c="#FF69B4", marker="*")

		plt.savefig(name, dpi=250, bbox_inches = 'tight', pad_inches = 0)
		plt.clf()
		os.chdir("..")
	break