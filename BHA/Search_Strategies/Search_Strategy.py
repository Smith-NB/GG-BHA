from abc import ABC, abstractmethod

class Search_Strategy(ABC):

	def __init__(self, search_strategy_information):
		self.search_strategy_information = search_strategy_information
		self.reseed_operator_pointer = self.search_strategy_information['reseed_operator_pointer']
		self.reseed_operator_pointer.set_search_strategy_pointer(self)
		self.check_search_strategy_information()
		self.print_search_strategy_information()
		
	def __repr__(self):
		return str(self.__dict__)

	@abstractmethod
	def handle_reseed_triggering(self):

		pass

	@abstractmethod
	def get_acceptance_boolean(self, cluster_old, cluster_new, kT):

		pass

	@abstractmethod
	def check_search_strategy_information(self):

		pass

	@abstractmethod
	def print_search_strategy_information(self):

		pass