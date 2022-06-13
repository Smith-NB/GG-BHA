from BHA.Get_Starting_Structure import get_latest_structure, generate_random_structure
from os import path
from ase.io import read

def resume(self):
	"""
	Attempts to resume the algorithm from where the last run finished.
	"""
	print("Attempting to resume the basin hopping algorithm from where the last run finished.")
	if resuming_files_present(self):
		self.atoms = get_latest_structure(self.lm_trajectory)
		self.atoms.set_calculator(self.calculator)
		self.rmin = get_latest_structure(self.lowest_trajectory).get_positions()

		f = open('information_for_resuming.txt', 'r')

		self.steps_completed = int(f.readline().split(':')[1])
		self.Emin = float(f.readline().split(':')[1])
		self.Emin_found_at = int(f.readline().split(':')[1])
		self.reseed_operator.E_to_beat = float(f.readline().split(':')[1])
		self.reseed_operator.steps_since_improvement = int(f.readline().split(':')[1])
		self.hops_accepted_since_reseed = f.readline().split(':')[1].strip() == "True"
		
		if not self.hops_accepted_since_reseed:
			self.atoms = generate_random_structure(self.cluster_makeup, self.boxtoplaceinlength, self.vacuumAdd)
			self.atoms.set_calculator(self.calculator)

		target_energies_check = f.readline().strip().split(':')[1].split(',')
		for i in range(len(target_energies_check)):
			target_energies_check[i] = float(target_energies_check[i])
			if target_energies_check[i] != self.target_energies[i]:
				print("Failed to resume properly; the target energies in runBHA.py does not match that in")
				print("the information_for_resuming.txt file. The algorithm is not currently designed to")
				print("restart and look for new cluster(s) that differ from the original cluster(s).")
				print("The algorithm will exit without having started")
				from BHA.Lock import lock_remove
				lock_remove()
				exit()


		self.targets_found = f.readline().strip().split(':')[1].split(',')
		for i in range(len(self.targets_found)):
			self.targets_found[i] = False if self.targets_found[i] == "False" else int(self.targets_found[i])

		if not False in self.targets_found:
			print("\n--------------------------------\nThe target cluster(s) have already been located.\nThe basin hopping algorithm will exit without restarting.\n--------------------------------\n")
			from BHA.Lock import lock_remove
			lock_remove()
			exit()

		f.close()
		f = open('information_for_resuming.txt', 'r')
		for line in f:
			print(line, end='')
		f.close()
	else:
		print("Failed to resume properly.")
		from BHA.Lock import lock_remove
		lock_remove()
		exit()

def resuming_files_present(self):
	"""
	Checks nessecary files are present.
	"""
	if not isinstance(self.lm_trajectory, str) and not isinstance(self.lowest_trajectory, str) and not isinstance(self.logfile, str):
		return False
	if not path.exists(self.lm_trajectory):
		return False
	if not path.exists(self.lowest_trajectory):
		return False
	if not path.exists(self.logfile) or self.logfile == '-':
		return False
	if not path.exists('information_for_resuming.txt'):
		return False
	return True
