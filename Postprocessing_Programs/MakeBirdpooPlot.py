#!/usr/bin/env python3

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os, sys, getopt
#from Postprocessing_Programs.MakeSimToGM import MakeSimToGM

def print_help():
	help_string = 'MakePlot.py [-o] [--options]\n'
	help_string += '\t-h:\tprint this message\n'
	help_string += '\t-d:\tdisplay the plot instead of saving it\n'
	help_string += '\t\tlong option: --display\n'
	help_string += '\t-p:\tOutput progress of script to the terminal.\n'
	help_string += '\t\tlong option: --progress\n'
	help_string += '\t-f:\tfile name of plot (no file extension).\n'
	help_string += '\t\tdefault name = "plot.png"\n'
	help_string += '\t\tlong option: --filename\n'
	help_string += '\t-c:\tColourmap to use.\n'
	help_string += '\t\tdefault colour map = None\n'
	help_string += '\t\tlong option: --cmap\n'
	help_string += '\t-t:\tTrials to plot\n'
	help_string += '\t\tNo default. Format: 1,2,...,n (no spaces).\n'
	help_string += '\t\tlong option: --trial_nums\n'
	help_string += '\t-y:\ty-axis limits.\n'
	help_string += '\t\tNo default. Format: ylow,yhigh (no spaces).\n'
	help_string += '\t\tlong option: --ylim\n'
	print(help_string)
	return




def custom_scatter(x, y, c, **kwargs):
  del kwargs["color"]
  plt.scatter(x, y, c = c, **kwargs)

def main(argv):
	display = False
	cmap = None
	ylim = []
	trial_nums = []
	filename = "plot.png"
	cmap = None
	cmap_col = None
	show_progress = False
	try:
		opts, args = getopt.getopt(argv,"hdpf:y:t:c:",["help", "display", "progress", "filename=", "ylim=", "trial_nums=", "cmap="])
	except getopt.GetoptError:
		print_help()
		sys.exit(2)

	for opt, arg in opts:

		if opt in ("-h, --help"):
			print_help()
			sys.exit()

		elif opt in ("-d", "--display"):
			display = True

		elif opt in ("-f", "--filename"):
			filename = arg
			if not filename.endswith(".png"):
				filename += ".png"

		elif opt in ("-p", "--progress"):
			show_progress = True

		elif opt in ("-y, --ylim"):
			for y in arg.split(','):
				ylim.append(-int(y))


		elif opt in ("-t", "--trials"):
			for t in arg.split(','):
				trial_nums.append(int(t))

		elif opt in ("-c", "--cmap"):
			cmap = arg
			cmap_col = "hop_num"

	data = {'energy': [], 'sim_to_GM': [], 'trial': [], 'hop_num': [], 'accepted_hop_num': []}
	for t in trial_nums:

		

		if not os.path.exists("Trial%d/sim_to_GM.txt" % t):
			pass#MakeSimToGM("Trial%d" % t)

		if show_progress:
			sys.stdout.write("\rParsing Trial%d                                " % t)
			sys.stdout.flush()
		
		f = open("Trial%d/sim_to_GM.txt" % t)
		for line in f:
			data['sim_to_GM'].append(float(line.strip()))
			data['trial'].append(t)
		f.close()			

		if os.path.exists("Trial%d/log.txt" % t):
			f = open("Trial%d/log.txt" % t)
			accepted_hop_num = 0
			f.readline() #skip first line/entry/cluster
			for line in f:
				if "RESEED" in line:
					continue
				elif "accepted True" in line:
					data['energy'].append(float(line.split()[3][:-1]))
					data['hop_num'].append(int(line.split()[1][:-1]))
					data['accepted_hop_num'].append(accepted_hop_num)
					accepted_hop_num += 1
			#remove final line
			if data['hop_num'][-1] == data['hop_num'][-2]: 
				for key in ['energy', 'hop_num', 'accepted_hop_num']: 
					data[key].pop()
			f.close()
	df = pd.DataFrame(data=data)

	if len(trial_nums) == 1:
		plt.scatter(data=df, x='sim_to_GM', y='energy', s=1, alpha=0.1)
		plt.xlim((0, 100))
	else:
		grid = sns.FacetGrid(df, col="trial", col_wrap=2, ylim=ylim)
		
		if cmap_col is None:
			grid.map(plt.scatter, "sim_to_GM", "energy", s=1)
		else:
			grid.map(custom_scatter, "sim_to_GM", "energy", cmap_col, s=1, cmap=cmap)

		grid.set_titles(col_template="")

	if display:
		plt.show()
	else:
		plt.savefig(filename, dpi=250)
	print()

if __name__ == "__main__":
	main(sys.argv[1:])


