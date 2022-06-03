from BHA.Types_Of_Mutations import randomMutate
from BHA.ExternalDefinitions import Exploded
from asap3.Internal.BuiltinPotentials import LennardJones, RGL
def get_starting_structure(cluster_makeup, trajectory):
	from os import path
	if trajectory is not None and path.exists(trajectory):
		return get_latest_structure(trajectory)
	else:
		return generate_random_structure(cluster_makeup)

	
def generate_random_structure(cluster_makeup, boxtoplaceinlength, vacuumAdd):
	"""
	Generate a new random cluster structure

	:param boxtoplaceinlength: This is the length of the box you would like to place atoms in to make a randomly constructed cluster.
	:type  boxtoplaceinlength: float
	:param vacuumAdd: The length of vacuum added around the cluster. Written in A.
	:type  vacuumAdd: float
	:param cluster_makeup: check this
	:type  cluster_makeup: {'Element': int(number of that 'element' in this cluster),...}
	"""
	while True:
		cluster = randomMutate(
							boxtoplaceinlength = boxtoplaceinlength,
							vacuumAdd = vacuumAdd,
							cluster_makeup = cluster_makeup,
							cluster_to_mutate = None, 
							percentage_of_cluster_to_randomise = None
							)
		if Exploded(cluster,max_distance_between_atoms=1.5): # make sure the randomised cluster has not split up when optimised.
			print("Cluster exploded. Will obtain a new cluster.")
			continue # Since the cluster has exploded, we throw it out and repeat the process by making a new randomised cluster 
		else:
			break
	return cluster

def get_latest_structure(trajectory):
	"""
	Retrieves the latest structure in a Trajectory (.traj) file.

	:param trajectory: The Trajectory file to read.
	:type  trajectory: Trajectory.
	"""
	from ase.io import read
	cluster = read(trajectory, -1, 'traj')
	return cluster

def get_calculator(calculator_information):
	"""
	Retrieves the calculator to be used by the ase.atoms object.
	Currently this just retrieved the LJ calculator, will introduce Gupta calculator later.
	"""
	if calculator_information['potential'] in ['LennardJones_ReducedUnits', 'LJRR', 'ljrr']:
		elements = [10]; sigma = [1]; epsilon = [1]; rCut = 1000;
		return LennardJones(elements, epsilon, sigma, rCut=rCut, modified=True)
	elif calculator_information['potential'] in ['LJ', 'lj', 'LennardJones', 'lennardjones']:
		return LennardJones(**calculator_information['params'])
	elif calculator_information['potential'] in ['RGL_Au', 'rgl_Au', 'Gupta_Au', 'gupta_Au']:
		#p, q, a, xi, r0, cutoff=sqrt(r0)
		return RGL({'Au': [10.53, 4.30, 0.2197, 1.855, 2.88]}, cutoff=2.88 * 2**0.5, debug=True)
	elif calculator_information['potential'] in ['RGL_Au_nc', 'rgl_Au_nc', 'Gupta_Au_nc', 'gupta_Au_nc']:
		#p, q, a, xi, r0, cutoff=sqrt(r0)
		return RGL({'Au': [10.53, 4.30, 0.2197, 1.855, 2.88]}, cutoff=1000, debug=True)
	elif calculator_information['potential'] in ['RGL', 'rgl', 'Gupta', 'gupta']:
		return RGL(**calculator_information['params'])

	"""
	elements = [10]; sigma = [1]; epsilon = [1]; rCut = 1000;
	lj_calc = LennardJones(elements, epsilon, sigma, rCut=rCut, modified=True)
	return lj_calc
	"""