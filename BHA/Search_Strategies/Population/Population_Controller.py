from abc import ABC, abstractmethod

class Population_Controller(ABC):

	def __init__(self, population_controller_information):
		self.population_controller_information = population_controller_information
		self.client = self.population_controller_information['client']
		self.check_population_controller_information()
		self.print_population_controller_information()

	def __repr__(self):
		return str(self.__dict__)

	@abstractmethod
	def time_to_update(self, cluster):

		pass

	@abstractmethod
	def get_cluster_to_append(self):

		pass

	@abstractmethod
	def notify_reseed_has_occured(self):

		pass

	@abstractmethod
	def check_population_controller_information(self):

		pass

	@abstractmethod
	def print_population_controller_information(self):

		pass

	@abstractmethod
	def log_population_controller_resumption_info(self):

		pass