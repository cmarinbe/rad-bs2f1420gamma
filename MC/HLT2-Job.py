from Gaudi.Configuration import *

from Moore.Configuration import Moore
Moore().DDDBtag   = "dddb-20170721-3"
Moore().CondDBtag = "sim-20170721-2-vc-md100"

#for local running
from GaudiConf import IOExtension
IOExtension().inputFiles(['13102601-5ev-20190605_wHLT1.xdigi'],clear=True)
Moore().outputFile = '13102601-5ev-20190605_wHLT2.xdigi'

importOptions("$APPCONFIGOPTS/Moore/MooreSimProductionForSeparateL0AppStep2015.py")
importOptions("$APPCONFIGOPTS/Conditions/TCK-0x6139160F.py")
importOptions("$APPCONFIGOPTS/Moore/DataType-2016.py")
importOptions("$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py")
importOptions("$APPCONFIGOPTS/Moore/MooreSimProductionHlt2.py")
