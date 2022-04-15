from BHA.Reseed_Operators.Reseed_Operator import Reseed_Operator

class None_Reseed_Operator(Reseed_Operator):

	def __init__(self, reseed_operator_information, steps_since_improvement = None, E_to_beat = None):
		super().__init__(reseed_operator_information, steps_since_improvement, E_to_beat)

	
	def time_to_reseed(self, cluster):
		return False
	
	def check_reseed_operator_information(self):
		pass

	def print_reseed_operator_information(self):
		print("reseed Operator Name: None")

