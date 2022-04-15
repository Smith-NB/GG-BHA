from abc import ABC, abstractmethod

class Reseed_Operator(ABC):

	def __init__(self, reseed_operator_information, steps_since_improvement = None, E_to_beat = None):
		self.reseed_operator_information = reseed_operator_information
		self.steps_since_improvement = steps_since_improvement
		self.E_to_beat = E_to_beat
		self.check_reseed_operator_information()
		self.print_reseed_operator_information()
	def __repr__(self):
		return str(self.__dict__)

	# this function is called by BHA.Search_Strategy.__init__() and opens a line of communication from the reseed operator
	# to the search strategy. The reverse line of communication (allowing the search strategy object to commuicate with
	# the reseed operator) is passed to the search strategy object in BHA.BH_Initialise.initialise().
	def set_search_strategy_pointer(self, search_strategy_pointer):
		self.search_strategy_pointer = search_strategy_pointer

	@abstractmethod
	def time_to_reseed(self, cluster):

		pass

	@abstractmethod
	def check_reseed_operator_information(self):

		pass

	@abstractmethod
	def print_reseed_operator_information(self):

		pass