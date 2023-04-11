
# The information about the Organisms program

__name__    = 'Garden Group Basin Hopping Algorithm'
__version__ = '1.1.5.2'
__author__  = 'Nicholas Smith and Dr. Anna Garden'

import sys
if sys.version_info[0] == 2:
	toString  = '================================================'+'\n'
	toString += 'This is the Garden Group Basin Hopping Algorithm'+'\n'
	toString += 'Version: '+str(__version__)+'\n'
	toString += '\n'
	toString += 'The  program requires Python3. You are attempting to execute this program in Python2.'+'\n'
	toString += 'Make sure you are running the  program in Python3 and try again'+'\n'
	toString += 'This program will exit before beginning'+'\n'
	toString += '================================================'+'\n'
	raise ImportError(toString)

__author_email__ = 'smini250@student.otago.ac.nz'
__license__ = 'None'
__url__ = 'to be added'
__doc__ = 'to be added'

from BHA.BH_Program import BasinHopping
#from Organisms.Subsidiary_Programs.MakeTrialsProgram import MakeTrialsProgram
#from Organisms.Postprocessing_Programs.make_energy_vs_similarity_results import make_energy_vs_similarity_results
#from Organisms.Subsidiary_Programs.GetNewlyInitilisedPopulation import GetNewlyInitilisedPopulation
__all__ = ['GA_Program','MakeTrialsProgram','make_energy_vs_similarity_results'] # 'GetNewlyInitilisedPopulation']