from Gaudi.Configuration import *
from Configurables import Boole, LHCbApp

#-- Event input

LHCbApp().DDDBtag   = "dddb-20170721-3"
LHCbApp().CondDBtag = "sim-20170721-2-vc-md100"

# from production request 48724
importOptions("$APPCONFIGOPTS/Boole/Default.py")
importOptions("$APPCONFIGOPTS/Boole/EnableSpillover.py")
importOptions("$APPCONFIGOPTS/Boole/DataType-2015.py")
importOptions("$APPCONFIGOPTS/Boole/Boole-SetOdinRndTrigger.py")
