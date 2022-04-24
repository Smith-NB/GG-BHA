#!/usr/bin/env python3
import matplotlib.pyplot as plt
import os, sys, getopt
from Postprocessing_Programs.ClusterStructures import get_structure
cb_r = "#D81B60"
cb_b = "#1E88E5"
cb_g = "#004D40"
cb_y = "#FFC107"
cb_o = "#EC6327"
cb_p = "#573AE0"
black = "#000000"

def main(argv):	
	sims = []
	help_string = 'MakeProgressPlot.py [-o] [--options]\n'
	help_string += '\t-h:\tdisplay this message.\n'
	help_string += '\t-d:\tdisplay plot instead of saving\n'
	help_string += '\t\tlong option: --display\n'
	help_string += '\t-f:\tfile name of plot (no file extension).\n'
	help_string += '\t\tdefault name = "plot.png"\n'
	help_string += '\t\tlong option: --filename\n'
	help_string += '\t-e:\tPlot energy and Similarity\n'
	help_string += '\t\tlong option: --energy\n'
	help_string += '\t-n:\tNumber of trials to plot (requires -t)\n'
	help_string += '\t\tNo default. Required int.\n'
	help_string += '\t\tlong option: --n_plots\n'
	help_string += '\t\tI cant be fucked, this only works for -n = 4\n'
	help_string += '\t-t:\tTrials to plot (requires -n)\n'
	help_string += '\t\tNo default. Required -n ints. Format: 1,2,...,n (no spaces)\n'
	help_string += '\t\tlong option: --trials\n'
	help_string += '\t-a:\tArrangement of subplots. (requires -n)\n'
	help_string += '\t\tNo default. Format: cols,rows (no spaces)\n'
	help_string += '\t\tlong option: --arrangement\n'
	help_string += '\t-x:\textent graph to show length until next accepted hop\n'
	help_string += '\t\tlong option: --extend\n'
	help_string += '\t-r:\tShow reseeds. Requires use of -x\n'
	help_string += '\t\tlong option: --reseed\n'


	display = False
	name = "plot.png"
	energy = False
	accepted_energies = []
	n_plots = 0
	trials = []
	rows = 0
	cols = 0
	extend = False
	show_reseed = False
	try:
		opts, args = getopt.getopt(argv,"hdef:n:t:a:xr",["display", "filename=", "energy", "n_plots=", "trials=", "arrangement=", "extend", "reseed"])
	except getopt.GetoptError:
		print(help_string)
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print(help_string)
			sys.exit()

		elif opt in ("-d", "--display"):
			display = True

		elif opt in ("-f", "--energy"):
			name = arg
			if not name.endswith(".png"):
				name += ".png"

		elif opt in ("-n", "--n_plots"):
			n_plots = int(arg)

		elif opt in ("-t", "--trials"):
			for i in arg.split(','):
				trials.append(int(i))

		elif opt in ("-a", "--arrangement"):
			rc = arg.split(',')
			rows = int(rc[0])
			cols = int(rc[1])
		
		elif opt in ("-e", "--filename"):
			energy = True
		
		elif opt in ("-x", "--extend"):
			extend = True

		elif opt in ("-r", "--reseed"):
			show_reseed = True


	if show_reseed and not extend:
		print("You must use -x is you use -r. See -h for help")
		exit(2)
	trial_dirs = []
	if n_plots != len(trials):
		print("You must list -n ints after -t. See -h for help.")
		exit(2)
	elif n_plots == 0:
		trial_dirs.append(".")
	else:
		for trial in trials:
			trial_dirs.append("Trial%d/" % trial)
	if rows != 0 and cols != 0:
		fig, axs = plt.subplots(rows, cols, figsize=(10, 2*n_plots), sharey=True)
		#axs[0].set_ylabel("Similarity to GM (%)")
		#fig = plt.figure(figsize=(10, 2*n_plots))
		#gs = fig.add_gridspec(1, 2, wspace=0)
		#axs = gs.subplots(sharex=True, sharey=True)
	else:
		fig, ax = plt.subplots()
		axs = []
		axs.append(ax)

	d_count = 0
	r = 0 
	c = 0
	loop_count = 0
	ax2 = []
	for d in trial_dirs:
		os.chdir(d)
		if not os.path.exists("sim_to_GM.txt"):
			from ase.io.trajectory import Trajectory
			from BHA.T_SCM_Methods import get_CNA_profile, get_CNA_similarity
			import numpy as np
			traj = Trajectory("local_minima.traj")
			GM = get_structure("LJ38_GM")
			GM_CNA = get_CNA_profile((GM, [1.3549]))
			sims_temp = []
			x = []
			i = 0
			for cluster in traj:
				cna = get_CNA_profile((cluster, [1.3549]))
				sys.stdout.write("\r                                                                  ")
				sims_temp.append(get_CNA_similarity(cna, GM_CNA))
				sys.stdout.flush()
				sys.stdout.write("\r" + str(i))
				sys.stdout.flush()
				i += 1

			np.savetxt("sim_to_GM.txt", sims_temp, fmt="%f")

		stag_len = 0
		stag_lens = []
		reseed = []
		step = -1
		if os.path.exists("log.txt"):
			log_file = open("log.txt", "r")
			for line in log_file:
				if "step" in line:
					s_check = int(line.strip().split()[1][:-1])
					if s_check == step:
						continue
					else:
						step = s_check

				if "True" in line:
					accepted_energies.append(float(line.rstrip().split()[3][:-1]))
					stag_lens.append(stag_len)
					stag_len = 0
				elif "False" in line:
					stag_len += 1
				elif show_reseed and "RESEED" in line:
					reseed.append(step)

		sims_f = open("sim_to_GM.txt", "r")
		sim_count = 0
		GM_count = 0
		for line in sims_f:
			if extend:
				for i in range(stag_lens[sim_count]):
					try:
						sims.append(sims[-1])
						if sims[-1] >= 90: GM_count += 1
					except IndexError:
						sims.append(0)
			sims.append(float(line.rstrip()))
			if sims[-1] >= 90: GM_count += 1
			sim_count += 1
		print(GM_count)
		if energy:
			
			axs[r, c].set_xlabel('Step no.')
			axs[r, c].set_ylabel(r'Energy of cluster ($\epsilon$)')
			plt.ylim([-174, -160])
			handles = []
			labels = []

			l1, = axs[r, c].plot(accepted_energies, color='g', label="Energy of accepted cluster")
			handles.append(l1)
			labels.append("Energy of accepted cluster")

			ax2.append(axs[r, c].twinx())
			ax2[loop_count].set_ylabel(r'Similarity (%)') 
			l3, = ax2[loop_count].plot(sims, label='Similarity to GM')
			handles.append(l3)
			labels.append("Similarity to GM")

			ax2[loop_count].legend(loc='lower left')
			box = ax2[loop_count].get_position()
			ax2[loop_count].set_position([box.x0, box.y0 + box.height * 0.1,
						box.width, box.height * 0.9])
			ax2[loop_count].legend(handles, labels, loc='upper center', bbox_to_anchor=(0.5, 1.15),
						fancybox=True, shadow=True, ncol=4)
		else:
			#axs[r, c].set_title(d)
			if n_plots == 4:
				axs[r, c].plot(sims)
				if show_reseed:
					reseed_yvals = []
					for re in reseed:
						reseed_yvals.append(sims[re])
					axs[r,c].scatter(reseed, reseed_yvals, s=10, c='r')
				axs[r, c].set_ylim([0,100])
				if extend:
					axs[r, c].set_xlabel("Attempted Hop Number")
				else:	
					axs[r, c].set_xlabel("Accepted Hop Number")
				axs[r, c].set_ylabel("Similarity to GM (%)")
			elif n_plots == 2:
				axs[c].plot(sims,zorder=1, c=cb_b)
				if show_reseed:
					reseed_yvals = []
					for re in reseed:
						reseed_yvals.append(sims[re])
					axs[c].scatter(reseed, reseed_yvals, s=10, c=cb_r,zorder=2)
				axs[c].set_ylim([0,100])
				if extend:
					axs[c].set_xlabel("Attempted Hop Number")
				else:	
					axs[c].set_xlabel("Accepted Hop Number")
				#axs[c].set_ylabel("Similarity to GM (%)")
				axs[c].set_xlim([0,2500])
		os.chdir('..')
		sims.clear()
		sims = []
		loop_count += 1
		c += 1
		if c == 2:
			c = 0
			r += 1

	fig.tight_layout()
	if display:
		plt.show()
	else:
		plt.savefig(name, dpi=250)

if __name__ == "__main__":
   main(sys.argv[1:])
