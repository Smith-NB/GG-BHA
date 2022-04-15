import numpy as np
from BHA.Deformation_Methods.Deformation_Method import Deformation_Method
from BHA.ExternalDefinitions import InclusionRadiusOfCluster, get_distance, convert_spherical_to_cartesian

class Geometric_Center_Displacement_Deformation_Method(Deformation_Method):

	def __init__(self, deformation_method_information):
		super().__init__(deformation_method_information)
		self.alpha_min = deformation_method_information['alpha_min']
		self.alpha_max = deformation_method_information['alpha_max']
		self.weight = deformation_method_information['weight']

	def get_deformed_coordinates(self, atoms):
		radius = InclusionRadiusOfCluster(atoms)
		center_of_mass = atoms.get_center_of_mass()

		#calculate radial displacement direction and magnitude
		spherical_disp = np.random.uniform(0., 360., (len(atoms),2)) 	#angles
		dist = []
		#Scale displacement magnitude by min/max distance and distance to center of mass
		for i in range(len(atoms)):
			distance_to_center = get_distance(atoms[i].position, center_of_mass)
			dist.append((self.alpha_max - self.alpha_min) * (distance_to_center/radius)**self.weight + self.alpha_min)		#scale distance
		#convert to cartesian coordinates
		cart_disp = []
		for i in range(len(dist)):
			cart_disp.append(convert_spherical_to_cartesian(dist[i], spherical_disp[i][0], spherical_disp[i][1]))

		positions = atoms.get_positions()
		positions += cart_disp

		return positions

	def check_deformation_method_information(self):
		keys = ['alpha_min', 'alpha_max', 'weight']
		missing = []
		for key in keys:
			if not key in self.deformation_method_information:
				missing.append(key)
		if len(missing) > 0:
			error_msg = '\n'
			error_msg += '--------------------------------------------------------'+'\n'
			error_msg += 'The following parameter(s) are missing from the deformation_method_information variable.\n'
			error_msg += missing[0]
			for i in range(1, len(missing)):
				error_msg += ', %s' % missing[i]
			error_msg += '.\n'
			error_msg += 'These parameter(s) are required for the Geometric Center Displacement Deformation Method.\n'
			error_msg += 'The basin hopping algorithm with exit without starting.\n'
			error_msg += '--------------------------------------------------------'+'\n'
			print(error_msg)
			exit()
		for key in keys:
			if not isinstance(self.deformation_method_information[key], int) and not isinstance(self.deformation_method_information[key], float):
				error_msg = '\n'
				error_msg += '--------------------------------------------------------\n'
				error_msg += 'the %s parameter must be float or int data \n' % key
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
			to_print += '\nAlpha_min: ' + str(self.deformation_method_information['alpha_min'])
			to_print += '\nAlpha_max: ' + str(self.deformation_method_information['alpha_max'])
			to_print += '\nWeight: ' + str(self.deformation_method_information['weight'])
			print(to_print)