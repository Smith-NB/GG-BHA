from BHA.Search_Strategies.Population.Population_Controller import Population_Controller
from ase.io import Trajectory
class Periodic_Population_Controller(Population_Controller):
	"""
	The Periodic Population Controller updates the population after a specified period. 
	A cluster maturity age can also be specified, where clusters will only be added to the
	population after they reach a certain age (measured in number of attempted hops).
	"""

	def __init__(self, population_controller_information):
		super().__init__(population_controller_information)
		self.period = self.population_controller_information['period']
		self.maturity_age = self.population_controller_information['maturity_age']

		self.premature_clusters = []
		self.premature_cluster_ages = []
		self.current_period = self.period
		self.current_LES_since_last_update = None

	def time_to_update(self, cluster):
		"""
		Checks if any clusters in the premature_clusters list have matured.
		Also checks if its time to append the latest LES to the premature_cluster list.
		"""
		#set update flag to false
		update = False
		#age all clusters and set update flag to true if any have matured.
		for i in range(len(self.premature_clusters)):
			self.premature_cluster_ages[i] += 1
			if self.premature_cluster_ages[i] >= self.maturity_age:
				update = True

		#Check if a new LES has been found since the last update to the population
		if self.current_LES_since_last_update is None or cluster.BH_energy < self.current_LES_since_last_update.BH_energy:
			self.current_LES_since_last_update = cluster


		#If a period has passed, add the latest LES CNA profile 
		#to the premature cluster list for aging, and set the LES to None.
		self.current_period -= 1
		if self.current_period <= 0:
			self.current_period = self.period
			self.premature_clusters.append(self.current_LES_since_last_update)
			self.current_LES_since_last_update = None
			self.premature_cluster_ages.append(0)
		return update

	def get_cluster_to_append(self):
		"""
		Retrieves the matured cluster to be added to the population.
		Should be the cluster at index 0 if self.premature_clusters

		returns: CNA profile of the cluster to append.
		rtype: Counter
		"""

		self.premature_cluster_ages.pop(0) #remove the age of the matured cluster (will be at index 0)
		return self.premature_clusters.pop(0) #remove and return the matured cluster CNA

	def log_population_controller_resumption_info(self):
		f = open("information_for_resuming.txt", "a")
		f.write('\nInformation for Periodic_Population_Controller\n')
		f.write('begin CNA profiles of premature_clusters\n')
		if self.current_LES_since_last_update is not None:
			self.premature_clusters.append(self.current_LES_since_last_update)
		for c in self.premature_clusters:
			for sig in c.CNA_profile[0]:
				f.write(str(sig).replace(' ', '').replace('(', '').replace(')', '') + ':')
				f.write(str(c.CNA_profile[0][sig]) + ';')
			f.write('\n')
		f.write("end CNA profiles of premature_clusters")		

		f.write("\npremature_cluster_ages: %s" % str(self.premature_cluster_ages))
		f.write("\ncurrent_period: %d" % self.current_period)
		if self.current_LES_since_last_update is not None:
			f.write("\nthe final cluster in population_history.traj is the current_LES_since_last_update and will be removed upon resumption")
		else:
			f.write("\nthere is no current_LES_since_last_update")
		f.write("\nthe final %d cluster(s) (before current_LES_since_last_update if present) in population_history.traj are premature and will be removed upon resumption" % len(self.premature_clusters))
		f.flush()
		f.close()

		traj = Trajectory("population_history.traj", "a")
		for cluster in self.premature_clusters:
			print("premature cluster written to traj")
			traj.write(cluster.atoms)
		traj.close()

	def retrieve_resumption_info(self):
		from collections import Counter
		from ase.io import Trajectory
		from BHA.BH_Cluster import Cluster
		from BHA.Get_Starting_Structure import get_calculator
		import shutil

		f = open("information_for_resuming.txt", "r")
		for i in range(5): f.readline() #skip first 5 lines
		line = f.readline() 
		if not line.startswith("Information for") or not line.strip().endswith("Periodic_Population_Controller"): #check population controller is correct
			print("Failed to resume properly; population controller mismatch")
			from BHA.Lock import lock_remove
			lock_remove()
			exit()

		f.readline() #skip next line

		#import premature CNA profiles
		logged_CNA_profiles = []
		line = f.readline()
		while line.strip() != "end CNA profiles of premature_clusters":
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
			logged_CNA_profiles.append([cna])
			line = f.readline()

		#import premature cluster ages
		line = f.readline()
		print(line)
		line = line.split('[')[1].replace(']','').strip()
		if ',' in line:
			line = line.split(',')
			for age in line:
				self.premature_cluster_ages.append(int(line.strip()))
		else:
			self.premature_cluster_ages.append(int(line.strip()))

		#import current period
		self.current_period = int(f.readline().split(':')[1].strip())

		pop_hist_traj = Trajectory("population_history.traj", "r")
		new_traj = Trajectory("temp.traj", "w")

		#get premature clusters and current_LES_since_last_update cluster ase.Atoms objects from traj.
		for i in range(len(pop_hist_traj)-len(logged_CNA_profiles)):
			new_traj.write(pop_hist_traj[i])

		for i in range(len(pop_hist_traj)-len(logged_CNA_profiles), len(pop_hist_traj)-1):
			self.premature_clusters.append(pop_hist_traj[i])

		if f.readline().strip() == "there is no current_LES_since_last_update":
			self.current_LES_since_last_update = None
			self.premature_clusters.append(pop_hist_traj[-1])
		else:
			self.current_LES_since_last_update = pop_hist_traj[-1]

		#create BHA.BH_Cluster Objects for premature clusters
		lj = get_calculator()
		for i in range(len(self.premature_clusters)):
			self.premature_clusters[i].set_calculator(lj)
			e = self.premature_clusters[i].get_potential_energy()
			rawcomp = self.premature_clusters[i].get_chemical_symbols()
			comp = {}
			for element in rawcomp:
				if element in comp:
					comp[element] += 1
				else:
					comp[element] = 1
			self.premature_clusters[i] = Cluster(composition = comp, 
												relaxed_positions = self.premature_clusters[i].get_positions(), 
												cell = self.premature_clusters[i].get_cell(),
												BH_energy = e,
												atoms = self.premature_clusters[i],
												CNA_profile = logged_CNA_profiles[i])

		#create BHA.Cluster Objects for current_LES_since_last_update
		if self.current_LES_since_last_update is not None:	
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
														atoms = self.current_LES_since_last_update,
														CNA_profile = logged_CNA_profiles[-1])

		pop_hist_traj.close()
		new_traj.close()
		shutil.move("temp.traj", "population_history.traj")
		f.close()

	def check_population_controller_information(self):
		missing_keys = None
		for key in ['period', 'maturity_age']:
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
			error_msg += 'search_strategy_information variable.\n'
			error_msg += missing_keys + '.\n'
			error_msg += 'These parameter(s) are required for the Energy Plus SCM\n'
			error_msg += 'Search Strategy.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()

		for key in ['period', 'maturity_age']:
			if not isinstance(self.population_controller_information[key], int):
				error_msg = '\n'
				error_msg += '--------------------------------------------------------\n'
				error_msg += 'the period and maturity_age parameters must be an int\n'
				error_msg += 'data type.\n'
				error_msg += 'Please check these parameters and try running the\n'
				error_msg += 'algorithm again.\n\n'
				error_msg += 'The basin hopping algorithm will exit without starting.\n'
				error_msg += '--------------------------------------------------------\n'
				print(error_msg)
				from BHA.Lock import lock_remove
				lock_remove()
				exit()

			if self.population_controller_information[key] < 1:
				error_msg = '\n'
				error_msg += '--------------------------------------------------------\n'
				error_msg += 'the period and maturity_age parameters must have values\n'
				error_msg += 'greater than 0.\n'
				error_msg += 'Please check these parameters and try running the\n'
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
		to_print += '\nPeriod: ' + str(self.population_controller_information['period'])
		to_print += '\nMaturity Age: ' + str(self.population_controller_information['maturity_age'])
		print(to_print)