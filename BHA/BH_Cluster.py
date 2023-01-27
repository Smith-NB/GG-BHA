from ase import Atoms
from BHA.T_SCM_Methods import get_CNA_profile
from asap3.analysis.localstructure import FullCNA
from collections import Counter
from uuid import uuid4

class Cluster():
	"""
	A class to store a description of a cluster
	Requires review.
	"""
	def __init__(self,
					composition = None,
					positions = None, 
					relaxed_positions = None, 
					cell = None, 
					BH_energy = None, 
					CNA_profile = None,
					atoms = None,
					UID = None):
		self.composition = composition
		self.positions = positions
		self.cell = cell
		self.BH_energy = BH_energy
		self.CNA_profile = CNA_profile
		self.relaxed_positions = relaxed_positions
		self.atoms = atoms
		self.UID = uuid4()
		print("Cluster UID: %s" % self.UID)

	def has_CNA_profile(self):
		return self.CNA_profile != None

	def has_energy(self):
		return self.BH_energy != None

	def calculate_CNA_profile(self, use_relaxed, r_Cut):
		formula = ""
		for element in self.composition: formula += str(element) + str(self.composition[element])
		if use_relaxed:
			a = Atoms(formula, positions = self.relaxed_positions, cell = self.cell)
			fcna = FullCNA(a, r_Cut)
			ncna = fcna.get_normal_cna()
			cna = Counter()
			for atom in ncna:
				cna += atom
			for sig in cna:
				cna[sig] = int(cna[sig]/2)
			self.CNA_profile = [cna]
			#self.CNA_profile = get_CNA_profile((Atoms(positions = self.relaxed_positions, cell = self.cell), [r_Cut]))
		else:
			a = Atoms(formula, positions = self.positions, cell = self.cell)
			fcna = FullCNA(a, r_Cut)
			ncna = fcna.get_normal_cna()
			cna = Counter()
			for atom in ncna:
				cna += atom
			for sig in cna:
				cna[sig] = int(cna[sig]/2)
			self.CNA_profile = [cna]
			#self.CNA_profile = get_CNA_profile((Atoms(positions = self.positions, cell = self.cell), [r_Cut]))