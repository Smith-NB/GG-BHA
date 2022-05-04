#Test edit for git
import numpy as np

#from ase.visualize import view
from ase.optimize.fire import FIRE
from ase.parallel import world
from ase.io import read

from BHA.BH_Cluster import Cluster
from BHA.BH_Initialise import initialise
from BHA.Get_Starting_Structure import generate_random_structure
from BHA.Lock import lock_remove

from BHA.T_SCM_Methods import get_CNA_similarity
from ase import Atoms
class BasinHopping():
	"""
	Basin hopping algorithm.

	After Wales and Doye, J. Phys. Chem. A, vol 101 (1997) 5111-5116

	and

	David J. Wales and Harold A. Scheraga, Science, Vol. 285, 1368 (1999)

	ASE Source code adapted by Nicholas Smith

	:param atoms: The system/cluster
	:type  atoms: ase.atoms
	:param optimizer: The optimizer to use for energy minimisations
	:type  optimizer: ase.optimize.optimize.Optimizer implementation
	:param fmax: maximal force for the optimizer
	:type  fmax: float
	:param dr: maximal stepwidth
	:type  dr: float
	:param steps_to_reseed: The number of steps afterwhich, if there has been no improvement to energy
	:type  steps_to_reseed: int
	:param boxtoplaceinlength: This is the length of the box you would like to place atoms in to make a randomly constructed cluster.
	:type  boxtoplaceinlength: float
	:param vacuumAdd: The length of vacuum added around the cluster. Written in A.
	:type  vacuumAdd: float
	:param logfile: File to log basin hopping algorithm output to. Use '-' for stdout.
	:type  logfile: File or str
	:param trajectory: File used to store trajectory of atomic movement for ACCEPTED steps.
	:type  trajectory: str
	:param optimizer_logfile: Logfile for the optimizer to use
	:type  optimizer_logfiele: str
	:param search_strategy_information: All information for the search strategy to use. Default {'search_strategy': 'Energy'}
	:type  search_strategy_information: dict
	:param exit_when_targets_found: boolean for wether or not to exit the algorithm when the GM is found.
	:type  exit_when_targets_found: bool
	:param target_energies: the energy of the GM.
	:type  target_energies: list of float or int
	:param rounding: decimal places to round to for comparing cluster energy to GM. Default = 2
	:type  rounding: int
	:param adjust_cm: Something to do with centre of mass
	:type  adjust_cm: bool
	"""
	def __init__(self, cluster_makeup,
				 optimizer=FIRE,
				 fmax=0.01,
				 dr=0.1,
				 reseed_operator_information={'reseed_operator': 'none'},
				 boxtoplaceinlength = 4.1,
				 vacuumAdd = 10,
				 logfile='log.txt',
				 trajectory='lowest.traj',
				 optimizer_logfile=None,
				 local_minima_trajectory='local_minima.traj',
				 search_strategy_information={'search_strategy': 'energy', 'temperature': 1.0},
				 exit_when_targets_found=False,
				 target_energies=None,
				 rounding=2,
				 adjust_cm=True,
				 total_length_of_running_time = 1
				):
		self.cluster_makeup = cluster_makeup
		self.optimizer = optimizer
		self.fmax = fmax
		self.dr = dr
		self.reseed_operator_information = reseed_operator_information
		self.boxtoplaceinlength = boxtoplaceinlength
		self.vacuumAdd = vacuumAdd
		self.logfile = logfile
		self.lowest_trajectory = trajectory
		self.optimizer_logfile = optimizer_logfile
		self.lm_trajectory = local_minima_trajectory
		self.search_strategy_information = search_strategy_information
		self.exit_when_targets_found = exit_when_targets_found
		self.target_energies = target_energies
		self.rounding = rounding
		self.adjust_cm = adjust_cm
		self.total_length_of_running_time = total_length_of_running_time
		print("v1.1.4")
		initialise(self)

	def run(self, steps):
		"""
		Hop the basins for specified number of steps.

		:param steps: number of steps to hop for.
		:type  steps: int
		"""

		print("--------------------------------")
		print("--------------------------------")
		print("Starting Basin Hopping Algorithm")
		print("--------------------------------")
		print("--------------------------------\n")

		cluster_old = Cluster(composition=self.cluster_makeup, positions = self.positions.copy(), cell = self.cell)
		cluster_old.BH_energy = self.get_transformed_energy(cluster_old.positions)
		cluster_old.relaxed_positions = self.atoms.get_positions()
		cluster_old.atoms = self.atoms.copy()
		#Complete the specified number of steps
		for step in range(steps):
			print("\n================================\n")
			print("Attempting step " + str(step) + ".")

			#generate a new cluster by perturbing the coordinates of the most recent cluster
			cluster_new = Cluster(composition=self.cluster_makeup, positions = self.move(cluster_old.relaxed_positions), cell = self.cell)
			#get the energy at the nearest minimim of the new cluster
			cluster_new.BH_energy = self.get_transformed_energy(cluster_new.positions)
			#set the new clusters atomic positions to that at the nearest local minimum            
			cluster_new.relaxed_positions = self.atoms.get_positions()
			cluster_new.atoms = self.atoms.copy()
			print("Generated new cluster, E = " + str(cluster_new.BH_energy) + " eV.")

			## If a new LES is found, update LES info. ##
			if cluster_new.BH_energy < self.Emin:
				print("A new overall LES has been found.")
				self.Emin = cluster_new.BH_energy
				self.Emin_found_at = step + self.steps_completed
				self.rmin = self.atoms.get_positions() #relaxed positions               
				self.store_structure(self.lowest_trajectory, self.atoms)			
					
				
			
			## Accept the new structure if its a lower energy structure. ##
			accept = self.search_strategy.get_acceptance_boolean(cluster_old, cluster_new)
			accept_str = "accepted." if accept else "rejected."
			print("The current step has been " + accept_str)
			self.log(step + self.steps_completed, cluster_new.BH_energy, self.Emin, accept, self.search_strategy.sim)

			## If this step has been accepted, update cluster_old and log relevant info. ##
			if accept:
				self.hops_accepted_since_reseed = True
				cluster_old = cluster_new
				self.store_structure(self.lm_trajectory, self.atoms)
				self.atoms.set_positions(cluster_new.positions)

			## Check if all target clusters have been located. ##
			if self.exit_when_targets_found:
				for i in range(len(self.target_energies)):
					if self.targets_found[i] == False and round(cluster_new.BH_energy, self.rounding) == self.target_energies[i]:
						self.targets_found[i] = step + self.steps_completed
				if not False in self.targets_found:
					print('All target clusters found based on energy.')
					
					print('target_energies: %.2f' % self.target_energies[0], end='')
					for i in range(1, len(self.target_energies)):
						print(', %.2f' % self.target_energies[i], end='')
					print()

					print('targets_found: %d' % self.targets_found[0])
					for i in range(1, len(self.targets_found)):
						print(', %d' % self.targets_found[i], end='')
					print()
					self.log(step + self.steps_completed, cluster_new.BH_energy, self.Emin, accept)
					self.log_resumption_info(step, cluster_new.BH_energy)
					break
				"""
				if round(self.Emin, self.rounding) == round(self.target_energies, self.rounding):   
					print('GM Found at ' + str(self.target_energies) + ' eV.')
					self.store_structure(self.lm_trajectory, self.atoms)
					self.atoms.set_positions(cluster_new.positions)
					self.log(step + self.steps_completed, cluster_new.BH_energy, self.Emin, True)
					self.log_resumption_info(step, cluster_new.BH_energy)
					break #End the algorithm
				"""

			## If reseeding is enabled and a new LES was not found. ##
			if self.reseed_operator.time_to_reseed(cluster_old):
				print(str(self.reseed_operator_information['steps_to_reseed']) + " steps have occured since the last improvement. reseeding.")
				#self.log(step + self.steps_completed, cluster_new.BH_energy, self.Emin, False)
				cluster_old = self.restart_search_from_random_start()
				self.hops_accepted_since_reseed = False
				continue


			if self.timer.has_elapsed_time():
				print("\nRun time has exceeded specified walltime.")
				print("The algorithm will begin to exit after " + str(step) + " steps were completed in this run.")
				break
		## Log any information nessecary for resuming the algorithm. ##
		self.log_resumption_info(step, cluster_old.BH_energy)
		print("\nThe basin hopping algorithm will now exit safely.")
		lock_remove()        

	def store_structure(self, storage_file, structure):
		if storage_file is not None:
			storage_file.write(structure)

	def restart_search_from_random_start(self):
		self.atoms = generate_random_structure(self.cluster_makeup, self.boxtoplaceinlength, self.vacuumAdd)
		cluster = Cluster(composition=self.cluster_makeup, positions = self.atoms.get_positions(), cell = self.cell)
		cluster.BH_energy = self.get_transformed_energy(self.atoms.get_positions())
		cluster.relaxed_positions = self.atoms.get_positions()
		cluster.atoms = self.atoms.copy()
		self.reseed_operator.E_to_beat = cluster.BH_energy
		self.logfile.write("RESEED\n")
		self.logfile.flush()
		return cluster


	def log_resumption_info(self, step, energy):
		print("\nLogging resumption information for any future runs.")
		f = open("information_for_resuming.txt", 'w')
		f.write("Steps_completed:" + str(step + self.steps_completed + 1))
		f.write("\nMinimum_energy:" + str(self.Emin))
		f.write("\nMinimum_energy_found_at_step:" + str(self.Emin_found_at))
		f.write("\nreseed_energy_to_beat:" + str(self.reseed_operator.E_to_beat))
		f.write("\nSteps_since_improvement:" + str(self.reseed_operator.steps_since_improvement))
		f.write("\nhops_accepted_since_reseed:" + str(self.hops_accepted_since_reseed))
		f.write("\ntarget_energies:" + str(self.target_energies[0]))
		for i in range(1, len(self.target_energies)):
			f.write("," + str(self.target_energies[i]))
		
		f.write("\ntargets_found:" + str(self.targets_found[0]))
		for i in range(1, len(self.targets_found)):
			f.write("," + str(self.targets_found[i]))
		f.flush()
		f.close()

		if hasattr(self.search_strategy, 'population'):
			self.search_strategy.population.controller.log_population_controller_resumption_info()

		if hasattr(self.reseed_operator, 'blacklist'):
			self.reseed_operator.blacklist.controller.log_population_controller_resumption_info()

		

	def log(self, step, En, Emin, accepted, sim=None):
		if self.logfile is None:
			return
		if sim == None:
			self.logfile.write('step %d, energy %15.6f, emin %15.6f, accepted %s, similarity None\n'
								% (step, En, Emin, str(accepted)))
		else:
			self.logfile.write('step %d, energy %15.6f, emin %15.6f, accepted %s, similarity %10.7f\n'
								% (step, En, Emin, str(accepted), sim))

		self.logfile.flush()

	def move(self, pos_old):
		"""Move atoms by a random step."""
		atoms = self.atoms
		# displace coordinates
		disp = np.random.uniform(-1., 1., (len(atoms), 3))
		rn = pos_old + self.dr * disp
		atoms.set_positions(rn)
		if self.cm is not None:
			cm = atoms.get_center_of_mass()
			atoms.translate(self.cm - cm)
		rn = atoms.get_positions()
		world.broadcast(rn, 0)
		atoms.set_positions(rn)
		return atoms.get_positions()

	def get_minimum(self):
		"""Return minimal energy and configuration."""
		atoms = self.atoms.copy()
		atoms.set_positions(self.rmin)
		return self.Emin, atoms

	def get_transformed_energy(self, positions):
		"""Return the energy of the nearest local minimum."""
		if np.sometrue(self.positions != positions):
			self.positions = positions
			self.atoms.set_positions(positions)
			opt = self.optimizer(self.atoms,
								 logfile=self.optimizer_logfile)
			opt.run(fmax=self.fmax)
		energy = self.atoms.get_potential_energy()
		return energy

	def todict(self):
		d = {'type': 'optimization',
			 'optimizer': self.__class__.__name__,
			 'local-minima-optimizer': self.optimizer.__name__,
			 'max-force': self.fmax,
			 'maximal-step-width': self.dr}
		return d
