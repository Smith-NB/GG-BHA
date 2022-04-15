#!/usr/bin/env python3
import matplotlib.pyplot as plt
import os, sys
sims = []

if os.path.exists("sim_to_GM.txt"):
	exit()
else:
	from ase.io.trajectory import Trajectory
	from BHA.T_SCM_Methods import get_CNA_profile, get_CNA_similarity
	import numpy as np
	traj = Trajectory("local_minima.traj")
	GM = traj[-1]
	GM_CNA = get_CNA_profile((GM, [1.3549]))
	x = []
	i = 0
	for cluster in traj:
		cna = get_CNA_profile((cluster, [1.3549]))
		sims.append(get_CNA_similarity(GM_CNA, cna))
		i += 1

	np.savetxt("sim_to_GM.txt", sims, fmt="%f")
