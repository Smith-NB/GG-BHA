from ase.optimize.fire import FIRE
from time import perf_counter
from BHA.BH_Program import BasinHopping

#Setup the BHA
cluster_makeup = {'Ne':98} 	#{'<Element Symbol>': <number of atoms>}
temperature = 0.8 				#kT, Determines likelihood of uphill moves being accepted: A = min[1, exp(ΔE/kT)]
search_strategy = 'energy' 		# 'energy' or 'energy_and_forbidden_hops' (the latter is the REHOP mode).
reseed_operator = 'new_LES' 	# 'none' or 'new_LES' or 'new_LES_or_blacklist_alt' (the latter is for the RESEED mode).


optimizer = FIRE  			#optimizer used for GA
fmax=0.01					#convergence criterion for ASE optimisers; the maximum force acting on any atom is less than fmax.
dr=0.4						#amount atoms can be moved by when perturbed for an attempted hop. 
boxtoplaceinlength = 5.2 	#cube dimension for randomly generating a structure (used for reseeding and starting seed strucure).
vacuumAdd = 10 			 	#amount of padding added to the above box for the cell, after structure generation
optimizer_logfile=None		#logfile for the ASE optimizer. None for no logging, otherwise specify filename.

exit_when_targets_found=True		#True or False. Specify if the search should terminate when clusters of target energies are located
target_energies=[-543.67, -543.64] 	#List of target energies (here the GM and Ih minimum of LJ104 are listed).
rounding=2							#Rounding for target energies
adjust_cm=True 						
r_Cut = 1.3549						#rCut value used by SCM for defining bond lengths/neighbours. Average between 1st and 2nd nearest neighbour distances used.
total_length_of_running_time = 71.5 #Specify maximum wall time of the search, in hours.


#pass search strategy (Metropolis Criterion) information to the BHA. Below is an example of the Energy (default) search strategy.
search_strategy_information = {'search_strategy': search_strategy, 'temperature': temperature}

#pass reseed operator information. The following specifies to reseed if the minimum energy obtained since the last reseed has
#not been improved upon in 100 steps, where energies are compared with a rounding of 2dp.
reseed_operator_information = {'reseed_operator': reseed_operator, 
				'steps_to_reseed': 100, 
				'rounding': 2}

# information for the potential calculator. 'LJRR' specified the LJ potential with reduced units (RR).
# the second line is equivalent to the first but allows for the explicit specification of all relavent parameters.
calculator_information = {'potential': 'LJRR'}
#calculator_information = calculator_information = {'potential': 'LJ', 'params': {'elements': [10], 'epsilon': [1], 'sigma': [1], 'rCut': 1000, 'modified': True}}
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
				r_Cut = r_Cut,
				calculator_information = calculator_information
				)


steps = 1000 #how many steps to perform with the BHA.

#run for n steps and print time taken to perform n steps.
ts = perf_counter()
bh.run(steps)
te = perf_counter()
print(ts-te)
