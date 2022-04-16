
def get_reseed_operator(reseed_operator_information):
	"""
	This function retrieves the search strategy to be used by the BHA.

	:param search_strategy_information: Information about the search strategy
	:type  search_strategy_information: dict
	"""
	operator_name = reseed_operator_information['reseed_operator']

	if operator_name == 'none':
		from BHA.Reseed_Operators.None_Reseed_Operator import None_Reseed_Operator
		return None_Reseed_Operator(reseed_operator_information, None, None)

	elif operator_name == 'new_LES':
		from BHA.Reseed_Operators.New_LES_Reseed_Operator import New_LES_Reseed_Operator
		return New_LES_Reseed_Operator(reseed_operator_information, None, None)

	elif operator_name == 'new_LES_or_blacklist':
		from BHA.Reseed_Operators.New_LES_Or_Blacklist_Reseed_Operator import New_LES_Or_Blacklist_Reseed_Operator
		return New_LES_Or_Blacklist_Reseed_Operator(reseed_operator_information, None, None)

	elif operator_name == 'new_LES_or_blacklist_alt':
		from BHA.Reseed_Operators.New_LES_Or_Blacklist_Reseed_Operator_Alt import New_LES_Or_Blacklist_Reseed_Operator_Alt
		return New_LES_Or_Blacklist_Reseed_Operator_Alt(reseed_operator_information, None, None)

	elif operator_name == 'energy_lowered':
		from BHA.Reseed_Operators.Energy_Lowered_Reseed_Operator import Energy_Lowered_Reseed_Operator
		return Energy_Lowered_Reseed_Operator(reseed_operator_information, None, None)

	else:
		valid_names = ['none', 'new_LES', 'new_LES_or_blacklist', 'energy_lowered']
		error_msg = '\n'
		error_msg += '--------------------------------------------------------'+'\n'
		error_msg += 'The reseed operator name you have defined is invalid.\n'
		error_msg += 'The following names are valid to use as the \'reseed_operator\' parameter.\n'
		error_msg += valid_names[0]
		for name in valid_names[1:]:
			error_msg += ', ' + name
		error_msg += '\nThe basin hopping algorithm will exit without starting.\n'
		error_msg += '--------------------------------------------------------'+'\n'
		print(error_msg)
		from BHA.Lock import lock_remove
		lock_remove()
		exit()