def additive_function(c_E, f_E_value, c_SCM, f_SCM_value):
	E_cont = c_E * f_E_value
	SCM_cont = c_SCM * f_SCM_value
	print("E_cont = " + str(E_cont))
	print("SCM_cont = " + str(SCM_cont))

	value = E_cont + SCM_cont
	print("Chance to accept = " + str(value))
	return value

def subtractive_function(c_E, f_E_value, c_SCM, f_SCM_value):
	E_cont = c_E * f_E_value
	SCM_cont = c_SCM * f_SCM_value
	print("E_cont = " + str(E_cont))
	print("SCM_cont = " + str(SCM_cont))

	value = E_cont - SCM_cont
	if value < 0:
		value = 0
	print("Chance to accept = " + str(value))
	return value

def get_prob_function(function):
	if function == 'additive':
		return additive_function
	elif function == 'subtractive':
		return subtractive_function
