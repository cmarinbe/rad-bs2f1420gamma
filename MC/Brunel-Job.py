from Gaudi.Configuration import *
from Configurables import Brunel, LHCbApp, L0Conf

LHCbApp().DDDBtag = "dddb-20170721-3"
LHCbApp().CondDBtag = "sim-20170721-2-vc-md100"

# from production request 48724
importOptions("$APPCONFIGOPTS/Brunel/DataType-2016.py")
importOptions("$APPCONFIGOPTS/Brunel/MC-WithTruth.py")
importOptions("$APPCONFIGOPTS/Brunel/SplitRawEventOutput.4.3.py")
importOptions("$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py")
