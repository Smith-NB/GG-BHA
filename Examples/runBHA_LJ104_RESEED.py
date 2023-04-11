from ase.optimize.fire import FIRE
from time import perf_counter
from BHA.BH_Program import BasinHopping

#Setup the BHA
cluster_makeup = {'Ne':104} 					#{'<Element Symbol>': <number of atoms>}
temperature = 0.8 								#kT, Determines likelihood of uphill moves being accepted: A = min[1, exp(ΔE/kT)]
search_strategy = 'energy' 	# 'energy' or 'energy_and_forbidden_hops' (the latter is the REHOP mode).
reseed_operator = 'new_LES_or_blacklist_alt' 					# 'none' or 'new_LES' or 'new_LES_or_blacklist_alt' (the latter is for the RESEED mode).


optimizer = FIRE  			#optimizer used for GA
fmax=0.01					#convergence criterion for ASE optimisers; the maximum force acting on any atom is less than fmax.
dr=0.4						#amount atoms can be moved by when perturbed for an attempted hop. 
boxtoplaceinlength = 5.3 	#cube dimension for randomly generating a structure (used for reseeding and starting seed strucure).
vacuumAdd = 10 			 	#amount of padding added to the above box for the cell, after structure generation
optimizer_logfile=None		#logfile for the ASE optimizer. None for no logging, otherwise specify filename.

exit_when_targets_found=True		#True or False. Specify if the search should terminate when clusters of target energies are located
target_energies=[-582.09,-582.04] 	#List of target energies (here the GM and Ih minimum of LJ104 are listed).
rounding=2							#Rounding for target energies
adjust_cm=True 						
r_Cut = 1.3549						#rCut value used by SCM for defining bond lengths/neighbours. Average between 1st and 2nd nearest neighbour distances used.
total_length_of_running_time = 71.5 #Specify maximum wall time of the search, in hours.


population_controller_information = {'population_controller': 'reseed'} #update the population when a reseed occurs (not including blacklist triggered reseeds).

#describes the blacklist, the 'size' defines the number of clusters that can be present in the blacklist.
population_information = {'population_controller_information': population_controller_information,
							'size': 5,	#size of the blacklist
							'similarity_mode': 'max'} #a cluster's similarity to the blacklist is the maximum similarity between it and each member of the blacklist.

#pass search strategy (Metropolis Criterion) information to the BHA. Below is an example of the Energy search strategy.
search_strategy_information = {'search_strategy': search_strategy, 'temperature': temperature}

#pass reseed operator information. The following specifies to reseed if the minimum energy obtained since the last reseed has
#not been improved upon in 100 steps, where energies are compared with a rounding of 2dp.
#Additionally, the RESEED blacklist mode is also used, where the 'sim_cut' entry specifies σ_BL.
reseed_operator_information = {'reseed_operator': reseed_operator, 
				'steps_to_reseed': 100, 
				'rounding': 2, 
				'r_Cut': r_Cut, 
				'sim_cut': 0.90, #clusters 90% similar to the blacklist are defined as within the taboo region
				'population_information': population_information} 

# information for the potential calculator. 'LJRR' specified the LJ potential with reduced units (RR).
# the second line is equivalent to the first but allows for the explicit specification of all relavent parameters.
calculator_information = {'potential': 'LJRR'}
#calculator_information = calculator_information = {'potential': 'LJ', 'params': {'elements': [10], 'epsilon': [1], 'sigma': [1], 'rCut': 1000, 'modified': True}}

population_information['calculator_information'] = calculator_information #this line is needed for if the search is restarted.

bh = BasinHopping(
				cluster_makeup = cluster_makeup,
				fmax = fmax,
				dr = dr,
				reseed_operator_information = reseed_operator_information,
				boxtoplaceinlength = boxtoplaceinlength,
				vacuumAdd = vacuumAdd,
				search_strategy_information = search_strategy_information,
				exit_when_targets_found = exit_when_targets_found,
				target_energies = target_energies,
				rounding = rounding,
				adjust_cm = adjust_cm,
				total_length_of_running_time = total_length_of_running_time,
				local_minima_trajectory='local_minima.traj',
				calculator_information=calculator_information,
				r_Cut = r_Cut,
				cnalog = "CNAlog.txt"
				)


steps = 1000 #how many steps to perform with the BHA.

#run for n steps and print time taken to perform n steps.
ts = perf_counter()
bh.run(steps)
te = perf_counter()
print(ts-te)
