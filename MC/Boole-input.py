# Local test options

from Gaudi.Configuration import *
from Configurables import Boole

#-- File catalogs 
FileCatalog().Catalogs = [ "xmlcatalog_file:NewCatalog.xml" ] # local test

# input file from previous step
EventSelector().Input = [ 'Gauss-13102601-5ev-20190605.sim' ] # local test
