#!/usr/bin/env python3

from ase.io.trajectory import Trajectory
from BHA.T_SCM_Methods import get_CNA_profile, get_CNA_similarity
from ase.io import write
import numpy as np
import os, sys, getopt

traj = Trajectory("local_minima.traj")
GM = traj[-1]
GM_CNA = get_CNA_profile((GM, [1.3549]))

x = []
i = 0
saved_clusters = 0
sims = []
for cluster in traj:
	cna = get_CNA_profile((cluster, [1.3549]))
	sims.append(get_CNA_similarity(GM_CNA, cna))
	sys.stdout.write("\r                                                                  ")
	sys.stdout.flush()
	sys.stdout.write("\r" + str(i))
	sys.stdout.flush()
	if sims[-1] >= 40 and sims[-1] != sims[-2]:
		write(filename=str(i) + "_" + str(round(sims[-1], 1)) + ".xyz", images = cluster, format='xyz')
		saved_clusters += 1
	i += 1
#np.savetxt("sim_to_GM.txt", sims, fmt="%f")