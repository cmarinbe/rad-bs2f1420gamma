from Gaudi.Configuration import *

from L0App.Configuration import L0App

L0App().DDDBtag   = "dddb-20170721-3"
L0App().CondDBtag = "sim-20170721-2-vc-md100"

L0App().outputFile = '13102601-L0App.digi'

# from production request 48724
importOptions( "$APPCONFIGOPTS/L0App/L0AppSimProduction.py" )
importOptions("$APPCONFIGOPTS/L0App/L0AppTCK-0x160F.py")
importOptions("$APPCONFIGOPTS/L0App/ForceLUTVersionV8.py")
importOptions( "$APPCONFIGOPTS/L0App/DataType-2016.py" )
importOptions( "$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py" )
