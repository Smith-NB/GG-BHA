from BHA.Reseed_Operators.Reseed_Operator import Reseed_Operator
from BHA.Search_Strategies.Population.Population import Population

class New_LES_Or_Blacklist_Reseed_Operator(Reseed_Operator):

	def __init__(self, reseed_operator_information, steps_since_improvement = None, E_to_beat = None):
		super().__init__(reseed_operator_information, steps_since_improvement)

		self.rounding = self.reseed_operator_information['rounding']
		self.steps_to_reseed = self.reseed_operator_information['steps_to_reseed']

		self.reseed_operator_information['population_information']['population_controller_information']['reseed_operator_pointer'] = self
		self.blacklist = Population(self.reseed_operator_information['population_information'])
		self.steps_since_improvement_arr = []


	
	def time_to_reseed(self, cluster):
		if round(cluster.BH_energy, self.rounding) < round(self.E_to_beat, self.rounding): #time to reseed reset by new LES
			self.E_to_beat = cluster.BH_energy
			self.steps_since_improvement_arr.append(self.steps_since_improvement)
			self.steps_since_improvement = 0
			return False
		elif self.steps_since_improvement >= self.steps_to_reseed: #reseed triggered
			self.steps_since_improvement_arr.append(self.steps_since_improvement)
			self.steps_since_improvement = 0
			print("RESEEDING-NEWLESRO")
			self.search_strategy_pointer.handle_reseed_triggering()
			return True
		else: #increment steps since improivement. one step closer to reseed being triggered.
			self.steps_since_improvement += 1
			return False
	
	def check_reseed_operator_information(self):
		missing_keys = None
		for key in ['steps_to_reseed', 'rounding']:
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
				error_msg += 'the steps_to_reseed and roundong parameters must be int \n'
				error_msg += 'data types (i.e. whole numbers).\n'
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
		print(to_print)

