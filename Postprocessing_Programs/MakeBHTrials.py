#!/usr/bin/python
import os, sys
from ase.optimize.fire import FIRE


imports = 'from ase.optimize.fire import FIRE'
imports += 'from ase.io import write'
imports += 'from time import perf_counter'
imports += 'from BHA.BH_Program import BasinHopping'

cluster_makeups = [{'Ne':38}]
temperature = 0.8
optimizer = FIRE
fmax = 0.01
dr = 0.4
boxtoplaceinlength = 4.1
vacuumAdd = 10
optimizer_logfile=None
exit_when_GM_found=True	
GM_energy=[-173.93] 	#-173.93 = E of LJ38 GM
rounding=2			#Default to 2dp
adjust_cm=True
total_length_of_running_time = 1
lenard_jones = True
steps = 100000


search_strategies = []
search_strategy_names = []
search_strategy_names.append('energy')
search_strategies.append({'search_strategy': 'energy', 'temperature':  0.8})
for i in range(1, 11):
	c_SCM = i/10;
	c_E = 1 - c_SCM
	search_strategies.append({'search_strategy': 'energy_plus_SCM', 
							'temperature': temperature, 
							'c_SCM': c_SCM, 'c_E': c_E, 
							'r_Cut': 1.3549, 'alpha': 1,
							'use_relaxed': True})
	search_strategy_names.append('energy_plus_SCM_c_SCM_' + str(c_SCM))


reseed_operators = []
reseed_operators += {'reseed_operator': reseed_operator, 'steps_to_reseed': 40, 'rounding': 2} 


for cluster in cluster_makeups:
	for ss in search_strategies:
		search_strategies = []
