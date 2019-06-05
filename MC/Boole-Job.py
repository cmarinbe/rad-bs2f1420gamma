from Gaudi.Configuration import *
from Configurables import Boole, LHCbApp

#-- File catalogs 
FileCatalog().Catalogs = [ "xmlcatalog_file:NewCatalog.xml" ] # local test

#-- Event input

LHCbApp().DDDBtag   = "dddb-20170721-3"
LHCbApp().CondDBtag = "sim-20170721-2-vc-md100"

Boole().DatasetName = "13102601-5ev-20190605"

# the following line necessary for local running, but prevents from working for running in batch mode
EventSelector().Input = [ 'Gauss-13102601-5ev-20190605.sim' ] # local test

OutputStream("DigiWriter").Output = "DATAFILE='PFN:13102601-5ev-20190605.xdigi' TYP='POOL_ROOTTREE' OPT='REC'"
OutputStream("DigiWriter").OptItemList += [ '/Event/Gen/HepMCEvents#1' ]

# from production request 48724
importOptions("$APPCONFIGOPTS/Boole/Default.py")
importOptions("$APPCONFIGOPTS/Boole/EnableSpillover.py")
importOptions("$APPCONFIGOPTS/Boole/DataType-2015.py")
importOptions("$APPCONFIGOPTS/Boole/Boole-SetOdinRndTrigger.py")
#importOptions("$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py")
