import numpy as np
from BHA.Search_Strategies.Search_Strategy import Search_Strategy
class Energy_Search_Strategy(Search_Strategy):

	def __init__(self, search_strategy_information):
		super().__init__(search_strategy_information)

		self.kT = self.search_strategy_information['temperature']
		self.sim = None
		self.r_Cut = 3.47646753
		self.cnalog = open("CNAlog.txt", "a")

	def get_acceptance_boolean(self, cluster_old, cluster_new):

		if not cluster_new.has_CNA_profile():
			cluster_new.calculate_CNA_profile(True, self.r_Cut)

		if cluster_new.BH_energy < cluster_old.BH_energy:
			self.log_CNA(cluster_new.CNA_profile)
			return True
			
		probability = np.exp((cluster_old.BH_energy - cluster_new.BH_energy) / self.kT)
		print("Chance to accept = " + str(probability))
		accept = probability > np.random.uniform()
		if accept: 
			self.log_CNA(cluster_new.CNA_profile)
		return accept

	def log_CNA(self, cna):
		cna = cna[0]
		cna_string = ""
		for sig in cna:
			cna_string += "%d," % sig[0]
			cna_string += "%d," % sig[1]
			cna_string += "%d:" % sig[2]
			cna_string += "%d;" % cna[sig]
		self.cnalog.write("%s\n" % cna_string)

	def handle_reseed_triggering(self):
		super().handle_reseed_triggering()

	def check_search_strategy_information(self):
		if not 'temperature' in self.search_strategy_information:
			error_msg = '\n'
			error_msg += '--------------------------------------------------------'+'\n'
			error_msg += 'The following parameter(s) are missing from the search_strategy_information variable.\n'
			error_msg += 'temperature' + '.\n'
			error_msg += 'These parameter(s) are required for the Energy Search Strategy.\n'
			error_msg += 'The basin hopping algorithm with exit without starting.\n'
			error_msg += '--------------------------------------------------------'+'\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()
		if not isinstance(self.search_strategy_information['temperature'], float) and not isinstance(self.search_strategy_information['temperature'], int):
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'the temperature parameter must be float or int data \n'
			error_msg += 'types (i.e. numerical).\n'
			error_msg += 'Please check this parameter and try running the\n'
			error_msg += 'algorithm again.\n\n'
			error_msg += 'The basin hopping algorithm with exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()

	def print_search_strategy_information(self):
		to_print = ''
		to_print += '\nSearch Strategy Name: ' + self.search_strategy_information['search_strategy']
		to_print += '\nTemperature: ' + str(self.search_strategy_information['temperature'])
		print(to_print)
