def get_deformation_method(deformation_method_information):
	"""
	This function retrieved the deformation method to be used by the BHA.

	:param deformation_method_information: Information about the deformation method.
	:type  deformation_method_information: dict.

	:returns The deformation method subclass.
	:rtype Subclass of BHA.Deformation_Methods.Deformation_Method
	"""

	method = deformation_method_information['method']

	if method == 'cartesian':
		from BHA.Deformation_Methods.Cartesian_Displacement_Deformation_Method import Cartesian_Displacement_Deformation_Method
		return Cartesian_Displacement_Deformation_Method(deformation_method_information)

	elif method == 'geometric_center':
		from BHA.Deformation_Methods.Geometric_Center_Displacement_Deformation_Method import Geometric_Center_Displacement_Deformation_Method
		return Geometric_Center_Displacement_Deformation_Method(deformation_method_information)

	elif method == 'angular':
		from BHA.Deformation_Methods.Angular_Deformation_Method import Angular_Deformation_Method
		return Angular_Deformation_Method(deformation_method_information)