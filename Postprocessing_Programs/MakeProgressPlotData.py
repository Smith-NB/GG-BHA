#!/usr/bin/env python3

from ase.io.trajectory import Trajectory
from BHA.T_SCM_Methods import get_CNA_profile, get_CNA_similarity
from Postprocessing_Programs.ClusterStructures import get_structure
import numpy as np
import matplotlib.pyplot as plt
import sys
import getopt

argv = sys.argv[1:]
print("Starting script")
print(argv)
#try:
opts, args = getopt.getopt(argv, "c:f:")

for opt, arg in opts:
	if opt in ['-c']:
		ref = get_structure(arg)
		if ref is None:
			print("Error; specified structure \'%s\' does not exist." % arg)
			sys.exit()
		ref_CNA = get_CNA_profile((ref, [1.3549]))
	if opt in ['-f']:
		fname = arg
		if os.path.exists(fname):
			print("specified file alread exists. Exiting")
			sys.exit()

#except:
#	print("Error")
#	sys.exit()

sims = []
traj = Trajectory("local_minima.traj")
x = []
i = 0
for cluster in traj:
	cna = get_CNA_profile((cluster, [1.3549]))
	sims.append(get_CNA_similarity(ref_CNA, cna))
	i += 1

np.savetxt(fname, sims, fmt="%f")
