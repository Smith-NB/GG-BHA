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
		if d.startswith("ico"):
			print("Moving to " + d)
			os.chdir(d)
			cluster_file = None
			for item in os.listdir(os.getcwd()):
				if item.endswith(".xyz"):
					cluster_file = item
					break
			if os.path.exists(cluster_file):
				os.rename(cluster_file, d + ".xyz")
			os.chdir("..")
	break