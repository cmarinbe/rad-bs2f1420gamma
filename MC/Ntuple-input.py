from GaudiConf import IOHelper

# Use the local input data
IOHelper().inputFiles([
    './test-100ev/000000.AllStreams.dst'
], clear=True)
