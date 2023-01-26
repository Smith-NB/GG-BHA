#!/usr/bin/env python3

import os, sys
import getopt
from Postprocessing_Programs.ClusterStructures import get_structure
from BHA.T_SCM_Methods import get_CNA_profile, get_CNA_similarity
from ase.io import read
from collections import Counter
argv = sys.argv[1:]
try:
	 opts, args = getopt.getopt(argv, "hr:t:c:f:")
except:
	print("Error")
	sys.exit(2)

ref = None
trials = None
rCut = None
out_fname = None
for opt, arg in opts:
	if opt == "-h":
		msg = "The following command line arguments are available\n"
		msg += "-h:\tprint this message."
		msg += "-r:\tspecify reference structure from ClusterStructures\n\tor as xyz file in local dir.\n"
		msg += "-t:\tspecify trials to run script in as numbers, comma delimited, OR range, colon delimited."
		msg += "-c:\tspecify rCut."
		msg += "-f:\tspecify filename.\n"
		print(msg)
		sys.exit()
	elif opt == "-r":
		if arg.endswith(".xyz"):	
			ref = read(arg)
		else:
			ref = get_structure(arg)
	elif opt == "-t":
		if "," in arg:
			trials = [int(t) for t in  arg.split(',')]
		elif ":" in arg:
			trange = [int(t) for t in arg.split(':')]
			trials = []
			for i in range(trange[0], trange[1]):
				trials.append(i)
	elif opt == "-c":
		rCut = float(arg)
	elif opt == "-f":
		out_fname = arg

if None in [ref, rCut, trials, out_fname]:
	print("All arguments are required. Use -h for help")

ref.CNA = get_CNA_profile((ref, [rCut]))
for t in trials:	
	if os.path.exists("Trial%d/%s" % (t, out_fname)): continue
	cnalog = open("Trial%d/CNAlog.txt" % t)
	simFile = open("Trial%d/%s" % (t, out_fname), "w")
	i = 0	
	for line in cnalog:
		i += 1
		cna = Counter()
		sig_abun_pairs = line.strip().split(';')[:-1]
		for pair in sig_abun_pairs:
			abundance = int(pair.split(':')[1])
			sigs = pair.split(':')[0]
			sigs = tuple([int(s) for s in sigs.split(',')])
			cna[sigs] = abundance
		simFile.write("%f\n" % get_CNA_similarity(ref.CNA, [cna]))
	cnalog.close()
	simFile.close()
