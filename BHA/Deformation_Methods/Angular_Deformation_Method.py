import numpy as np
from BHA.Deformation_Methods.Deformation_Method import Deformation_Method
from BHA.Deformation_Methods.Atom_Selection import get_atom_selection
from BHA.ExternalDefinitions import InclusionRadiusOfCluster, convert_spherical_to_cartesian

class Angular_Deformation_Method(Deformation_Method):

	def __init__(self, deformation_method_information):
		super().__init__(deformation_method_information)
		self.n_atoms_to_move = deformation_method_information['n_atoms_to_move']
		self.selection_criterion = deformation_method_information['selection_criterion']
		self.atom_selection = get_atom_selection(self.selection_criterion)

	def get_deformed_coordinates(self, atoms):
		if self.n_atoms_to_move > len(atoms): self.n_atoms_to_move = len(atoms)

		radius = InclusionRadiusOfCluster(atoms)
		center_of_mass = atoms.get_center_of_mass()
		spherical_disp = np.random.uniform(0., 360., (self.n_atoms_to_move, 2))
		cart_coords = []
		for i in range(self.n_atoms_to_move):
			cart_coords.append(convert_spherical_to_cartesian(radius, spherical_disp[i][0], spherical_disp[i][1]))
			cart_coords[i] += center_of_mass

		atoms_to_move = self.atom_selection.get_atoms_to_mutate(atoms, self.n_atoms_to_move)
		positions = atoms.get_positions()
		for i in range(self.n_atoms_to_move):
			positions[atoms_to_move[i]] = cart_coords[i]

		return positions


	def check_deformation_method_information(self):
		keys = ['n_atoms_to_move', 'selection_criterion']
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
			error_msg += 'These parameter(s) are required for the Angular Deformation Method.\n'
			error_msg += 'The basin hopping algorithm with exit without starting.\n'
			error_msg += '--------------------------------------------------------'+'\n'
			print(error_msg)
			exit()
		if not isinstance(self.deformation_method_information['n_atoms_to_move'], int):
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'the n_atoms_to_move parameter must be an int data type.\n'
			error_msg += 'Please check this parameter and try running the\n'
			error_msg += 'algorithm again.\n\n'
			error_msg += 'The basin hopping algorithm with exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			exit()
		if not isinstance(self.deformation_method_information['selection_criterion'], str):
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'the selection_criterion parameter must be a str data type.\n'
			error_msg += 'Please check this parameter and try running the\n'
			error_msg += 'algorithm again.\n\n'
			error_msg += 'The basin hopping algorithm with exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			exit()

	def print_deformation_method_information(self):
			to_print = ''
			to_print += '\nDeformation Method Name: ' + self.deformation_method_information['method']
			to_print += '\nNumber of atoms to move: ' + str(self.deformation_method_information['n_atoms_to_move'])
			to_print += '\nSelection Criterion: ' + str(self.deformation_method_information['selection_criterion'])
			print(to_print)