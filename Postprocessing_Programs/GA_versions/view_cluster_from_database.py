#!/opt/nesi/mahuika/Python/3.6.3-gimkl-2017a/bin/python

import sys
from ase.io import read
from ase.visualize import view

id_name = sys.argv[1]

database_system_name = 'GA_Recording_Database.db'

system = read(database_system_name+'@id='+str(id_name))
if len(system) > 1:
	exit('Error')
system = system[0]
view(system)