import os

"""Macro that should launch a train on ganga
with Gauss / Boole / Moore / Brunel

"""

# =============================================================================
#  Settings variables
# =============================================================================


# -- software version
Gauss_version = "v49r10"
Boole_version = "v30r3" #Boole of 2016 data
L0_version = "v25r4" #Moore of 2016 data
HLT_version = "v25r4" #Moore of 2016 data
Brunel_version = "v50r5" #Brunel of 2016 MC
Turbo_version = "v41r4p3" # DaVinci for Turbo 2016
Strip_version = "v41r4p5" # DaVinci for S28r1p1

# -- software option files directory
cmtpath = "/exp/LHCb/marin/cmtuser"

# -- software platform
Gauss_platform = "x86_64-slc6-gcc48-opt"
Boole_platform = "x86_64-slc6-gcc49-opt"
L0_platform = "x86_64-slc6-gcc48-opt"
HLT_platform = "x86_64-slc6-gcc48-opt"
Brunel_platform = "x86_64-slc6-gcc49-opt"
Turbo_platform = "x86_64-slc6-gcc48-opt"
Strip_platform = "x86_64-slc6-gcc49-opt"

# -- Task
test = True
nJobMax = 100
nsubjob = 1000 if not test else 2
evtpersubjob = 500 if not test else 10

# =============================================================================
#  Main part
# =============================================================================

# the task
train = LHCbTask()  # create a task
train.name = 'Bs2f1420Gamma_fullMC'
train.float = nJobMax

# -- Configure Gauss

GaussWagon = LHCbTransform(name='Step 1: Gauss ', backend=Dirac())
GaussApp = GaudiExec()
GaussApp.directory = cmtpath + "/GaussDev_" + Gauss_version
GaussApp.platform = Gauss_platform
GaussApp.options = ["Gauss-Job.py"]
GaussWagon.application = GaussApp

# number of units to create for MC generation (mandatory when using no input file).
GaussWagon.mc_num_units = 1
GaussWagon.splitter = GaussSplitter(numberOfJobs=nsubjob, eventsPerJob=evtpersubjob)
GaussWagon.outputfiles = [
    DiracFile("*.sim"),
    DiracFile("*.root"),
    LocalFile("*.xml")]
train.appendTransform(GaussWagon)

# -- Configure Boole

BooleWagon = LHCbTransform(name='Step 2: Boole ', backend=Dirac())
BooleApp = GaudiExec()
BooleApp.directory = cmtpath + "/BooleDev_" + Boole_version
BooleApp.platform  = Boole_platform
BooleApp.options  = ["Boole-Job.py"]
BooleWagon.application = BooleApp

dataBoole = TaskChainInput(include_file_mask=['\.sim$'], input_trf_id=GaussWagon.getID())
BooleWagon.addInputData(dataBoole)
BooleWagon.outputfiles = [
    DiracFile("*.digi"),
    LocalFile("*.xml")]
#BooleWagon.delete_chain_input = True
train.appendTransform(BooleWagon)

# -- Configure L0
L0Wagon = LHCbTransform(name='Step 3: L0 ', backend=Dirac())
L0App = GaudiExec()
L0App.directory = cmtpath + "/MooreDev_" + L0_version
L0App.platform  = L0_platform
L0App.options  = ["L0-Job.py"]
L0Wagon.application = L0App

dataL0 = TaskChainInput(include_file_mask=['\.digi$'], input_trf_id=BooleWagon.getID())
L0Wagon.addInputData(dataL0)
L0Wagon.outputfiles = [
    DiracFile("*.digi"),
    LocalFile("*.xml")]
L0Wagon.delete_chain_input = True
train.appendTransform(L0Wagon)

# -- Configure HLT1

HLT1Wagon = LHCbTransform(name='Step 4: HLT1 ', backend=Dirac())
HLT1App = GaudiExec()
HLT1App.directory = cmtpath + "/MooreDev_" + HLT_version
HLT1App.platform  = HLT_platform
HLT1App.options  = ["HLT1-Job.py"]
HLT1Wagon.application = HLT1App

dataHLT1 = TaskChainInput(include_file_mask=['\.digi$'], input_trf_id=L0Wagon.getID())
HLT1Wagon.addInputData(dataHLT1)
HLT1Wagon.outputfiles = [
    DiracFile("*.digi"),
    LocalFile("*.xml")]
HLT1Wagon.delete_chain_input = True
train.appendTransform(HLT1Wagon)

# -- HLT2
HLT2Wagon = LHCbTransform(name='Step 4: HLT2 ', backend=Dirac())
HLT2App = GaudiExec()
HLT2App.directory = cmtpath + "/MooreDev_" + HLT_version
HLT2App.platform  = HLT_platform
HLT2App.options  = ["HLT2-Job.py"]
HLT2Wagon.application = HLT2App

dataHLT2 = TaskChainInput(include_file_mask=['\.digi$'], input_trf_id=HLT1Wagon.getID())
HLT2Wagon.addInputData(dataHLT2)
HLT2Wagon.outputfiles = [
    DiracFile("*.digi"),
    LocalFile("*.xml")]
HLT2Wagon.delete_chain_input = True
train.appendTransform(HLT2Wagon)


# -- Configure Brunel

BrunelWagon = LHCbTransform(name='Step 5: Brunel ', backend=Dirac())
BrunelApp = GaudiExec()
BrunelApp.directory = cmtpath + "/BrunelDev_" + Brunel_version
BrunelApp.platform  = Brunel_platform
BrunelApp.options  = ["Brunel-Job.py"]
BrunelWagon.application = BrunelApp

dataBrunel = TaskChainInput(include_file_mask=['\.digi$'], input_trf_id=HLT2Wagon.getID())
BrunelWagon.addInputData(dataBrunel)
BrunelWagon.outputfiles = [
    DiracFile('*.dst'),
    DiracFile("*.root"),
    LocalFile("*.xml")]
BrunelWagon.delete_chain_input = True
train.appendTransform(BrunelWagon)

# -- Configure Stripping

StripWagon = LHCbTransform(name='Step 5: Strip ', backend=Dirac())
StripApp = GaudiExec()
StripApp.directory = cmtpath + "/DaVinciDev_" + Strip_version
StripApp.platform  = Strip_platform
StripApp.options  = ["Strip-Job.py"]
StripWagon.application = StripApp

dataStrip = TaskChainInput(include_file_mask=['\.dst$'], input_trf_id=BrunelWagon.getID())
StripWagon.addInputData(dataStrip)
StripWagon.outputfiles = [
    DiracFile('*.dst'),
    DiracFile("*.root"),
    LocalFile("*.xml")]
StripWagon.delete_chain_input = True
train.appendTransform(StripWagon)


# -- Run!
if not test:
    train.run()



# For reference: steps from 2016 MC radiative production
"""
ID: 48724
Name: RDWG - Sim09d Model for 2016 - MD - Pythia8 - Radiative hh gamma
Type: Simulation
State: Done
Priority: 1a
Author: mmulder WG: RD
Event type: 
Number of events: 
Starting Date: 2018-08-01
Finalization Date: 2018-08-31
Fast Simulation Type: 
Retention Rate: 1

Simulation Conditions: Beam6500GeV-2016-MagDown-Nu1.6-25ns-Pythia8
Beam: beta*~3m, zpv=-3.1mm, xAngle=-0.395mrad and yAngle=0 Beam energy: 6500 GeV Generator: Pythia8 G4 settings: specified in sim step
Magnetic field: -1 Detector: 2016, Velo closed around average x=0.84mm and y=-0.18mm Luminosity: pp collisions nu = 1.6, 25ns spillover

Processing Pass: Sim09d/Trig0x6139160F/Reco16/Turbo03/Stripping28r1p1NoPrescalingFlagged
MC Version: 2016
Step 1 Sim09d - 2016 - MD - Nu1.6 (Lumi 4 at 25ns) - 25ns spillover - Pythia8(133852/Sim09d) : Gauss-v49r10
System config: x86_64-slc6-gcc48-opt MC TCK: 
Options: $APPCONFIGOPTS/Gauss/Beam6500GeV-md100-2016-nu1.6.py;$APPCONFIGOPTS/Gauss/EnableSpillover-25ns.py;$APPCONFIGOPTS/Gauss/DataType-2016.py;$APPCONFIGOPTS/Gauss/RICHRandomHits.py;$DECFILESROOT/options/@{eventType}.py;$LBPYTHIA8ROOT/options/Pythia8.py;$APPCONFIGOPTS/Gauss/G4PL_FTFP_BERT_EmNoCuts.py Options format: Multicore: N
DDDB: dddb-20170721-3 Condition DB: sim-20170721-2-vc-md100 DQTag: 
Extra: AppConfig.v3r359;DecFiles.v30r20 Runtime projects: 
Visible: Y Usable:Yes
Input file types: Output file types: SIM

Step 2 Digi14c for 2015 - 25ns spillover(133533/Digi14c) : Boole-v30r3
System config: x86_64-slc6-gcc49-opt MC TCK: 
Options: $APPCONFIGOPTS/Boole/Default.py;$APPCONFIGOPTS/Boole/EnableSpillover.py;$APPCONFIGOPTS/Boole/DataType-2015.py;$APPCONFIGOPTS/Boole/Boole-SetOdinRndTrigger.py Options format: Multicore: N
DDDB: fromPreviousStep Condition DB: fromPreviousStep DQTag: 
Extra: AppConfig.v3r338 Runtime projects: 
Visible: N Usable:Yes
Input file types: SIM Output file types: DIGI

Step 3 L0 emulation for 2016 - TCK 0x160F - DIGI(130088/L0Trig0x160F) : Moore-v25r4
System config: x86_64-slc6-gcc48-opt MC TCK: 
Options: $APPCONFIGOPTS/L0App/L0AppSimProduction.py;$APPCONFIGOPTS/L0App/L0AppTCK-0x160F.py;$APPCONFIGOPTS/L0App/ForceLUTVersionV8.py;$APPCONFIGOPTS/L0App/DataType-2016.py;$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py Options format: l0app Multicore: N
DDDB: fromPreviousStep Condition DB: fromPreviousStep DQTag: 
Extra: AppConfig.v3r297 Runtime projects: 
Visible: N Usable:Yes
Input file types: DIGI(N) Output file types: DIGI(N)

Step 4 TCK-0x5138160F (HLT1) Flagged for 2016 - DIGI(130089/Trig0x5138160F) : Moore-v25r4
System config: x86_64-slc6-gcc48-opt MC TCK: 
Options: $APPCONFIGOPTS/Moore/MooreSimProductionForSeparateL0AppStep2015.py;$APPCONFIGOPTS/Conditions/TCK-0x5138160F.py;$APPCONFIGOPTS/Moore/DataType-2016.py;$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py;$APPCONFIGOPTS/Moore/MooreSimProductionHlt1.py Options format: Multicore: N
DDDB: fromPreviousStep Condition DB: fromPreviousStep DQTag: 
Extra: AppConfig.v3r297 Runtime projects: 
Visible: N Usable:Yes
Input file types: DIGI(N) Output file types: DIGI(N)

Step 5 TCK-0x6139160F (HLT2) Flagged for 2016 - DIGI(133524/Trig0x6139160F) : Moore-v25r4
System config: x86_64-slc6-gcc48-opt MC TCK: 
Options: $APPCONFIGOPTS/Moore/MooreSimProductionForSeparateL0AppStep2015.py;$APPCONFIGOPTS/Conditions/TCK-0x6139160F.py;$APPCONFIGOPTS/Moore/DataType-2016.py;$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py;$APPCONFIGOPTS/Moore/MooreSimProductionHlt2.py Options format: Multicore: N
DDDB: fromPreviousStep Condition DB: fromPreviousStep DQTag: 
Extra: AppConfig.v3r355 Runtime projects: 
Visible: Y Usable:Yes
Input file types: DIGI Output file types: DIGI

Step 6 Reco16 for MC 2016(133720/Reco16) : Brunel-v50r4
System config: x86_64-slc6-gcc62-opt MC TCK: 
Options: $APPCONFIGOPTS/Brunel/DataType-2016.py;$APPCONFIGOPTS/Brunel/MC-WithTruth.py;$APPCONFIGOPTS/Brunel/SplitRawEventOutput.4.3.py;$APPCONFIGOPTS/Persistency/Compression-ZLIB-1.py Options format: Multicore: N
DDDB: fromPreviousStep Condition DB: fromPreviousStep DQTag: 
Extra: AppConfig.v3r314;SQLDDDB.v7r10 Runtime projects: 
Visible: Y Usable:Yes
Input file types: DIGI Output file types: DST

Step 7 Turbo lines (MC), Turbo 2016 - Stripping28 - uDST(131791/Turbo03) : DaVinci-v41r4p3
System config: x86_64-slc6-gcc48-opt MC TCK: 
Options: $APPCONFIGOPTS/Turbo/Tesla_2016_LinesFromStreams_MC.py;$APPCONFIGOPTS/Turbo/Tesla_PR_Truth_2016.py;$APPCONFIGOPTS/Turbo/Tesla_Simulation_2016.py;$APPCONFIGOPTS/Turbo/Tesla_FilterMC.py Options format: Tesla Multicore: N
DDDB: fromPreviousStep Condition DB: fromPreviousStep DQTag: 
Extra: AppConfig.v3r322;TurboStreamProd.v4r1p4 Runtime projects: 
Visible: Y Usable:Yes
Input file types: DST Output file types: DST

Step 8 Stripping28r1p1-NoPrescalingFlagged for Sim09 - pp at 13 TeV - DST(133138/Stripping28r1p1NoPrescalingFlagged) : DaVinci-v41r4p5
System config: x86_64-slc6-gcc49-opt MC TCK: 
Options: $APPCONFIGOPTS/DaVinci/DV-Stripping28r1p1-Stripping-MC-NoPrescaling-DST.py;$APPCONFIGOPTS/DaVinci/DataType-2016.py;$APPCONFIGOPTS/DaVinci/InputType-DST.py Options format: Multicore: N
DDDB: fromPreviousStep Condition DB: fromPreviousStep DQTag: 
Extra: AppConfig.v3r350;TMVAWeights.v1r9 Runtime projects: 
Visible: Y Usable:Yes
Input file types: DST Output file types: ALLSTREAMS.DST
"""
