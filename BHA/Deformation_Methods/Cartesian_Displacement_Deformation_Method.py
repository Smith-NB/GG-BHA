import numpy as np
from BHA.Deformation_Methods.Deformation_Method import Deformation_Method

class Cartesian_Displacement_Deformation_Method(Deformation_Method):

	def __init__(self, deformation_method_information):
		super().__init__(deformation_method_information)
		self.step_width = deformation_method_information['step_width']
	
	def get_deformed_coordinates(self, atoms):
		disp = np.random.uniform(-1., 1., (len(atoms), 3))
		disp *= self.step_width
		positions = atoms.get_positions()
		positions += disp
		return positions

	def check_deformation_method_information(self):
		if not 'step_width' in self.deformation_method_information:
			error_msg = '\n'
			error_msg += '--------------------------------------------------------'+'\n'
			error_msg += 'The following parameter(s) are missing from the deformation_method_information variable.\n'
			error_msg += 'step_width' + '.\n'
			error_msg += 'These parameter(s) are required for the Cartesian Displacement Deformation Method.\n'
			error_msg += 'The basin hopping algorithm with exit without starting.\n'
			error_msg += '--------------------------------------------------------'+'\n'
			print(error_msg)
			exit()
		if not isinstance(self.deformation_method_information['step_width'], int) and not isinstance(self.deformation_method_information['step_width'], float):
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'the step_width parameter must be float or int data \n'
			error_msg += 'types (i.e. numerical).\n'
			error_msg += 'Please check this parameter and try running the\n'
			error_msg += 'algorithm again.\n\n'
			error_msg += 'The basin hopping algorithm with exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			exit()

	def print_deformation_method_information(self):
			to_print = ''
			to_print += '\nDeformation Method Name: ' + self.deformation_method_information['method']
			to_print += '\nStep-Width: ' + str(self.deformation_method_information['step_width'])
			print(to_print)