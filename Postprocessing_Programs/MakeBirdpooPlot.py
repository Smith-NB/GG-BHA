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
	help_string += '\t\tNo default. Format: ylow,yhigh (no spaces, no minus signs).\n'
	help_string += '\t\tlong option: --ylim\n'
	help_string += '\t-a:\talpha value (transparency).\n'
	help_string += '\t\tDefault = 1. Value must be between 0 and 1.\n'
	help_string += '\t\tlong option: --alpha\n'
	help_string += '\t-r:\tsimilairty reference filename.\n'
	help_string += '\t\tDefault = \'sim_to_GM.txt\'.\n'
	help_string += '\t\tlong option: --ref\n'
	help_string += '\t-e:\tEnd point\n'
	help_string += '\t\tSpecified how many data points to plot before stopping.\n'
	help_string += 'Default = None.\n'
	help_string += '\t\tlong option: --end\n'
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
	alpha = 1
	ref = "sim_to_GM.txt"
	refi = 0
	end = None
	try:
		opts, args = getopt.getopt(argv,"hdpf:y:t:c:a:r:e:",["help", "display", "progress", "filename=", "ylim=", "trial_nums=", "cmap=", "alpha=", "ref=", "end="])
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

		elif opt in ("-a", "--alpha"):
			try:
				alpha = float(arg)
			except ValueError:
				print("Please input a float for alpha")
				sys.exit(2)
			if alpha > 1 or alpha < 0:
				print("Value must be between 0 and 1. Exitting")
				sys.exit(2)

		elif opt in ("-r", "--ref"):
			ref = arg.strip().split(',')
			if len(ref) == 2:
				refi = int(ref[1])
				ref = ref[0]
			else:
				ref = ref[0]
				refi = 0
			ref_label = ref.replace(".txt", "")

		elif opt in ("-e", "--end"):
			try: 
				end = int(arg)
			except ValueError:
				print("Please input integer value. Exitting")
				sys.exit(2)

	data = {'energy': [], 'sim_to_GM': [], 'trial': [], 'hop_num': [], 'accepted_hop_num': []}
	for t in trial_nums:

		if show_progress:
			sys.stdout.write("\rParsing Trial%d                                " % t)
			sys.stdout.flush()
		
		f = open("Trial%d/%s" % (t, ref))
		for line in f:
			if refi == 0:
				data['sim_to_GM'].append(float(line.strip()))
			else:
				data['sim_to_GM'].append(float(line.strip().split()[refi]))
			data['trial'].append(t)
		f.close()			

		if os.path.exists("Trial%d/log.txt" % t):
			f = open("Trial%d/log.txt" % t)
			accepted_hop_num = 0
			#f.readline() #skip first line/entry/cluster
			for line in f:
				if "RESEED" in line:
					continue
				elif "accepted True" in line:
					data['energy'].append(float(line.split()[3][:-1]))
					data['hop_num'].append(int(line.split()[1][:-1]))
					data['accepted_hop_num'].append(accepted_hop_num)
					accepted_hop_num += 1
			#remove final line for completed trials
			if data['hop_num'][-1] == data['hop_num'][-2]: 
				for key in ['energy', 'hop_num', 'accepted_hop_num']: 
					data[key].pop()
			f.close()
	for key in data:
		data[key] = data[key][:end]
	df = pd.DataFrame(data=data)

	if len(trial_nums) == 1:
		plt.scatter(data=df[:end], x='sim_to_GM', y='energy', s=1)
		plt.xlim((0, 100))
		plt.ylim(ylim)
	else:
		grid = sns.FacetGrid(df, col="trial", col_wrap=2, ylim=ylim, alpha=alpha)
		
		if cmap_col is None:
			grid.map(plt.scatter, "sim_to_GM", "energy", s=1, alpha=alpha)
		else:
			grid.map(custom_scatter, "sim_to_GM", "energy", cmap_col, s=1, cmap=cmap, alpha=alpha)

		grid.set_titles(col_template="")

	if display:
		plt.show()
	else:
		plt.savefig(filename, dpi=250)
	print()

if __name__ == "__main__":
	main(sys.argv[1:])


