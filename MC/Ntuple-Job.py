# DaVinci options file for ntuple production

##### DaVinci basic settings ##########
from Configurables import DaVinci
nameTuple = "radiativehhpi0RG_R16S28r1p1_MC.root"
DaVinci().EvtMax    = -1
DaVinci().TupleFile = "{0}.root".format(nameTuple)
DaVinci().PrintFreq = 1000

# cute messages
from Gaudi.Configuration import MessageSvc
MessageSvc().Format = "% F%60W%S%7W%R%T %0W%M"

DaVinci().Simulation = True
DaVinci().Lumi       = False
DaVinci().DataType   = "2016"
DaVinci().InputType  = "DST"

##### Conditions settings ##########
from Configurables import CondDB
DaVinci().DDDBtag = "dddb-20170721-3"
DaVinci().CondDBtag = "sim-20170721-2-vc-md100"

##### BASE DTT ##########
from Configurables import DecayTreeTuple
from DecayTreeTuple.Configuration import *
dtt = DecayTreeTuple("BaseTuple")
dtt.ToolList = ["TupleToolEventInfo",
                 "TupleToolPrimaries",
                 "TupleToolRecoStats",
                 "TupleToolCPU",
                 "TupleToolKinematic",
                 "TupleToolPid",
                 "TupleToolAngles",
                 "TupleToolDira",
                 "TupleToolL0Data",
                 "TupleToolDalitz",
                 "TupleToolPhotonInfo",
                 "TupleToolParticleStats",
                 "TupleToolCaloHypo",
                 # MC tuple tools
                 'TupleToolMCTruth',
                 'MCTupleToolEventType',
                 'MCTupleToolPrimaries',
                 'TupleToolMCBackgroundInfo']

# verbose TupleTools
dtt_geo = dtt.addTupleTool("TupleToolGeometry")
dtt_geo.Verbose = True

dtt_trk = dtt.addTupleTool("TupleToolTrackInfo")
dtt_trk.Verbose = True

# Mass substitution info
dtt_subM = dtt.addTupleTool("TupleToolSubMass")
dtt_subM.Substitution += [ 'pi+ => K+'    , 'pi+ => p+'   ,
                            'K+  => pi+'   , 'K+  => p+'   ,
                            'p+  => pi+'   , 'p+  => K+'   ,
                            'gamma => pi0' , 'pi0 =>gamma' ]
dtt_subM.DoubleSubstitution += [ 'pi+/pi- => K+/K-  ' , 'pi+/pi- => p+/p~- ' ,
                                 'pi+/pi- => p+/K-  ' , 'pi+/pi- => K+/p~- ' ,
                                 'K+/K-   => pi+/pi-' , 'K+/K-   => p+/p~- ' ,
                                 'K+/K-   => p+/pi- ' , 'K+/K-   => pi+/p~-' ,
                                 'K+/pi-  => pi+/K- ' , 'K+/pi-  => p+/K-  ' ,
                                 'K+/pi-  => pi+/p~-' , 'K+/pi-  => p+/p~- ' ,
                                 'p+/pi-  => pi+/p~-' , 'p+/pi-  => K+/p~- ' ,
                                 'p+/pi-  => pi+/K- ' , 'p+/pi-  => K+/K-  ' ,
                                 'p+/K-   => K+/p~- ' , 'p+/K-   => pi+/p~-' ,
                                 'p+/K-   => K+/pi- ' , 'p+/K-   => pi+/pi-' , 
                                 'pi+/gamma => K+/pi0', 'pi+/gamma => p+/pi0',
                                 'K+/gamma => pi+/pi0', 'K+/gamma  => p+/pi0',
                                 'p+/gamma => pi+/pi0', 'p+/gamma  => K+/pi0',
                                 'pi+/pi0 => K+/gamma', 'pi+/pi0 => p+/gamma',
                                 'K+/pi0 => pi+/gamma', 'K+/pi0  => p+/gamma',
                                 'p+/pi0 => pi+/gamma', 'p+/pi0  => K+/gamma']

# L0Calo
dtt_L0ECAL = dtt.addTupleTool("TupleToolL0Calo/L0Ecal")
dtt_L0ECAL.WhichCalo = "ECAL"

dtt_L0HCAL = dtt.addTupleTool("TupleToolL0Calo/L0Hcal")
dtt_L0HCAL.WhichCalo = "HCAL"

# Proto particle info
dtt_ProtoP = dtt.addTupleTool("TupleToolProtoPData")
dtt_ProtoP.DataList = ['*Comb*', '*Prob*','VeloCharge','InAcc*',
                       'IsPhoton','*IsNot*','*PhotonID*','*CaloCluster*','*CaloTr*',
                       '*Neutral*','*Shape*','*PrsM*','*CaloDeposit*',
                       '*ShowerShape*','*ClusterMass*']

# Photon veto info
dtt_PhVeto = dtt.addTupleTool("TupleToolVeto/PhotonVeto")
dtt_PhVeto.Particle = "gamma"
dtt_PhVeto.Veto['Pi02gg'] = ['/Event/Phys/StdLoosePi02gg/Particles']
dtt_PhVeto.Veto['Pi0R']   = ['/Event/Phys/StdLooseResolvedPi0/Particles']
dtt_PhVeto.Veto['Eta2gg'] = ['/Event/Phys/StdLooseEta2gg/Particles']
dtt_PhVeto.Veto['Eta']    = ['/Event/Phys/StdLooseResolvedEta/Particles']
dtt_PhVeto.Veto['Pi0M']   = ['/Event/Phys/StdLooseMergedPi0/Particles']

# TISTOS info
dtt_TISTOS = dtt.addTupleTool("TupleToolTrigger")
dtt_TISTOS.VerboseL0   = True
dtt_TISTOS.VerboseHlt1 = True
dtt_TISTOS.VerboseHlt2 = True
dtt_TISTOS.TriggerList = [
    'L0CALO','L0Photon','L0Electron','L0Hadron', 'L0Muon','L0DiMuon',
    'Hlt1TrackMVA','Hlt1TwoTrackMVA', 'Hlt1B2PhiGamma_LTUNB',
    'Hlt1B2GammaGamma','Hlt1TrackMuon',
    'Hlt1TrackMVALoose','Hlt1TwoTrackMVALoose', # 2016
    'Hlt2RadiativeBs2PhiGamma','Hlt2RadiativeBs2PhiGammaUnbiased',
    'Hlt2RadiativeBd2KstGamma','Hlt2RadiativeBd2KstGammaULUnbiased',
    'Hlt2RadiativeLb2L0GammaLL', 'Hlt2RadiativeLb2L0GammaEELL',
    'Hlt2RadiativeB2GammaGamma', 'Hlt2RadiativeB2GammaGammaLL',
    'Hlt2RadiativeB2GammaGammaDD', 'Hlt2RadiativeB2GammaGammaDouble',
    'Hlt2RadiativeIncHHGamma','Hlt2RadiativeIncHHHGamma',
    'Hlt2RadiativeIncHHGammaEE','Hlt2RadiativeIncHHHGammaEE',
    'Hlt2Topo2Body','Hlt2Topo3Body','Hlt2Topo4Body'
    'Hlt2TopoE2Body','Hlt2TopoE3Body','Hlt2TopoE4Body',
    'Hlt2TopoEE2Body','Hlt2TopoEE3Body','Hlt2TopoEE4Body',
    ]


##### Stripping filter ##########
from PhysConf.Filters import LoKi_Filters
fltrs = LoKi_Filters (
    STRIP_Code = "HLT_PASS_RE('.*Beauty2XGamma.*')"
    )
DaVinci().EventPreFilters = fltrs.filters('Filters')

##### Mass substitution ##########
# ie do the magic
from Configurables import SubstitutePID
from PhysSelPython.Wrappers import DataOnDemand

name      = 'kkpi0RG'
line      = 'Beauty2XGamma2pi_pi0R_Line'
#line      = 'Beauty2XGammaphiOmega_2pipi0R_Line'
particles = '/Event/AllStreams/Phys/'+line+'/Particles'
inputs    = [DataOnDemand(particles)]

b = 'B_s0'
r = ['phi(1680)' ,'phi(1020)']
d = ['K+' ,'K-']

sub = SubstitutePID(name+'Subst', Code="DECTREE('X0 -> (X0 -> (X0 -> X+ X- ) pi0 ) gamma')")
sub.Substitutions[' X0 ->  ( X0 ->  (X0 -> ^X+   X- )  pi0 ) gamma']=  d[0]
sub.Substitutions[' X0 ->  ( X0 ->  (X0 ->  X+  ^X- )  pi0 ) gamma']=  d[1]
sub.Substitutions[' X0 -> ^( X0 ->  (X0 ->  X+   X- )  pi0 ) gamma']=  r[0]
sub.Substitutions[' X0 ->  ( X0 -> ^(X0 ->  X+   X- )  pi0 ) gamma']=  r[1]
sub.Substitutions[' X0 ->  ( X0 ->  (X0 ->  X+  X-  )  pi0 ) gamma']=  b
filter = "INTREE(ID=='%s') & INTREE(ID=='%s') & INTREE(ID=='%s') & INTREE(ID=='%s') & INTREE(ID=='%s')" % (b,r[0],r[1],d[0],d[1]) # why is this needed??
sub.MaxParticles=2000

# define selection and sequence
from PhysSelPython.Wrappers import Selection, SelectionSequence
from Configurables import FilterDesktop, GaudiSequencer
sel_sub = Selection(name+'SubSel', Algorithm=sub, RequiredSelections=inputs)
filt    = FilterDesktop(name+'Filt', Code=filter)
sel_filt= Selection(name+'FiltSel', Algorithm=filt, RequiredSelections=[sel_sub])

sel_seq = SelectionSequence(name+'SelSeq', TopSelection=sel_filt)
seq     = GaudiSequencer(name+'Seq')
seq.Members += [sel_seq.sequence()]


##### Bs2KKpi0Gamma DTT ##########
decay = 'B_s0 -> ^(phi(1680) -> ^(phi(1020) -> ^K+  ^K-) ^(pi0 -> ^gamma ^gamma)) ^gamma'
dtt_pi0R = dtt.clone(name+'Tuple')
dtt_pi0R.Decay = decay
dtt_pi0R.Branches = { 'B'  : '^('+decay.replace('^','')+')' }

# DTF
dtf_BMFit = dtt_pi0R.addTupleTool("TupleToolDecayTreeFitter/BMassFit")
dtf_BMFit.Verbose = True
dtf_BMFit.UpdateDaughters = True
dtf_BMFit.constrainToOriginVertex = False
dtf_BMFit.daughtersToConstrain = ['B_s0']

dtf_MFit = dtt_pi0R.addTupleTool("TupleToolDecayTreeFitter/MassFit")
dtf_MFit.Verbose = True
dtf_MFit.UpdateDaughters = True
dtf_MFit.constrainToOriginVertex = False
dtf_MFit.daughtersToConstrain = ['pi0']

# Vtx Isoln
dtt_vtxIso = dtt_pi0R.addTupleTool('TupleToolVtxIsoln')
dtt_vtxIso.Verbose=True    

# offlineVertexFitter
from Configurables import OfflineVertexFitter
dtt_pi0R.VertexFitters.update( { "" : "OfflineVertexFitter"} )
dtt_pi0R.addTool(OfflineVertexFitter)
dtt_pi0R.OfflineVertexFitter.useResonanceVertex = False

# configure decay maker
dtt_pi0R.Inputs = sel_seq.outputLocations()
seq.Members += [ dtt_pi0R ]

# configure the categories
catSeq = GaudiSequencer('hhpi0RG')
catSeq.IgnoreFilterPassed = True
catSeq.Members += [seq]

DaVinci().UserAlgorithms += [catSeq]

# EOF
