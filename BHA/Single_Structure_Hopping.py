import numpy as np

from ase.optimize.fire import FIRE
from ase.io.trajectory import Trajectory
from BHA.T_SCM_Methods import get_CNA_similarity, get_CNA_profile
from BHA.BH_Cluster import Cluster
from ase import Atoms
from asap3.Internal.BuiltinPotentials import LennardJones
from BHA.Deformation_Methods.Get_Deformation_Method import get_deformation_method
class SingleStructureHopping():
	"""Basin hopping algorithm.

	After Wales and Doye, J. Phys. Chem. A, vol 101 (1997) 5111-5116

	and

	David J. Wales and Harold A. Scheraga, Science, Vol. 285, 1368 (1999)
	"""

	def __init__(self, atoms,
				optimizer=FIRE,
				fmax=0.01,
				logfile='SS_log.txt',
				local_minima_trajectory='SS_local_minima.traj',
				adjust_cm=True,
				deformation_method_information={"method": "cartesian", "stepwidth": 0.4}
				):
		"""Parameters:

		atoms: Atoms object
			The Atoms object to operate on.

		trajectory: string
			Pickle file used to store trajectory of atomic movement.

		logfile: file object or str
			If *logfile* is a string, a file with that name will be opened.
			Use '-' for stdout.
		"""
		self.atoms = atoms
		self.atoms.set_calculator(self.get_calculator())
		self.cell = self.atoms.get_cell()
		self.optimizer = optimizer
		self.fmax = fmax
		if adjust_cm:
			self.cm = atoms.get_center_of_mass()
		else:
			self.cm = None
		self.logfile = logfile
		if isinstance(self.logfile, str):
			self.logfile = open(self.logfile, 'a')
		self.lm_trajectory = local_minima_trajectory
		if isinstance(self.lm_trajectory, str):
			self.lm_trajectory = Trajectory(self.lm_trajectory, 'a', self.atoms)
		self.deformation_method_information = deformation_method_information
		self.initialize()
		

	def initialize(self):
		self.positions = 0.0 * self.atoms.get_positions()
		self.Emin = self.get_transformed_energy(self.atoms.get_positions()) or 1.e32
		self.rmin = self.atoms.get_positions()
		self.positions = self.atoms.get_positions()

		self.deformation_method = get_deformation_method(self.deformation_method_information)

	def run(self, steps):
		"""Hop the basins for defined number of steps."""
		from ase.visualize import view
		r_cut = 1.3549
		print("---------------------------------")
		print("---------------------------------")
		print("Starting Single Structure Hopping")
		print("-------------v_1.0.8-------------")
		print("---------------------------------")
		print("---------------------------------\n")

		cluster_old = Cluster(positions = self.positions.copy(), cell = self.cell)
		cluster_old.BH_energy = self.get_transformed_energy(cluster_old.positions)
		cluster_old.relaxed_positions = self.atoms.get_positions()
		cluster_old.calculate_CNA_profile(True, r_cut)
		#Complete the specified number of steps
		for step in range(steps):
			print("\n================================\n")
			print("Attempting step " + str(step) + ".")
			self.atoms.set_positions(cluster_old.relaxed_positions)
			new_positions = self.deformation_method.get_deformed_coordinates(self.atoms)
			cluster_new = Cluster(positions = new_positions, cell = self.cell)
			self.atoms.set_positions(new_positions)
			cluster_new.BH_energy = self.get_transformed_energy(cluster_new.positions)
			cluster_new.relaxed_positions = self.atoms.get_positions()
			cluster_new.calculate_CNA_profile(True, r_cut)
			sim = get_CNA_similarity(cluster_old.CNA_profile, cluster_new.CNA_profile)
			self.store_structure(self.lm_trajectory, self.atoms)
			print("Generated new cluster, E = " + str(cluster_new.BH_energy) + " eV.")
			print("similarity = " + str(sim) + " %.")
			print("\n================================\n")
			self.log(step, cluster_new.BH_energy, sim)
	def log(self, step, En, sim):
		if self.logfile is None:
			return
		self.logfile.write('step %d, energy %15.6f, similarity %15.6f\n'
						   % (step, En, sim))
		self.logfile.flush()

	def get_transformed_energy(self, positions):
		"""Return the energy of the nearest local minimum."""
		if np.sometrue(self.positions != positions):
			self.positions = positions
			self.atoms.set_positions(positions)
			opt = self.optimizer(self.atoms, logfile=None)
			opt.run(fmax=self.fmax)
		energy = self.atoms.get_potential_energy()
		return energy

	def store_structure(self, storage_file, structure):
		if storage_file is not None:
			storage_file.write(structure)

	def get_calculator(self):
		elements = [10]; sigma = [1]; epsilon = [1]; rCut = 1000;
		lj_calc = LennardJones(elements, epsilon, sigma, rCut=rCut, modified=True)
		return lj_calc