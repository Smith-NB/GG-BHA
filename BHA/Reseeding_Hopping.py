import numpy as np

from ase.optimize.fire import FIRE
from ase.io.trajectory import Trajectory
from BHA.T_SCM_Methods import get_CNA_similarity, get_CNA_profile
from BHA.BH_Cluster import Cluster
from BHA.Get_Starting_Structure import generate_random_structure
from ase import Atoms
from asap3.Internal.BuiltinPotentials import LennardJones
from Postprocessing_Programs.ClusterStructures import get_structure

class ReseedingHopping():
	"""Basin hopping algorithm.

	After Wales and Doye, J. Phys. Chem. A, vol 101 (1997) 5111-5116

	and

	David J. Wales and Harold A. Scheraga, Science, Vol. 285, 1368 (1999)
	"""

	def __init__(self, cluster_makeup, structure_to_compare,
				optimizer=FIRE,
				fmax=0.01,
				dr=0.4,
				logfile='SS_log.txt',
				local_minima_trajectory='SS_local_minima.traj',
				boxtoplaceinlength = 4.1,
				vacuumAdd = 10,
				adjust_cm=True):
		"""Parameters:

		atoms: Atoms object
			The Atoms object to operate on.

		trajectory: string
			Pickle file used to store trajectory of atomic movement.

		logfile: file object or str
			If *logfile* is a string, a file with that name will be opened.
			Use '-' for stdout.
		"""
		self.cluster_makeup = cluster_makeup
		self.structure_to_compare = structure_to_compare
		self.boxtoplaceinlength = boxtoplaceinlength
		self.vacuumAdd = vacuumAdd

		self.atoms = generate_random_structure(self.cluster_makeup, self.boxtoplaceinlength, self.vacuumAdd)
		self.atoms.set_calculator(self.get_calculator())
		self.cell = self.atoms.get_cell()
		self.optimizer = optimizer
		self.fmax = fmax
		self.dr = dr

		if adjust_cm:
			self.cm = self.atoms.get_center_of_mass()
		else:
			self.cm = None
		self.logfile = logfile
		if isinstance(self.logfile, str):
			self.logfile = open(self.logfile, 'a')
		self.lm_trajectory = local_minima_trajectory
		if isinstance(self.lm_trajectory, str):
			self.lm_trajectory = Trajectory(self.lm_trajectory, 'a', self.atoms)
		self.initialize()
		

	def initialize(self):
		self.positions = 0.0 * self.atoms.get_positions()
		self.Emin = self.get_transformed_energy(self.atoms.get_positions()) or 1.e32
		self.rmin = self.atoms.get_positions()
		self.positions = self.atoms.get_positions()

	def run(self, steps):
		"""Hop the basins for defined number of steps."""
		r_cut = 1.3549
		print("---------------------------------")
		print("---------------------------------")
		print("---Starting Reseeding Hopping----")
		print("-------------v_1.0.7-------------")
		print("---------------------------------")
		print("---------------------------------\n")

		GM = get_structure(self.structure_to_compare)
		GM_CNA_profile = get_CNA_profile((GM, [1.3549]))

		for step in range(steps):
			print("\n================================\n")
			print("Attempting step " + str(step) + ".")
			cluster = generate_random_structure(self.cluster_makeup, self.boxtoplaceinlength, self.vacuumAdd)
			cluster = Cluster(positions = cluster.get_positions(), cell = self.cell)
			cluster.BH_energy = self.get_transformed_energy(cluster.positions)
			cluster.relaxed_positions = self.atoms.get_positions()
			cluster.calculate_CNA_profile(True, r_cut)
			sim_to_GM = get_CNA_similarity(cluster.CNA_profile, GM_CNA_profile)
			self.store_structure(self.lm_trajectory, self.atoms)
			print("Generated new cluster, E = " + str(cluster.BH_energy) + " eV.")
			print("\n================================\n")
			self.log(step, cluster.BH_energy, sim_to_GM)


	def log(self, step, En, sim):
		if self.logfile is None:
			return
		self.logfile.write('step %6d, energy %15.6f, similarity to GM %15.6f\n'
						   % (step, En, sim))
		self.logfile.flush()

	def move(self, ro):
		"""Move atoms by a random step."""
		atoms = self.atoms
		# displace coordinates
		disp = np.random.uniform(-1., 1., (len(atoms), 3))
		rn = ro + self.dr * disp
		atoms.set_positions(rn)
		if self.cm is not None:
			cm = atoms.get_center_of_mass()
			atoms.translate(self.cm - cm)
		rn = atoms.get_positions()
		atoms.set_positions(rn)
		return atoms.get_positions()

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
