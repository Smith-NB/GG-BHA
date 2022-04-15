import numpy as np
from BHA.Search_Strategies.Search_Strategy import Search_Strategy
from BHA.Search_Strategies.Population.Population import Population

class Energy_And_Forbidden_Hops_Search_Strategy(Search_Strategy):

	def __init__(self, search_strategy_information):
		super().__init__(search_strategy_information)

		self.kT = self.search_strategy_information['temperature']
		self.sim_cut = self.search_strategy_information['sim_cut']
		self.use_relaxed = self.search_strategy_information['use_relaxed']
		self.r_Cut = self.search_strategy_information['r_Cut']
		self.reseed_operator_pointer = self.search_strategy_information['reseed_operator_pointer']

		self.search_strategy_information['population_information']['r_Cut'] = self.r_Cut
		self.search_strategy_information['population_information']['population_controller_information']['reseed_operator_pointer'] = self.reseed_operator_pointer
		self.population = Population(self.search_strategy_information['population_information'])
		self.sim = None

	def get_acceptance_boolean(self, cluster_old, cluster_new):

		#Calculate CNA profiles if they do not already exist
		if not cluster_old.has_CNA_profile():
			cluster_old.calculate_CNA_profile(self.use_relaxed, self.r_Cut)
		if not cluster_new.has_CNA_profile():
			cluster_new.calculate_CNA_profile(self.use_relaxed, self.r_Cut)

		self.population.update(cluster_old)

		#print sim info
		try:
			self.sim = self.population.similarity_of_cluster(cluster_new.CNA_profile)/100
			print("similarity = " + str(self.sim*100) + " %.")
		except TypeError:
			self.sim = None
			print("similarity = None")


		if self.sim is not None and self.sim >= self.sim_cut: #Reject hop if it is too similar to blacklist (forbidden hop)
			print("Chance to accept = FORBIDDEN")
			return False
		elif cluster_new.BH_energy < cluster_old.BH_energy: #accept hop if it is not forbidden and is lower in energy
			return True
		else:	#calculate chance to accept hop based on Boltzmann distribution
			probability = np.exp((cluster_old.BH_energy - cluster_new.BH_energy) / self.kT)
			print("Chance to accept = " + str(probability))
			accept = probability > np.random.uniform()
			return accept

	def handle_reseed_triggering(self):
		print("EAFHSS-RESEEDING")
		self.population.controller.notify_reseed_has_occured()

	def check_search_strategy_information(self):
		missing_keys = None
		for key in ['temperature', 'sim_cut', 'population_information', 'use_relaxed', 'r_Cut']:
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
			error_msg += 'These parameter(s) are required for the Energy and\n'
			error_msg += 'Forbidden Hops Search Strategy.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()


		for key in ['temperature', 'sim_cut', 'r_Cut']:
			if not isinstance(self.search_strategy_information[key], float) and not isinstance(self.search_strategy_information[key], int):
				error_msg = '\n'
				error_msg += '--------------------------------------------------------\n'
				error_msg += 'the temperature, sim_cut and r_Cut parameters\n'
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

		if not isinstance(self.search_strategy_information['population_information'], dict):
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'the population_information parameter must be a dictionary\n'
			error_msg += 'data type.\n'
			error_msg += 'Please check this parameter and try running the\n'
			error_msg += 'algorithm again.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()

		if not isinstance(self.search_strategy_information['population_information']['population_controller_information'], dict):
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'the population_information parameter must have a key\n'
			error_msg += 'called "population_controller_information that is itself.\n'
			error_msg += 'an instance of a dictionary.\n'
			error_msg += 'Please check this parameter and try running the\n'
			error_msg += 'algorithm again.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()

		if self.search_strategy_information['population_information']['population_controller_information']['population_controller'] != "reseed":
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'the population for the Energy and Forbidden Hops Search\n'
			error_msg += 'Strategy must be controlled by the Reseed_Population_Controller,\n'
			error_msg += 'i.e. population_controller must be \'reseed\'.\n'
			error_msg += 'Please check this parameter and try running the\n'
			error_msg += 'algorithm again.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()

		if self.search_strategy_information['sim_cut'] < 0 or self.search_strategy_information['sim_cut'] > 1:
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'sim_cut must be greater than 0 and less than 1\n'
			error_msg += 'Please adjust this parameter and try running the\n'
			error_msg += 'algorithm again.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()

	def print_search_strategy_information(self):
		to_print = ''
		to_print += '\nSearch Strategy Name: ' + self.search_strategy_information['search_strategy']
		to_print += '\nTemperature: ' + str(self.search_strategy_information['temperature'])
		to_print += '\nsim_cut: ' + str(self.search_strategy_information['sim_cut'])
		to_print += '\nuse_relaxed: ' + str(self.search_strategy_information['use_relaxed'])
		to_print += '\nr_Cut: ' + str(self.search_strategy_information['r_Cut'])
		print(to_print)
