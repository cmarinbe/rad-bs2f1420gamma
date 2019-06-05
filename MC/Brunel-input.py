#following lines necessary for local running! need to be omitted for batch mode 
from GaudiConf import IOExtension
from Gaudi.Configuration import FileCatalog

IOExtension().inputFiles(['13102601-HLT2.digi'],clear=True)
FileCatalog().Catalogs = [ "xmlcatalog_file:NewCatalog.xml" ] # local test
