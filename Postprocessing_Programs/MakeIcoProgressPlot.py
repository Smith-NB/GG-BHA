#!/usr/bin/env python3
import matplotlib.pyplot as plt
import os, sys, getopt
import numpy as np
from ase import Atoms

def get_ico():
	return Atoms(symbols='Ne38', pbc=np.array([False, False, False]), 
			cell=np.array(
				[[23.8204175 ,  0.        ,  0.        ],
				[ 0.        , 23.8165006 ,  0.        ],
				[ 0.        ,  0.        , 24.02128846]]),
			positions=np.array(
				[[12.85948753, 10.69097678, 12.3799274 ],
				[13.17176121, 11.59623236, 11.80248214],
				[11.74885165, 10.58451662, 12.30493724],
				[12.09969487, 13.87875804, 11.23325141],
				[13.47263124, 12.4996623 , 11.21621597],
				[11.69986762, 11.83162308, 11.39275531],
				[11.57588959, 12.45372441, 12.29433616],
				[13.03514283, 13.41592337, 11.68120196],
				[12.34205285, 10.94844925, 11.43310607],
				[10.75066024, 12.79418795, 10.64293929],
				[ 9.75432931, 12.21107284, 12.06138069],
				[10.14002718, 11.35741173, 12.70359915],
				[12.2140628 , 10.99407666, 13.23946151],
				[10.6103671 , 12.35513591, 12.74305364],
				[12.55480531, 12.9619056 , 10.77534487],
				[10.06933171, 13.1402397 , 11.46366323],
				[11.63071351, 13.41107135, 10.33405754],
				[11.72759159, 12.30863908, 10.41004667],
				[10.85171597, 11.68583495, 10.71938681],
				[12.07532785, 13.39667868, 12.22584144],
				[10.74795486, 12.30485593, 11.62666914],
				[13.4251877 , 12.55236837, 12.33074913],
				[11.56242713, 11.88400414, 13.1990781 ],
				[12.4677958 , 12.52770893, 12.87943247],
				[12.64869442, 11.85290794, 10.85117754],
				[10.95882297, 13.77272804, 11.14948765],
				[11.08614066, 10.889218  , 13.1566698 ],
				[11.23145915, 10.84524539, 11.35162082],
				[13.11386271, 11.63380583, 12.92170593],
				[11.82507537, 11.20332272, 10.48221145],
				[10.92737845, 13.29005472, 12.14160354],
				[ 9.87917482, 12.16565145, 10.95257334],
				[12.20507024, 11.58384394, 12.32452175],
				[10.2525476 , 11.32494538, 11.58840233],
				[11.60428279, 12.91373344, 11.32426869],
				[12.50483534, 12.46813871, 11.7555777 ],
				[10.63856653, 10.48456153, 12.216977  ],
				[11.11925368, 11.48293143, 12.24486263]]))

def main(argv):	
	sims = []

	help_string = 'MakeProgressPlot.py [-o] [--options]\n'
	help_string += '\t-h:\tdisplay this message.'
	help_string += '\t-d:\tdisplay plot instead of saving\n'
	help_string += '\t\tlong option: --display\n'
	help_string += '\t-f:\tfile name of plot (no file extension).\n'
	help_string += '\t\tdefault name = "plot.png"\n'
	help_string += '\t\tlong option: --name\n'

	display = False
	name = "plot.png"
	try:
		opts, args = getopt.getopt(argv,"hdf:",["display", "filename="])
	except getopt.GetoptError:
		print(help_string)
		sys.exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print(help_string)
			sys.exit()

		elif opt in ("-d", "--display"):
			display = True

		elif opt in ("-f", "--filename"):
			name = arg
			if not name.endswith(".png"):
				name += ".png"

	if os.path.exists("sim_to_ico.txt"):
		sims_f = open("sim_to_ico.txt")
		for line in sims_f:
			sims.append(float(line.rstrip()))
	else:
		from ase.io.trajectory import Trajectory
		from BHA.T_SCM_Methods import get_CNA_profile, get_CNA_similarity
		import numpy as np
		from Postprocessing_Programs.ClusterStructures import get_structure
		traj = Trajectory("local_minima.traj")
		ico = get_structure("LJ75_ico")
		ico_CNA = get_CNA_profile((ico, [1.3549]))
		x = []
		i = 0
		for cluster in traj:
			"""sys.stdout.write("\r                                                                  ")
			sys.stdout.flush()
			sys.stdout.write("\r" + str(i))
			sys.stdout.flush()"""
			cna = get_CNA_profile((cluster, [1.3549]))
			sims.append(get_CNA_similarity(ico_CNA, cna))
			i += 1

		np.savetxt("sim_to_ico.txt", sims, fmt="%f")
	plt.plot(sims, color='r')
	plt.ylim([0,100])
	plt.xlabel("Accepted Hop Number")
	plt.ylabel("Similarity to Ico(%)")
	if display:
		plt.show()
	else:
		plt.savefig(name, dpi=250)

if __name__ == "__main__":
   main(sys.argv[1:])
