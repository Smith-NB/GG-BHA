import numpy as np
from BHA.T_SCM_Methods import get_CNA_similarity, get_CNA_profile
from Postprocessing_Programs.ClusterStructures import get_structure
from BHA.Get_Starting_Structure import get_calculator
from BHA.Search_Strategies.Search_Strategy import Search_Strategy
from BHA.BH_Cluster import Cluster

class Energy_Search_Strategy_For_LJ104_Oh_DAC_Test(Search_Strategy):

	def __init__(self, search_strategy_information):
		super().__init__(search_strategy_information)

		self.kT = self.search_strategy_information['temperature']
		self.sim = None
		self.ref = get_CNA_profile((get_structure("LJ104_ico"), [1.3549]))


	def get_acceptance_boolean(self, cluster_old, cluster_new):

		if not cluster_new.has_CNA_profile():
			cluster_new.calculate_CNA_profile(self.use_relaxed, self.r_Cut)

		self.sim = get_CNA_similarity(self.ref, cluster_new.CNA_profile)/100
		print("similarity = " + str(self.sim*100) + " %.")

		if self.sim > 0.40:
			return False

		if cluster_new.BH_energy < cluster_old.BH_energy:
			return True
			
		probability = np.exp((cluster_old.BH_energy - cluster_new.BH_energy) / self.kT)
		print("Chance to accept = " + str(probability))
		accept = probability > np.random.uniform()
		return accept

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
