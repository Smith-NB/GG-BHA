import numpy as np
from BHA.Search_Strategies.Search_Strategy import Search_Strategy
from BHA.T_SCM_Methods import get_CNA_similarity
from ase import Atoms
from ase.visualize import view
from BHA.Search_Strategies.Sim_Functions import get_sim_function
from BHA.Search_Strategies.Prob_Functions import get_prob_function
from BHA.Search_Strategies.Population.Population import Population

class Energy_Plus_Population_SCM_Search_Strategy(Search_Strategy):
	"""
	This class describes the Energy + SCM Search Strategy.
	This search strategy determines if a new step / cluster will be accepted based on both its energy
	and its structure.

	:param search_strategy_information: parameters to be used by this search strategy.
	:type  dict (with the following keys: ['temperature', 'c_SCM', 'c_E', 'alpha', 'r_Cut'])
	"""
	def __init__(self, search_strategy_information):
		super().__init__(search_strategy_information)
		self.sim = None
		
		self.sim_function = get_sim_function(self.search_strategy_information['sim_function'])
		self.prob_function = get_prob_function(self.search_strategy_information['prob_function'])
		
		self.reseed_operator_pointer = self.search_strategy_information['reseed_operator_pointer']
		self.search_strategy_information['population_information']['population_controller_information']['reseed_operator_pointer'] = self.reseed_operator_pointer

		self.search_strategy_information['population_information']['client'] = "search_strategy"
		self.search_strategy_information['population_information']['r_Cut'] = self.search_strategy_information['r_Cut']
		self.population = Population(search_strategy_information['population_information'])

		self.r_Cut = self.search_strategy_information['r_Cut']
		self.c_SCM = self.search_strategy_information['c_SCM']
		self.c_E = self.search_strategy_information['c_E']
		self.energy_piecewise = self.search_strategy_information['energy_piecewise']
		self.alpha = self.search_strategy_information['alpha']
		self.use_relaxed = self.search_strategy_information['use_relaxed']
		self.kT = self.search_strategy_information['temperature']
		self.E_min = float('inf')
		
	def get_acceptance_boolean(self, cluster_old, cluster_new):
		"""
		Determines if a step is accepted or rejected.

		:param cluster_old: The most recent accepted cluster to be compared against.
		:type  cluster_old: BHA.Cluster
		:param cluster_new: The new cluster to be accepted or rejected.
		:type  cluster_new: BHA.Cluster
		"""

		#If the new cluster has a lower energy, return True

		if not cluster_old.has_CNA_profile():
			cluster_old.calculate_CNA_profile(self.use_relaxed, self.r_Cut)

		if not cluster_new.has_CNA_profile():
			cluster_new.calculate_CNA_profile(self.use_relaxed, self.r_Cut)

		try:
			self.sim = self.population.similarity_of_cluster(cluster_new.CNA_profile)/100
			print("similarity = " + str(self.sim*100) + " %.")
		except TypeError:
			self.sim = None
			print("similarity = None")

		self.population.update(cluster_old)

		# Performed after sim calculated for completion of data. #
		if self.energy_piecewise == True and cluster_new.BH_energy < cluster_old.BH_energy:
			return True
		
		if self.energy_piecewise == False and cluster_new.BH_energy < self.E_min:
			self.E_min = cluster_new.BH_energy
			print("New E_min found. Autoaccepting")
			return True

		E_val = np.exp((cluster_old.BH_energy - cluster_new.BH_energy) / self.kT)
		if E_val > 1:
			E_val = 1
		#covers for if the population is empty
		if self.sim is None:
			probability = E_val
		else:
			SCM_val = self.sim_function(self.alpha, self.sim)
			probability = self.prob_function(self.c_E, E_val, self.c_SCM, SCM_val)
		
		accept = probability > np.random.uniform()

		return accept			

	def handle_reseed_triggering(self):
		super().handle_reseed_triggering()

	def check_search_strategy_information(self):	
		"""
		Checks the search_strategy_information dictionary contains the requried keys.
		"""
		missing_keys = None
		for key in ['temperature', 'c_SCM', 'c_E', 'energy_piecewise', 'alpha', 'use_relaxed', 'r_Cut', 'sim_function', 'prob_function', 'population_information']:
			if not key in self.search_strategy_information:
				if missing_keys != None:
					missing_keys += ', '
					missing_keys += key
				else:
					missing_keys = key 
		if missing_keys != None:
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'The following parameter(s) are missing from the \n'
			error_msg += 'search_strategy_information variable.\n'
			error_msg += missing_keys + '.\n'
			error_msg += 'These parameter(s) are required for the Energy Plus Population\n'
			error_msg += 'Search Strategy.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()

		for key in ['temperature', 'c_SCM', 'c_E', 'alpha', 'r_Cut']:
			if not isinstance(self.search_strategy_information[key], float) and not isinstance(self.search_strategy_information[key], int):
				error_msg = '\n'
				error_msg += '--------------------------------------------------------\n'
				error_msg += 'the temperature, c_SCM, c_E, alpha and r_Cut parameters\n'
				error_msg += 'must be float or int data types (i.e. numerical).\n'
				error_msg += 'Please check these parameters and try running the\n'
				error_msg += 'algorithm again.\n\n'
				error_msg += 'The basin hopping algorithm will exit without starting.\n'
				error_msg += '--------------------------------------------------------\n'
				print(error_msg)
				from BHA.Lock import lock_remove
				lock_remove()
				exit()

		if not isinstance(self.search_strategy_information['use_relaxed'], bool):
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'the use_realxed parameter must be a boolean data type \n'
			error_msg += '(i.e. True or False).\n'
			error_msg += 'Please check this parameter and try running the\n'
			error_msg += 'algorithm again.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()
		if not isinstance(self.search_strategy_information['energy_piecewise'], bool):
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'the energy_piecewise parameter must be a boolean data type \n'
			error_msg += '(i.e. True or False).\n'
			error_msg += 'Please check this parameter and try running the\n'
			error_msg += 'algorithm again.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()
		if self.search_strategy_information['c_SCM'] > 1 or self.search_strategy_information['c_SCM'] < 0:
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'c_SCM must be greater than 0 and less than 1\n'
			error_msg += 'Please adjust this parameter and try again.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()
		if self.search_strategy_information['c_E'] > 1 or self.search_strategy_information['c_E'] < 0:
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'c_E must be greater than 0 and less than 1\n'
			error_msg += 'Please adjust this parameter and try again.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()
		if self.search_strategy_information['c_SCM'] + self.search_strategy_information['c_E'] != 1.0 and self.search_strategy_information['prob_function'] == 'additive':
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'The contrubutions of Energy and Structure (SCM) must\n'
			error_msg += 'sum to unity (i.e. c_E + c_SCM == 1) for an additive prob_function\n'
			error_msg += 'Please adjust these contrubutions and try again.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()
		if self.search_strategy_information['c_E'] != 1 and self.search_strategy_information['prob_function'] == 'subtractive':
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'c_E must be 1 for a subtractive prob_function.\n'
			error_msg += 'Please adjust this parameter and try again.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()
		if self.search_strategy_information['sim_function'] not in ['exponential', 'neg_exponential', 'neg_tangent', 'linear', 'pass']:
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'The sim_function parameter must be one of the following: \n'
			error_msg += '\texponential, neg_exponential, neg_tangent, linear.'
			error_msg += 'Please correct this parameter and try again.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()

		if self.search_strategy_information['prob_function'] not in ['additive', 'subtractive']:
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'The function parameter must be one of the following: \n'
			error_msg += '\additive, subtractive.'
			error_msg += 'Please correct this parameter and try again.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()
	def print_search_strategy_information(self):
		"""
		Prints information about the search strategy.
		"""
		to_print = ''
		to_print += '\nSearch Strategy Name: ' + self.search_strategy_information['search_strategy']
		to_print += '\nTemperature: ' + str(self.search_strategy_information['temperature'])
		to_print += '\nc_SCM: ' + str(self.search_strategy_information['c_SCM'])
		to_print += '\nc_E: ' + str(self.search_strategy_information['c_E'])
		to_print += '\nSim Function: ' + str(self.search_strategy_information['sim_function'])
		to_print += '\nProb Function: ' + str(self.search_strategy_information['prob_function'])
		to_print += '\nAlpha: ' + str(self.search_strategy_information['alpha'])
		s = 'Yes.' if self.search_strategy_information['use_relaxed'] else 'No.'
		to_print += '\nUse Relaxed Structure: ' + s
		to_print += '\nr_Cut: ' + str(self.search_strategy_information['r_Cut'])
		print(to_print)