#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import os, sys, getopt
from ase.io import read
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
def main(argv):
	help_string = 'MakePlot.py [-o] [--options]\n'
	help_string += '\t-h:\tprint this message\n'
	help_string += '\t-d:\tdisplay the plot instead of saving it\n'
	help_string += '\t\tlong option: --display\n'
	help_string += '\t-f:\tfile name of plot (no file extension).\n'
	help_string += '\t\tdefault name = "plot.png"\n'
	help_string += '\t\tlong option: --filename\n'
	help_string += '\t-c:\tColourmap to use.\n'
	help_string += '\t\tdefault colour map = None\n'
	help_string += '\t\tlong option: --cmap\n'
	help_string += '\t-m\tMark a specific cluster on the plot\n'
	help_string += '\t\trequires file of cluster. no default value.\n'
	help_string += '\t\tlong option: --mark_cluster'
	help_string += '\t-n:\tNumber of trials to plot (requires -t)'
	help_string += '\t\tNo default. Required int.'
	help_string += '\t\tlong option: --n_plots'
	help_string += '\t\tI cant be fucked, this only works for -n = 4'
	help_string += '\t-t:\tTrials to plot (requires -n)'
	help_string += '\t\tNo default. Required -n ints. Format: 1,2,...,n (no spaces)'
	help_string += '\t\tlong option: --trials'
	help_string += '\t-a:\tArrangement of subplots. (requires -n)'
	help_string += '\t\tNo default. Format: cols,rows (no spaces)'
	help_string += '\t\tlong option: --arrangement'
	display = False
	cmap = None
	c = None
	steps = []
	name = "plot.png"
	mark_cluster = False
	n_plots = 0
	trials = []
	rows = 0
	cols = 0
	paths = False
	try:
		opts, args = getopt.getopt(argv,"hdp:f:c:m:n:t:a:y:",["display", "paths=", "filename=", "cmap=", "mark_cluster=", "n_plots=", "trials=", "arrangement=", "ylim="])
	except getopt.GetoptError:
		print(help_string)
		sys.exit(2)
	for opt, arg in opts:

		if opt == '-h':
			print(help_string)
			sys.exit()
		elif opt in ("-y", "--ylim"):
			ylow = -float(arg.split(',')[0])
			yhigh = -float(arg.split(',')[1])
		
		elif opt in ("-p", "--paths"):
			paths = True
			n_paths = int(arg)		

		elif opt in ("-d", "--display"):
			display = True

		elif opt in ("-f", "--filename"):
			name = arg
			if not name.endswith(".png"):
				name += ".png"

		elif opt in ("-c", "--cmap"):
			cmap = arg
			if arg is not None and arg is not "None":
				c = steps
			if cmap == "jet_cbt":
				jet = cm.get_cmap('jet_r', 256)
				jet_cb_colors = jet(np.linspace(0, 1, 256))
				prot_matrix = [[56.667, 43.333,  0], [55.833, 44.167,  0], [0, 24.167, 75.833]]
				for i in range(256):
					r = jet_cb_colors[i][0]*prot_matrix[0][0]/100 + jet_cb_colors[i][1]*prot_matrix[0][1]/100 + jet_cb_colors[i][2]*prot_matrix[0][2]/100 
					g = jet_cb_colors[i][0]*prot_matrix[1][0]/100 + jet_cb_colors[i][1]*prot_matrix[1][1]/100 + jet_cb_colors[i][2]*prot_matrix[1][2]/100
					b = jet_cb_colors[i][0]*prot_matrix[2][0]/100 + jet_cb_colors[i][1]*prot_matrix[2][1]/100 + jet_cb_colors[i][2]*prot_matrix[2][2]/100
					jet_cb_colors[i][0] = r
					jet_cb_colors[i][1] = g
					jet_cb_colors[i][2] = b
				jet_cb = ListedColormap(jet_cb_colors)
				cmap = jet_cb
			elif cmap == "jet_cbi":
				nodes = [0.0, 0.1, 0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
				colors = ["#484010", "#8A7B1F", "#AB9819", "#FFE202", "#FEE45A", "#8CA3F4", "#005EC7", "#004694", "#00254E"]
				cmap = LinearSegmentedColormap.from_list("mycmap", list(zip(nodes, colors)))

		elif opt in ("-m", "--mark_cluster"):
			from BHA.T_SCM_Methods import get_CNA_profile, get_CNA_similarity
			from Postprocessing_Programs.ClusterStructures import get_structure
			from asap3.Internal.BuiltinPotentials import LennardJones
			mark_cluster = True
			cluster_file = arg
			if os.path.exists(cluster_file):
				cluster = read(cluster_file)
				elements = [10]; sigma = [1]; epsilon = [1]; rCut = 1000;
				lj_calc = LennardJones(elements, epsilon, sigma, rCut=rCut, modified=True)
				cluster.set_calculator(lj_calc)
				marked_energy = cluster.get_potential_energy()
				GM = get_structure("LJ38_GM")
				marked_sim = get_CNA_similarity(get_CNA_profile((cluster, [1.3549])), get_CNA_profile((GM, [1.3549])))
			else:
				print(cluster_file + " not found.")
				sys.exit(2)

		elif opt in ("-n", "--n_plots"):
			n_plots = int(arg)

		elif opt in ("-t", "--trials"):
			for i in arg.split(','):
				trials.append(int(i))

		elif opt in ("-a", "--arrangement"):
			rc = arg.split(',')
			rows = int(rc[0])
			cols = int(rc[1])

	path = os.getcwd()
	sims = []
	energies = []
	i = 0

	trial_dirs = []
	if n_plots != len(trials):
		print("You must list -n ints after -t. See -h for help.")
		print(n_plots)
		print(len(trials))
		exit(2)
	elif n_plots == 0:
		trial_dirs.append(".")
		dot_size = 10
	else:
		for trial in trials:
			trial_dirs.append("Trial%d/" % trial)
			dot_size = 5
	if rows != 0 and cols != 0:
		fig, axs = plt.subplots(rows, cols, figsize=(10, 2*n_plots))
	else:
		fig, ax = plt.subplots()
		axs = []
		axs.append(ax)

	d_count = 0
	r = 0 
	col = 0
	for d in trial_dirs:
		os.chdir(d)
		"""
		if os.path.exists("sim_to_GM.txt"):
			sim_file = open("sim_to_GM.txt")
			for line in sim_file:
				sims.append(float(line.rstrip()))
				steps.append(i)
				i += 1
			sim_file.close()
		"""
		if os.path.exists("log.txt"):
			log_file = open("log.txt")
			n_steps = 1 #as first hop doesnt count
			for line in log_file:
				n_steps += 1
			to_skip = n_steps-700000
			#to_skip = 0
			c_step = 0
			log_file = open("log.txt")
			reseed_indicies = []
			for line in log_file:
				if "RESEED" in line: 
					reseed_indicies.append(len(energies))
					continue
				c_step += 1
				if c_step < to_skip: continue
				if "accepted True" in line:
					energies.append(float(line.rstrip().split()[3][:-1]))
			energies.pop(0) #remove first entry
		elif os.path.exists("SS_log.txt"):
			log_file = open("SS_log.txt")
			for line in log_file:
				energies.append(float(line.rstrip().split()[3][:-1]))
		GM_well_count = 0	
		len_sims_file = 0
		if os.path.exists("sim_to_GM.txt"):
			sim_file = open("sim_to_GM.txt")
			for line in sim_file:
				len_sims_file += 1
			c_step = 0
			to_skip = len_sims_file-len(energies)
			sim_file = open("sim_to_GM.txt")
			i = 0
			c.clear()
			for line in sim_file:
				c_step += 1
				if c_step <= to_skip: continue
				sims.append(float(line.rstrip()))
				steps.append(i**4)
				if float(line.rstrip()) > 80: GM_well_count += 1
				i += 1
			sim_file.close()
			print(GM_well_count)
		#print(len(energies))
		#print(len(sims))
		if n_plots == 4:
			axs[r, col].scatter(sims, energies, c=c, s=dot_size, cmap=cmap)
			axs[r, col].set_xlabel("Similarity (%)")
			axs[r, col].set_ylabel("Energy")
			axs[r, col].set_ylim([-174, -162])
			axs[r, col].set_xlim([0, 100])
		elif n_plots == 2:
			cbardata = axs[col].scatter(sims, energies, c=c, s=0.1, cmap=cmap)
			axs[col].set_xlabel("Similarity (%)")
			axs[0].set_ylabel(r"Energy ($\varepsilon$)")
			axs[col].set_ylim([ylow, yhigh])
			axs[col].set_xlim([0, 100])
			
		if mark_cluster:
			axs[r, col].scatter(marked_sim, marked_energy, c="#FF69B4", marker="*")
		show_final_path = True
		if paths:
			pathcs = ['red', 'cyan', 'lime', 'deeppink']
			pathcs = ['yellow', 'teal', 'gray', 'snow']
			for i in range(n_paths):
				simpath = []
				epath = []
				for j in range(reseed_indicies[-2-i], reseed_indicies[-1-i]-1):
					simpath.append(sims[j])
					epath.append(energies[j])	
				axs[col].plot(simpath, epath, c=pathcs[i], linewidth=1)
			simpath = []
			epath = []
			for i in range(reseed_indicies[-1], len(energies)):
				simpath.append(sims[i])
				epath.append(energies[i])
			axs[col].plot(simpath, epath, c='k', linewidth=1)
		os.chdir('..')
		sims.clear()
		energies.clear()
		#c.clear()
		sims = []
		col += 1
		if col == 2:
			col = 0
			r += 1
	from mpl_toolkits.axes_grid1 import make_axes_locatable
	divider = make_axes_locatable(plt.gca())
	cax = divider.append_axes("right", "5%", pad="3%")
	cbar = fig.colorbar(cbardata, cax=cax, ticks=[max(c),min(c)])
	axs[1].axes.yaxis.set_ticklabels([])
	cbar.ax.set_yticklabels(['GM Found', 'Search start'])
	plt.tight_layout()
	if display:
		plt.show()
	else:
		plt.savefig(name, dpi=250, bbox_inches='tight')
if __name__ == "__main__":
	main(sys.argv[1:])
