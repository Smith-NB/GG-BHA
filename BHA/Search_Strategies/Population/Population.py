from BHA.T_SCM_Methods import get_CNA_profile, get_CNA_similarity
from BHA.Search_Strategies.Population.Get_Population_Controller import get_population_controller
from ase.io import Trajectory
from ase import Atoms
class Population():

	def __init__(self, population_information):
		self.population_information = population_information
		self.check_population_information()

		self.size = population_information["size"]
		self.similarity_mode = population_information["similarity_mode"]
		self.similarity_of_cluster = self.get_similarity_calculation_method()
		self.controller = get_population_controller(population_information["population_controller_information"])
		self.r_Cut = population_information['r_Cut']
		self.cna_list = []
		self.cna_list_length = 0
		self.population_traj = Trajectory("population_history.traj", "a")
		if len(self.population_traj) != 0:
			self.population_traj.close() #close traj file to avoid simultaneous edit errors
			self.controller.retrieve_resumption_info() #have the controller resume from logged info (editing traj file in the process)
			self.population_traj = Trajectory("population_history.traj", "r") #reopen the new traj file
			for i in range(-self.size if self.size <= len(self.population_traj) else -len(self.population_traj), 0): #add the stored structure CNAs to the population (upto the population size)
				self.cna_list.append(get_CNA_profile((self.population_traj[i], [self.r_Cut])))
			self.cna_list_length = len(self.cna_list)
			self.population_traj.close()
			self.population_traj = Trajectory("population_history.traj", "a")

	def update(self, cluster):
		if self.controller.time_to_update(cluster):
			self.add_cluster(self.controller.get_cluster_to_append())

	def add_cluster(self, cluster):
		#add cna profile to the list
		self.cna_list.append(cluster.CNA_profile)
		self.population_traj.write(cluster.atoms)
		print(str(cluster.UID) + " added to pop")
		print(self.cna_list_length)
		#if population is oversized, remove oldest cluster.
		if self.cna_list_length >= self.size:
			self.cna_list.pop(0)
		else:
			self.cna_list_length += 1

	def get_max_similarity_to_population(self, cluster_cna):
		if len(self.cna_list) == 0:
			return None
		sigma = 0
		

		for cna in self.cna_list:
			s = get_CNA_similarity(cluster_cna, cna)
			print("test %f" % s)
			if s > sigma:
				sigma = s

		return sigma

	def get_avg_similarity_to_population(self, cluster_cna):
		if len(self.cna_list) == 0:
			return None
		sigma = 0

		for cna in self.cna_list:
			sigma += get_CNA_similarity(cluster_cna, cna)

		sigma /= self.cna_list_length
		return sigma

	def get_similarity_calculation_method(self):
		if self.similarity_mode == 'max':
			return self.get_max_similarity_to_population
		elif self.similarity_mode == 'avg':
			return self.get_avg_similarity_to_population


	def check_population_information(self):
		missing_keys = None
		for key in ['population_controller_information', 'size', 'similarity_mode']:
			if not key in self.population_information:
				if missing_keys != None:
					missing_keys += ', '
					missing_keys += key
				else:
					missing_keys = key 

		if missing_keys != None:
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'The following parameter(s) are missing from the \n'
			error_msg += 'population_information variable.\n'
			error_msg += missing_keys + '.\n'
			error_msg += 'These parameter(s) are required for the Population \n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()

		if not isinstance(self.population_information['size'], int):
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'the size parameters must be an int data type\n'
			error_msg += 'Please check this parameters and try running the\n'
			error_msg += 'algorithm again.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()

		if self.population_information['size'] < 1:
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'the size parameter must have values greater than 0.\n'
			error_msg += 'Please check these parameters and try running the\n'
			error_msg += 'algorithm again.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()

		if self.population_information['similarity_mode'] not in ['max', 'avg']:
			error_msg = '\n'
			error_msg += '--------------------------------------------------------\n'
			error_msg += 'The similarity_mode parameter must be one of the following: \n'
			error_msg += '\tmax, avg'
			error_msg += 'Please correct this parameter and try again.\n\n'
			error_msg += 'The basin hopping algorithm will exit without starting.\n'
			error_msg += '--------------------------------------------------------\n'
			print(error_msg)
			from BHA.Lock import lock_remove
			lock_remove()
			exit()
