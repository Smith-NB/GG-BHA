def get_search_strategy(search_strategy_information):
	"""
	This function retrieves the search strategy to be used by the BHA.

	:param search_strategy_information: Information about the search strategy
	:type  search_strategy_information: dict
	"""
	strategy_name = search_strategy_information['search_strategy']

	if strategy_name == 'energy':
		from BHA.Search_Strategies.Energy_Search_Strategy import Energy_Search_Strategy

		return Energy_Search_Strategy(search_strategy_information)

	elif strategy_name == 'energy_plus_SCM':
		from BHA.Search_Strategies.Energy_Plus_SCM_Search_Strategy import Energy_Plus_SCM_Search_Strategy
		return Energy_Plus_SCM_Search_Strategy(search_strategy_information)

	elif strategy_name == 'energy_plus_population_SCM':
		from BHA.Search_Strategies.Energy_Plus_Population_SCM_Search_Strategy import Energy_Plus_Population_SCM_Search_Strategy
		return Energy_Plus_Population_SCM_Search_Strategy(search_strategy_information)

	elif strategy_name == 'energy_minus_penalty':
		from BHA.Search_Strategies.Energy_Minus_Penalty_Search_Strategy import Energy_Minus_Penalty_Search_Strategy
		return Energy_Minus_Penalty_Search_Strategy(search_strategy_information)

	elif strategy_name == 'energy_and_forbidden_hops':
		from BHA.Search_Strategies.Energy_And_Forbidden_Hops_Search_Strategy import Energy_And_Forbidden_Hops_Search_Strategy
		return Energy_And_Forbidden_Hops_Search_Strategy(search_strategy_information)


	else:
		valid_names = ['energy', 'energy_plus_SCM', 'energy_plus_population_SCM', 'energy_minus_penalty', 'energy_and_forbidden_hops']
		error_msg = '\n'
		error_msg += '--------------------------------------------------------'+'\n'
		error_msg += 'The search strategy name you have defined is invalid.\n'
		error_msg += 'The following names are valid to use as the \'search_stragegy\' parameter.\n'
		error_msg += valid_names[0]
		for name in valid_names[1:]:
			error_msg += ', ' + name
		error_msg += '\nThe basin hopping algorithm will exit without starting.\n'
		error_msg += '--------------------------------------------------------'+'\n'
		print(error_msg)
		from BHA.Lock import lock_remove
		lock_remove()
		exit()