import numpy as np

def exponential_function(alpha, sim):
	return np.exp(-1 * alpha * sim)

def neg_exponential_function(alpha, sim):
	beta = np.log((1/(np.power(10, -1 * alpha))) + 1)
	return (1 - np.exp(beta * sim)) * np.power(10, -1 * alpha) + 1

def neg_tangent(alpha, sim):
	beta =  np.arctan(1/alpha)
	return 1 - alpha * np.tan(beta * sim)

def linear_function(alpha, sim):
	prob = alpha - alpha * sim
	if prob > 1:
		return 1
	else:
		return prob

def pass_function(alpha, sim):
	return sim

def get_sim_function(function):
	if function == 'exponential':
		return exponential_function
	elif function == 'neg_exponential':
		return neg_exponential_function
	elif function == 'neg_tangent':
		return neg_tangent
	elif function == 'linear':
		return linear_function
	elif function == 'pass':
		return pass_function
