#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import os, sys, getopt
from ase.io import read
from BHA.T_SCM_Methods import get_CNA_profile, get_CNA_similarity
from Postprocessing_Programs.ClusterStructures import get_structure
from asap3.Internal.BuiltinPotentials import LennardJones

log = open("GM_located_freq.txt", "a")

for roots, dirs, files in os.walk(os.getcwd()):
	dirs.sort()
	for d in dirs:
		curr_GM_freq = 0
		print("Moving to " + d)
		os.chdir(d)
		if os.path.exists("sim_to_GM.txt"):
			sim_file = open("sim_to_GM.txt")
			for line in sim_file:
				if float(line.rstrip()) == 100:
					curr_GM_freq += 1
		log.write(d + ": " + str(curr_GM_freq) + "\n")
		os.chdir("..")
	break

log.flush()
log.close()