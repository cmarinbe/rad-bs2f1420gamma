from Gaudi.Configuration import importOptions
from Configurables import LHCbApp

LHCbApp().DDDBtag = "dddb-20170721-3"
LHCbApp().CondDBtag = "sim-20170721-2-vc-md100"

#following lines necessary for local running! need to be omitted for batch mode 
from GaudiConf import IOExtension                                 
IOExtension().inputFiles(['13102601-5ev-20190605.xdst'],clear=True)
#FileCatalog().Catalogs = [ "xmlcatalog_file:NewCatalog.xml" ] # local test

# from production request 48724
importOptions("$APPCONFIGOPTS/DaVinci/DV-Stripping28r1p1-Stripping-MC-NoPrescaling-DST.py")
importOptions("$APPCONFIGOPTS/DaVinci/DataType-2016.py")
importOptions("$APPCONFIGOPTS/DaVinci/InputType-DST.py")
