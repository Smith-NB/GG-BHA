import numpy as np
from BHA.Search_Strategies.Search_Strategy import Search_Strategy
from BHA.T_SCM_Methods import get_CNA_similarity
from ase import Atoms
from ase.visualize import view
from BHA.Search_Strategies.Sim_Functions import get_sim_function

class Energy_Plus_SCM_Search_Strategy(Search_Strategy):
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
		self.function = get_sim_function(self.search_strategy_information['function'])

		self.r_Cut = self.search_strategy_information['r_Cut']
		self.c_SCM = self.search_strategy_information['c_SCM']
		self.c_E = self.search_strategy_information['c_E']
		self.alpha = self.search_strategy_information['alpha']
		self.use_relaxed = self.search_strategy_information['use_relaxed']
		self.kT = self.search_strategy_information['temperature']
		self.E_min = float('inf')
		self.energy_piecewise = self.search_strategy_information['energy_piecewise']
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

		self.sim = get_CNA_similarity(cluster_old.CNA_profile, cluster_new.CNA_profile)/100
		print("similarity = " + str(self.sim*100) + " %.")
	
		if self.energy_piecewise == True and cluster_new.BH_energy < cluster_old.BH_energy:
			return True
		
		if self.energy_piecewise == False and cluster_new.BH_energy < self.E_min:
			self.E_min = cluster_new.BH_energy
			print("New E_min found. Autoaccepting")
			return True

		E_cont = np.exp((cluster_old.BH_energy - cluster_new.BH_energy) / self.kT) * self.c_E
		SCM_cont = self.function(self.alpha, self.sim) * self.c_SCM
		print("E_cont = " + str(E_cont))
		print("SCM_cont = " + str(SCM_cont))
		print("Chance to accept = " + str(E_cont + SCM_cont))
		accept = E_cont + SCM_cont > np.random.uniform()

		return accept			

	def handle_reseed_triggering(self):
		super().handle_reseed_triggering()

	def check_search_strategy_information(self):	
		"""
		Checks the search_strategy_information dictionary contains the requried keys.
		"""
		missing_keys = None
		for key in ['temperature', 'c_SCM', 'c_E', 'alpha', 'use_relaxed', 'r_Cut', 'energy_piecewise']:
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
			error_msg += 'These parameter(s) are required for the Energy Plus SCM\n'
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
		if self.search_strategy_information['c_SCM'] + self.search_strategy_information['c_E'] != 1.0:
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'The contrubutions of Energy and Structure (SCM) must\n'
			error_msg += 'sum to unity (i.e. c_E + c_SCM == 1)\n'
			error_msg += 'Please adjust these contrubutions and try again.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()
		if self.search_strategy_information['function'] not in ['exponential', 'neg_exponential', 'neg_tangent', 'linear']:
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'The function parameter must be one of the following: \n'
			error_msg += 'exponential, neg_exponential, neg_tangent, linear'
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
		to_print += '\nfunction: ' + str(self.search_strategy_information['function'])
		to_print += '\nAlpha: ' + str(self.search_strategy_information['alpha'])
		s = 'Yes.' if self.search_strategy_information['use_relaxed'] else 'No.'
		to_print += '\nUse Relaxed Structure: ' + s
		to_print += '\nr_Cut: ' + str(self.search_strategy_information['r_Cut'])
		print(to_print)
