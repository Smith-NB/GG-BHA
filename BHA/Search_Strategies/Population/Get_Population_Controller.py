def get_population_controller(population_controller_information):
	"""
	This function retrieves the population controller to be used by the BHA.

	:param search_strategy_information: Information about the population controller
	:type  search_strategy_information: dict
	"""

	controller_name = population_controller_information['population_controller']

	if controller_name == 'periodic':
		from BHA.Search_Strategies.Population.Periodic_Population_Controller import Periodic_Population_Controller
		return Periodic_Population_Controller(population_controller_information)

	elif controller_name == 'static':
		from BHA.Search_Strategies.Population.Static_Population_Controller import Static_Population_Controller
		return Static_Population_Controller(population_controller_information)
		
	elif controller_name == 'reseed':
		from BHA.Search_Strategies.Population.Reseed_Population_Controller import Reseed_Population_Controller
		return Reseed_Population_Controller(population_controller_information)

		"""
		elif controller_name == 'LES':
			from BHA.Search_Strategies.Population.LES_Population_Controller import LES_Population_Controller
			return LES_Population_Controller(population_controller_information)
		"""
	else:
		valid_names = ['periodic', 'static', 'reseed']#, 'LES']
		error_msg = '\n'
		error_msg += '--------------------------------------------------------'+'\n'
		error_msg += 'The population controller name you have defined is invalid.\n'
		error_msg += 'The following names are valid to use as the \'population_controller\' parameter.\n'
		error_msg += valid_names[0]
		for name in valid_names[1:]:
			error_msg += ', ' + name
		error_msg += '\nThe basin hopping algorithm will exit without starting.\n'
		error_msg += '--------------------------------------------------------'+'\n'
		print(error_msg)
		from BHA.Lock import lock_remove
		lock_remove()
		exit()