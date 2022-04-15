from abc import ABC, abstractmethod
import numpy as np
from BHA.ExternalDefinitions import get_coordination_number
class Atom_Selection(ABC):

	def __init__(self):
		pass

	def __repr__(self):
		return str(self.__dict__)

	@abstractmethod
	def get_atoms_to_mutate(self, atoms, n_atoms_to_mutate):

		pass

class Coordination_Atom_Selection(Atom_Selection):

	
	
	def __init__(self):
		super().__init__()

	def get_atoms_to_mutate(self, atoms, n_atoms_to_move):
		coord_list = get_coordination_number(atoms, 1.3549)
		coord_list = sorted(coord_list, key = lambda l:l[1])
		atoms_to_move = []
		i = 0
		while i < len(coord_list) and len(atoms_to_move) < n_atoms_to_move:
			j = i+1
			curr_coordination = coord_list[i][1]
			while j < len(coord_list) and coord_list[j][1] == curr_coordination:
				j += 1
			l = j-i
			if l + len(atoms_to_move) <= n_atoms_to_move:
				for x in range(i, j):
					atoms_to_move.append(coord_list[x][0])
			else:
				for a in range(n_atoms_to_move - len(atoms_to_move)):
					atoms_to_move.append(coord_list[np.random.randint(i, j)][0])
				break
			i = j
		return atoms_to_move

class Random_Atom_Selection(Atom_Selection):

	def __init__(self):
		super().__init__()

	def get_atoms_to_mutate(self, atoms, n_atoms_to_move):
		atoms_to_move = []
		cluster_size = len(atoms)
		n = 0
		while n < n_atoms_to_move:
			atom = np.random.randint(0, len(cluster_size))
			if not atom in atoms_to_move:
				atoms_to_move.append(atom)
				n += 1

		return atoms_to_move

def get_atom_selection(selection_criterion):
	if selection_criterion == 'random':
		return Random_Atom_Selection()
	elif selection_criterion == 'coordination':
		return Coordination_Atom_Selection()