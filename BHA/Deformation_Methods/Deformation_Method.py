from abc import ABC, abstractmethod

class Deformation_Method(ABC):

	def __init__(self, deformation_method_information):
		self.deformation_method_information = deformation_method_information
		self.check_deformation_method_information()
		self.print_deformation_method_information()

	def __repr__(self):
		return str(self.__dict__)

	@abstractmethod
	def get_deformed_coordinates(self, atoms):

		pass

	@abstractmethod
	def check_deformation_method_information(self):

		pass

	@abstractmethod
	def print_deformation_method_information(self):

		pass

	def distance_between_points(p1, p2):
		'''
		Calculates distance between two points in 3D space.

		:param p1: Cartesian coordinates of point 1.
		:type p1: iterable of three ints or floats.
		:param p2: Cartesian coordinates of point 2.
		:type p2: iterable of three ints or floats.

		:returns The distance between the two points
		:rtype float
		'''
		xdiff = p1[0] - p2[0]
		ydiff = p1[1] - p2[1]
		zdiff = p1[2] - p2[2]
		dist = np.sqrt(xdiff**2 + ydiff**2 + zdiff**2)
		return dist

	def convert_spherical_to_cartesian(r, theta, phi):
		'''
		Takes spherical coordinates (3D polar coordinates) and converts it to cartesian coordinates

		:param r: distance from origin.
		:type r: int or float.
		:param theta: azimuthal angle from the z axis to the x, y plane, in degrees
		:type theta: int or float.
		:param phi: polar angle along x, y plane, in degrees
		:type phi: int or float.

		:returns The cartesian coordinates.
		:rtypes list of three floats.
		'''
		deg_to_rad = np.pi/180
		x = float(r * np.sin(phi * deg_to_rad) * np.cos(theta * deg_to_rad))
		y = float(r * np.sin(phi * deg_to_rad) * np.sin(theta * deg_to_rad))
		z = float(r * np.cos(phi * deg_to_rad))

		return [x, y, z]
