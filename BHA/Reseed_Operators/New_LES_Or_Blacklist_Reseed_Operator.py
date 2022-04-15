from BHA.Reseed_Operators.Reseed_Operator import Reseed_Operator
from BHA.Search_Strategies.Population.Population import Population

class New_LES_Or_Blacklist_Reseed_Operator(Reseed_Operator):

	def __init__(self, reseed_operator_information, steps_since_improvement = None, E_to_beat = None):
		super().__init__(reseed_operator_information, steps_since_improvement)

		self.rounding = self.reseed_operator_information['rounding']
		self.steps_to_reseed = self.reseed_operator_information['steps_to_reseed']
		self.r_Cut = self.reseed_operator_information['r_Cut']
		self.sim_cut = self.reseed_operator_information['sim_cut']

		self.reseed_operator_information['population_information']['client'] = "reseed_operator"
		self.reseed_operator_information['population_information']['r_Cut'] = self.r_Cut
		self.reseed_operator_information['population_information']['population_controller_information']['reseed_operator_pointer'] = self
		print("initialise blacklist")
		self.blacklist = Population(self.reseed_operator_information['population_information'])
		self.steps_since_improvement_arr = []


	
	def time_to_reseed(self, cluster):

		if not cluster.has_CNA_profile():
			cluster.calculate_CNA_profile(True, self.r_Cut)


		#print sim info
		try:
			sim = self.blacklist.similarity_of_cluster(cluster.CNA_profile)/100
			print("blacklist similarity = " + str(sim*100) + " %.")
		except TypeError:
			sim = None
			print("blacklist similarity = None")

		self.blacklist.update(cluster)

		if sim is not None and sim >= self.sim_cut: #cluster too close to blacklist, reseed triggered
			self.search_strategy_pointer.handle_reseed_triggering()
			self.blacklist.controller.notify_reseed_has_occured()
			self.steps_since_improvement = 0
			return True
		elif round(cluster.BH_energy, self.rounding) < round(self.E_to_beat, self.rounding): #steps until reseed reset by new LES
			self.E_to_beat = cluster.BH_energy
			self.steps_since_improvement_arr.append(self.steps_since_improvement)
			self.steps_since_improvement = 0
			return False
		elif self.steps_since_improvement >= self.steps_to_reseed: #reseed triggered by stagnation
			self.steps_since_improvement_arr.append(self.steps_since_improvement)
			self.steps_since_improvement = 0
			self.blacklist.controller.notify_reseed_has_occured()
			self.search_strategy_pointer.handle_reseed_triggering()
			return True
		else: #increment steps since improivement. one step closer to reseed being triggered.
			self.steps_since_improvement += 1
			return False
	
	def check_reseed_operator_information(self):
		missing_keys = None
		for key in ['steps_to_reseed', 'rounding', 'r_Cut', 'sim_cut']:
			if not key in self.reseed_operator_information:
				if missing_keys != None:
					missing_keys += ', '
					missing_keys += key
				else:
					missing_keys = key 
		if missing_keys != None:
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'The following parameter(s) are missing from the \n'
			error_msg += 'reseed_operator_information variable.\n'
			error_msg += missing_keys + '.\n'
			error_msg += 'These parameter(s) are required for the Energy Plus SCM\n'
			error_msg += 'Search Strategy.\n\n'
			error_msg += 'The basin hopping algorithm with exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()

		for key in ['steps_to_reseed', 'rounding']:
			if not isinstance(self.reseed_operator_information[key], int):
				error_msg = '\n'
				error_msg += '--------------------------------------------------------\n'
				error_msg += 'the steps_to_reseed and rounding parameters must be int \n'
				error_msg += 'data types (i.e. whole numbers).\n'
				error_msg += 'Please check these parameters and try running the\n'
				error_msg += 'algorithm again.\n\n'
				error_msg += 'The basin hopping algorithm with exit without starting.\n'
				error_msg += '--------------------------------------------------------\n'
				print(error_msg)
				from BHA.Lock import lock_remove
				lock_remove()
				exit()

		for key in ['r_Cut', 'sim_cut']:
			if not isinstance(self.reseed_operator_information[key], int) and not isinstance(self.reseed_operator_information[key], float):
				error_msg = '\n'
				error_msg += '--------------------------------------------------------\n'
				error_msg += 'the r_Cut and sim_Cut parameters must be numerical \n'
				error_msg += 'data types (i.e. int or float).\n'
				error_msg += 'Please check these parameters and try running the\n'
				error_msg += 'algorithm again.\n\n'
				error_msg += 'The basin hopping algorithm with exit without starting.\n'
				error_msg += '--------------------------------------------------------\n'
				print(error_msg)
				from BHA.Lock import lock_remove
				lock_remove()
				exit()

		if self.reseed_operator_information['sim_cut'] < 0 or self.reseed_operator_information['sim_cut'] > 1:
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'the sim_cut parameter value must be between 0 and 1.\n'
			error_msg += 'Please check these parameters and try running the\n'
			error_msg += 'algorithm again.\n\n'
			error_msg += 'The basin hopping algorithm with exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()

	def print_reseed_operator_information(self):
		"""
		Prints information about the reseed operator.
		"""
		to_print = ''
		to_print += '\nreseed Operator Name: ' + self.reseed_operator_information['reseed_operator']
		to_print += '\nSteps to reseed: ' + str(self.reseed_operator_information['steps_to_reseed'])
		to_print += '\nRounding Criterion (dp): ' + str(self.reseed_operator_information['rounding'])
		to_print += '\nr_Cut: ' + str(self.reseed_operator_information['r_Cut'])
		to_print += '\nsim_cut: ' + str(self.reseed_operator_information['sim_cut'])
		print(to_print)

