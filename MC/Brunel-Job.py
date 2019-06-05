from Gaudi.Configuration import *
from Configurables import Brunel, LHCbApp, L0Conf

LHCbApp().DDDBtag = "dddb-20170721-3"
LHCbApp().CondDBtag = "sim-20170721-2-vc-md100"

Brunel().DatasetName = '13102601-5ev-20190605'
Brunel().Simulation = True
Brunel().OutputType='XDST'

L0Conf().EnsureKnownTCK=False

#following lines necessary for local running! need to be omitted for batch mode 
from GaudiConf import IOExtension                                 
IOExtension().inputFiles(['13102601-5ev-20190605_wHLT2.xdigi'],clear=True)
FileCatalog().Catalogs = [ "xmlcatalog_file:NewCatalog.xml" ] # local test

# from production request 48724
importOptions("$APPCONFIGOPTS/Brunel/DataType-2016.py")
importOptions("$APPCONFIGOPTS/Brunel/MC-WithTruth.py")
importOptions("$APPCONFIGOPTS/Brunel/SplitRawEventOutput.4.3.py")
importOptions("$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py")
