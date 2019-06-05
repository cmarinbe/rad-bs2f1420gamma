from Gaudi.Configuration import *

from Moore.Configuration import Moore
Moore().DDDBtag = "dddb-20170721-3"
Moore().CondDBtag = "sim-20170721-2-vc-md100"

#for local running
Moore().outputFile = '13102601-HLT1.digi'

# from production request 48724
importOptions("$APPCONFIGOPTS/Moore/MooreSimProductionForSeparateL0AppStep2015.py")
importOptions("$APPCONFIGOPTS/Conditions/TCK-0x5138160F.py")
importOptions("$APPCONFIGOPTS/Moore/DataType-2016.py" )
importOptions("$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py" )
importOptions("$APPCONFIGOPTS/Moore/MooreSimProductionHlt1.py")
