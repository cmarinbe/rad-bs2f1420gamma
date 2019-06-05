from Gaudi.Configuration import *

from L0App.Configuration import L0App

FileCatalog().Catalogs = [ "xmlcatalog_file:NewCatalog.xml" ] # local test

#for local running
from GaudiConf import IOExtension
IOExtension().inputFiles(['Boole.digi'],clear=True)

