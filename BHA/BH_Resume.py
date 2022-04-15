from BHA.Get_Starting_Structure import get_latest_structure
from os import path
from ase.io import read

def resume(self):
	"""
	Attempts to resume the algorithm from where the last run finished.
	"""
	print("Attempting to resume the basin hopping algorithm from where the last run finished.")
	if resuming_files_present(self):
		self.atoms = get_latest_structure(self.lm_trajectory)
		self.rmin = get_latest_structure(self.lowest_trajectory).get_positions()

		f = open('information_for_resuming.txt', 'r')

		self.steps_completed = int(f.readline().split(':')[1])
		self.Emin = float(f.readline().split(':')[1])
		self.Emin_found_at = int(f.readline().split(':')[1])
		self.reseed_operator.E_to_beat = float(f.readline().split(':')[1])
		self.reseed_operator.steps_since_improvement = int(f.readline().split(':')[1])
		if round(self.Emin, self.rounding) == round(self.GM_energy, self.rounding):
			print("\n--------------------------------\nThe GM has already been located.\nThe basin hopping algorithm will exit without restarting.\n--------------------------------\n")
			from BHA.Lock import lock_remove
			lock_remove()
			exit()

		to_print = ''
		to_print += '\nSteps completed in previos run(s): ' + str(self.steps_completed)
		to_print += '\nEmin found in previous run(s): ' + str(self.Emin)
		to_print += '\nEmin found since last reseed: ' + str(self.reseed_operator.E_to_beat)
		to_print += '\nSteps since a new LES was found from last reseed: ' + str(self.reseed_operator.steps_since_improvement)
		print(to_print)
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
