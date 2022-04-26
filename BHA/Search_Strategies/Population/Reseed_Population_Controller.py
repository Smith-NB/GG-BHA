from BHA.Search_Strategies.Population.Population_Controller import Population_Controller
from ase.io import Trajectory
class Reseed_Population_Controller(Population_Controller):
	"""
	The Periodic Population Controller updates the population after a specified period. 
	A cluster maturity age can also be specified, where clusters will only be added to the
	population after they reach a certain age (measured in number of attempted hops).
	"""

	def __init__(self, population_controller_information):
		super().__init__(population_controller_information)
		self.current_LES_since_last_update = None
		self.cluster_to_append = None
		self.reseed_triggered_last_hop = False

	def time_to_update(self, cluster):
		if self.reseed_triggered_last_hop:
			if self.current_LES_since_last_update is None:
				self.current_LES_since_last_update = cluster
			self.reseed_triggered_last_hop = False
			self.cluster_to_append = self.current_LES_since_last_update
			self.current_LES_since_last_update = None
			return True

		if self.current_LES_since_last_update is None or cluster.BH_energy < self.current_LES_since_last_update.BH_energy:
			self.current_LES_since_last_update = cluster
		return False


	def get_cluster_to_append(self):
		cluster_to_append = self.cluster_to_append
		self.cluster_to_append = None
		return cluster_to_append

	def notify_reseed_has_occured(self):
		self.reseed_triggered_last_hop = True		

	def log_population_controller_resumption_info(self):
		f = open("information_for_resuming.txt", "a")
		f.write('\nInformation for Reseed_Population_Controller; client = %s\n' % self.client)
		
		if self.current_LES_since_last_update is not None:
			f.write('Begin .xyz file formatted text for current_LES_since_last_update cluster:\n')
			from ase.io import write
			write("temp.xyz", self.current_LES_since_last_update.atoms, format='xyz')
			xyz = open('temp.xyz', 'r')
			for line in xyz:
				f.write(line)
			xyz.close()
			import os
			os.remove('temp.xyz')
			f.write('End .xyz file formatted text for current_LES_since_last_update cluster\n')

			f.write('begin CNA profile of current_LES_since_last_update\n')
			for sig in self.current_LES_since_last_update.CNA_profile[0]:
				f.write(str(sig).replace(' ', '').replace('(', '').replace(')', '') + ':')
				f.write(str(self.current_LES_since_last_update.CNA_profile[0][sig]) + ';')
			f.write('\n')
			f.write("end CNA profiles of current_LES_since_last_update\n")	
		else:
			f.write("There is no current_LES_since_last_update at this time.\n")
		


		f.write("reseed_triggered_last_hop: %s" % str(self.reseed_triggered_last_hop))
	
	def retrieve_resumption_info(self):
		from collections import Counter
		from ase.io import Trajectory
		from BHA.BH_Cluster import Cluster
		from BHA.Get_Starting_Structure import get_calculator
		import shutil

		f = open("information_for_resuming.txt", "r")
		line = f.readline() 
		if not line.startswith("Information for") or not line.strip().endswith("Reseed_Population_Controller; client = %s" % self.client): #check population controller is 
			found_correct_info_block = False
			for l in f:
				if l.startswith("Information for") and l.strip().endswith("Reseed_Population_Controller; client = %s" % self.client):
					line = l
					found_correct_info_block = True
					break
			if not found_correct_info_block:
				print("Failed to resume properly; population controller mismatch")
				from BHA.Lock import lock_remove
				lock_remove()
				exit()


		line = f.readline()
		if "There is no current_LES_since_last_update at this time." in line:
			self.current_LES_since_last_update = None
		else:
			xyz = open('temp.xyz', 'w')
			line = f.readline()
			while not "End .xyz file formatted text for current_LES_since_last_update cluster" in line:
				xyz.write(line)
				line = f.readline()
			xyz.close()
			from ase.io import read
			self.current_LES_since_last_update = read('temp.xyz', format='xyz')
			import os
			os.remove('temp.xyz')

			#Create BHA.BH_Cluster Object
			lj = get_calculator()
			self.current_LES_since_last_update.set_calculator(lj)
			e = self.current_LES_since_last_update.get_potential_energy()
			rawcomp = self.current_LES_since_last_update.get_chemical_symbols()
			comp = {}
			for element in rawcomp:
				if element in comp:
					comp[element] += 1
				else:
					comp[element] = 1
			self.current_LES_since_last_update = Cluster(composition = comp, 
														relaxed_positions = self.current_LES_since_last_update.get_positions(), 
														cell = self.current_LES_since_last_update.get_cell(),
														BH_energy = e,
														atoms = self.current_LES_since_last_update)
			f.readline() #skip next line (the header for start of CNA profile)
			line = f.readline()
			while line.strip() != "end CNA profiles of current_LES_since_last_update":
				cna = Counter()
				sigs = []
				abundances = []
				data = line.strip().split(';')[:-1]
				for row in data:
					sig = row.split(':')[0].split(',')
					for i in range(len(sig)):
						sig[i] = int(sig[i])
					sigs.append(tuple(sig))
					abundances.append(int(row.split(':')[1]))
				for s,a in zip(sigs, abundances):
					cna[s] = a
				self.current_LES_since_last_update.CNA_profile = [cna]
				line = f.readline()

		self.reseed_triggered_last_hop = f.readline().split(':')[1].strip() == "True"
		

	def check_population_controller_information(self):
		missing_keys = None
		for key in ['reseed_operator_pointer']:
			if not key in self.population_controller_information:
				if missing_keys != None:
					missing_keys += ', '
					missing_keys += key
				else:
					missing_keys = key 
		if missing_keys != None:
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'The following parameter(s) are missing from the \n'
			error_msg += 'population_controller_information variable.\n'
			error_msg += missing_keys + '.\n'
			error_msg += 'These parameter(s) are required for the Energy Plus SCM\n'
			error_msg += 'Search Strategy.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()


		if self.population_controller_information['reseed_operator_pointer'].reseed_operator_information['reseed_operator'] == 'none':
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'the Reseed_Population_Controller requires a Reseed Operator\n'
			error_msg += 'other than the None_Reseed_Operator.\n'
			error_msg += 'Please check this parameter and try running the\n'
			error_msg += 'algorithm again.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()

	def print_population_controller_information(self):
		"""
		Prints information about the search strategy.
		"""
		to_print = ''
		to_print += '\nPopulation Controller Name: ' + self.population_controller_information['population_controller']
		print(to_print)