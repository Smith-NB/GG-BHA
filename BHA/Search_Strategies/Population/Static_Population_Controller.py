from BHA.Search_Strategies.Population.Population_Controller import Population_Controller

class Static_Population_Controller(Population_Controller):
	"""
	This population controller is intended for an 'a priori' test, where the population is
	pre-defined and kept static, i.e. the population never changed from its initial state.
	"""
	def __init__(self, population_controller_information):
		super().__init__(population_controller_information)

	def time_to_update(self, cluster):
		"""
		Checks if any clusters in the premature_clusters list have matured.
		Also checks if its time to append to the premature_cluster list.
		"""
		return False

	def get_cluster_to_append(self):
		"""
		Retrieves the matured cluster to be added to the population.
		Should be the cluster at index 0 if self.premature_clusters

		returns: CNA profile of the cluster to append.
		rtype: Counter
		"""
		pass

	def check_population_controller_information(self):
		pass

	def print_population_controller_information(self):
		"""
		Prints information about the search strategy.
		"""
		to_print = ''
		to_print += '\nPopulation Controller Name: ' + self.population_controller_information['population_controller']
		print(to_print)

	def log_population_controller_resumption_info(self):
		pass