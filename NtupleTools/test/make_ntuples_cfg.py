#!/usr/bin/env cmsRun
'''

Ntuple Generation
=================

Generates the ntuples for a given list of final state generation.

Usage:

./make_ntuples_cfg.py channels="mt,em,mm,eemm" [options]

There are some additional pre-defined groups of channels which are expanded
for your convenience::

zh = eeem, eeet, eemt, eett, emmm, emmt, mmmt, mmtt,
zz = eeee, eemm, mmmm,
zgg = eegg, mmgg
llt = emt, mmt, eet, mmm, emm
zg = mmg,eeg
zgxtra = mgg, emg, egg,

The available options (which are set to zero or one) are::

skipEvents=0   - events to skip (for debugging)
maxEvents=-1   - events to run on
rerunMCMatch=0 - rerun MC matching
eventView=0    - make a row in the ntuple correspond to an event
                 instead of a final state in an event.
passThru=0     - turn off any preselection/skim
dump=0         - if one, dump process python to stdout
verbose=0      - print out timing information
noPhotons=0    - don't build things which depend on photons.
runMVAMET=0    - run the MVAMET algorithm
htt=0          - adds Higgs2Taus analysis settings
era="2018"       - choose which era
isLFV=0        - adds LFV Higgs analysis settings
fullJES=0      - adds full systematics for all ~27 JES uncertainties
runningLocal=0 - for sqlite loading and other path names, record if we a running locally or on Condor for example
svFit=1        - run the SVfit on appropriate pairs
rerunQGJetID=0 - rerun the quark-gluon JetID
rerunJets=0    - rerun with new jet energy corrections
runMetFilter=0 - apply met filters
runDQM=0       - run over single object final states to test all 
                 object properties (wont check diobject properties)
hzz=0          - Include FSR contribution a la HZZ4l group, 
                 include all ZZ candidates (including alternative lepton pairings).
zh=0           - This relaxes the criteria for choosing the Z candidates in
                 3lepton+tau and 4lepton final states, is just produces additional combos
isSync=0       - (with eCalib=1 and isMC=1) Apply electron energy 
                 resolution corrections as a 1sigma shift instead of smearing 
                 for synchronization purposes.
eCalib=0       - Apply electron energy scale and resolution corrections.
nExtraJets=0   - Include basic info about this many jets (ordered by pt). 
                 Ignored if final state involves jets.
paramFile=''   - custom parameter file for ntuple production
keepPat=0      - Instead of making flat ntuples, write high level 
                 physics objects including the PATFinalState objects
                 memory use if you don't use them)
isEmbedded=0   - run on embedded sameples
'''

import FWCore.ParameterSet.Config as cms

import os
import copy
from FinalStateAnalysis.NtupleTools.hzg_sync_mod import set_passthru
from FinalStateAnalysis.NtupleTools.ntuple_builder import \
    make_ntuple, add_ntuple
from FinalStateAnalysis.Utilities.version import cmssw_major_version, \
    cmssw_minor_version
import PhysicsTools.PatAlgos.tools.helpers as helpers

process = cms.Process("Ntuples")
cmsswversion=os.environ['CMSSW_VERSION']

# if you want to debug in the future, uncomment this
#process.ProfilerService = cms.Service (
#      "ProfilerService",
#       firstEvent = cms.untracked.int32(2),
#       lastEvent = cms.untracked.int32(500),
#       paths = cms.untracked.vstring('schedule') 
#)
#
#process.SimpleMemoryCheck = cms.Service(
#    "SimpleMemoryCheck",
#    ignoreTotal = cms.untracked.int32(1)
#)


process.options = cms.untracked.PSet(
    allowUnscheduled = cms.untracked.bool(True),
)

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
options = TauVarParsing.TauVarParsing(
    skipEvents=0,  # Start at an event offset (for debugging)
    reportEvery=5000,
    channels='mt,et',
    rerunMCMatch=False,
    eventView=0,  # Switch between final state view (0) and event view (1)
    passThru=0,  # Turn off preselections
    dump=0,  # If one, dump process python to stdout
    verbose=0,  # If one print out the TimeReport
    noPhotons=0,  # If one, don't assume that photons are in the PAT tuples.
    svFit=0,  # If one, SVfit appropriate lepton pairs.
    rochCor="",
    eleCor="",
    rerunQGJetID=0,  # If one reruns the quark-gluon JetID
    runMVAMET=0,  # If one, (re)build the MVA MET (using pairwise algo)
    htt=1,         # If one, apply Higgs2Taus analysis settings
    era="2018",
    fullJES=0,
    runningLocal=0, # For sqlite loading and other path names, record if we a running locally or on Condor for example
    runMETNoHF=0,  # If one, use get metnohf (needs to be recalculated in miniaodv1)
    usePUPPI=0,
    rerunJets=0,
    dblhMode=False, # For double-charged Higgs analysis
    runTauSpinner=0,
    GlobalTag="",
    runMetFilter=0,
    runDQM=0,
    hzz=0,
    zh=0,
    paramFile='',
    runWZ=0,
    isLFV=0,
    runMetUncertainties=0,
    metShift=0,
    runFSRFilter=0, # 1 = filter for ZG, -1 inverts filter for DY
    eventsToSkip='',
    isEmbedded=0,
)

options.register(
    'skimCuts',
    '',
    TauVarParsing.TauVarParsing.multiplicity.list,
    TauVarParsing.TauVarParsing.varType.string,
    'additional cuts to impose on the NTuple'
)
options.register(
    'nExtraJets',
    0,
    TauVarParsing.TauVarParsing.multiplicity.singleton,
    TauVarParsing.TauVarParsing.varType.int,
    'Number of pt-ordered jets to keep some info about. Ignored if final state involves jets.',
)
options.register(
    'keepPat',
    0,
    TauVarParsing.TauVarParsing.multiplicity.singleton,
    TauVarParsing.TauVarParsing.varType.int,
    'If 1, write final PAT objects rather than a flat ntuple. '
    'If 2, also keep packedGenParticles. If 3 or more, also keep '
    'packedPFCands (increases size significantly).',
)
options.register(
    'eCalib',
    0,
    TauVarParsing.TauVarParsing.multiplicity.singleton,
    TauVarParsing.TauVarParsing.varType.int,
    'Apply electron energy scale and resolution corrections. '
    'For data, this is a correction; for MC, it is a smearing'
)
options.register(
    'isSync',
    0,
    TauVarParsing.TauVarParsing.multiplicity.singleton,
    TauVarParsing.TauVarParsing.varType.int,
    'Apply electron energy correction as a 1-sigma shift instead of a '
    'smearing. Only used if eCalib=0 and isMC=1.'
)

options.register(
    'skipMET',
    1,
    TauVarParsing.TauVarParsing.multiplicity.singleton,
    TauVarParsing.TauVarParsing.varType.int,
    "Skip MET corrections and systematics (good way to reduce memory "
    "use if you don't need them)."
)

options.register(
    'miniAODName',
    '',
    TauVarParsing.TauVarParsing.multiplicity.singleton,
    TauVarParsing.TauVarParsing.varType.string,
    "name of miniAOD parent file"
)

options.outputFile = "ntuplize.root"
options.parseArguments()

#########################
### Customize the job ###
#########################

# list of filters to apply
filters = []

# SV Fit requires MVA MET
#options.runMVAMET = (options.runMVAMET or options.svFit or options.htt)

eventsToSkip = cms.untracked.VEventRange()
if options.eventsToSkip:
    # if it is a file
    if os.path.isfile(options.eventsToSkip):
        with open(options.eventsToSkip,'r') as f:
            for e in f:
                eventsToSkip.append(e.rstrip())
    else:
        print 'Warning: event file {0} does not exist.'.format(options.eventsToSkip)


process.source = cms.Source(
    "PoolSource",
    fileNames=cms.untracked.vstring(options.inputFiles),
    skipEvents=cms.untracked.uint32(options.skipEvents),
    eventsToSkip=eventsToSkip,
)

from FinalStateAnalysis.NtupleTools.parameters.default import parameters
if options.paramFile:
    # add custom parameters
    if os.path.isfile(options.paramFile):
        print 'Using custom parameter file %s' % os.path.abspath(options.paramFile)
        import imp
        custParamModule = imp.load_source('custParamModule',options.paramFile)
        from custParamModule import parameters as custParams
        parameters.update(custParams)
    else:
        print 'Failed to load custom parameters, using default.'
    pass
if options.runWZ:
    from FinalStateAnalysis.NtupleTools.parameters.wz import parameters as wzParams
    parameters.update(wzParams)
    #options.eCalib=1 TODO fix when no longer broken
    

if options.eventsToProcess:
    process.source.eventsToProcess = cms.untracked.VEventRange(
        options.eventsToProcess)

# If desired, apply a luminosity mask
if options.lumiMask:
    print "Applying LumiMask from", options.lumiMask
    process.source.lumisToProcess = options.buildPoolSourceLumiMask()

process.TFileService = cms.Service(
    "TFileService", fileName=cms.string(options.outputFile)
)

process.maxEvents = cms.untracked.PSet(
    input=cms.untracked.int32(options.maxEvents))

process.schedule = cms.Schedule()

### To use IgProf's neat memory profiling tools, uncomment the following 
### lines then run this cfg with igprof like so:
###      $ igprof -d -mp -z -o igprof.mp.gz cmsRun ... 
### this will create a memory profile every 250 events so you can track use
### Turn the profile into text with
###      $ igprof-analyse -d -v -g -r MEM_LIVE igprof.yourOutputFile.gz > igreport_live.res
### To do a performance profile instead of a memory profile, change -mp to -pp
### in the first command and remove  -r MEM_LIVE from the second
### For interpretation of the output, see http://igprof.org/text-output-format.html

#from IgTools.IgProf.IgProfTrigger import igprof
#process.load("IgTools.IgProf.IgProfTrigger")
#process.igprofPath = cms.Path(process.igprof)
#process.igprof.reportEventInterval     = cms.untracked.int32(250)
#process.igprof.reportToFileAtBeginJob  = cms.untracked.string("|gzip -c>igprof.begin-job.gz")
#process.igprof.reportToFileAtEvent = cms.untracked.string("|gzip -c>igprof.%I.%E.%L.%R.event.gz")
#process.schedule.append(process.igprofPath)

#load magfield and geometry (for mass resolution)
process.load('Configuration.Geometry.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('Configuration.StandardSequences.Services_cff')

# Need the global tag for geometry etc.
envvar = 'mcgt' if options.isMC else 'datagt'

# All data falls under unified GT (6 Feb 2017) ReReco BCDEFG, Prompt H
GT = {'mcgt': '102X_upgrade2018_realistic_v19', 'datagt': '102X_dataRun2_Prompt_v14'} # For data run D
#GT = {'mcgt': '102X_upgrade2018_realistic_v12', 'datagt': '102X_dataRun2_Sep2018Rereco_v1'} # For data run ABC

if options.era=="2018":
  GT = {'mcgt': '102X_upgrade2018_realistic_v19', 'datagt': '102X_dataRun2_v11'}
if options.era=="2018prompt":
  GT = {'mcgt': '102X_upgrade2018_realistic_v19', 'datagt': '102X_dataRun2_Prompt_v14'}
if options.era=="2017":
  GT = {'mcgt': '94X_mc2017_realistic_v17', 'datagt': '94X_dataRun2_v11'}
if options.era=="2016":
  GT = {'mcgt': '94X_mcRun2_asymptotic_v3', 'datagt': '94X_dataRun2_v10'}


from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, GT[envvar], '')

print 'Using globalTag: %s' % process.GlobalTag.globaltag

# Count events at the beginning of the tuplization
process.load("FinalStateAnalysis.RecoTools.eventCount_cfi")
process.load("FinalStateAnalysis.PatTools.finalStates.patFinalStateLSProducer_cfi")
process.generateMetaInfo = cms.Path(process.eventCount *
                                    process.summedWeight *
                                    process.finalStateLS
                                    )
process.schedule.append(process.generateMetaInfo)

######################################################################
### Uncomment if a hard process tau skim is desired
# process.load("FinalStateAnalysis.NtupleTools.genTauFilter_cfi")
# filters.append(process.filterForGenTaus)
######################################################################

# Drop the input ones, just to make sure we aren't screwing anything up
process.buildFSASeq = cms.Sequence()
from FinalStateAnalysis.PatTools.patFinalStateProducers \
    import produce_final_states
# Which collections are used to build the final states
fs_daughter_inputs = {
    'electrons': 'slimmedElectrons',
    'muons': 'slimmedMuons',
    'taus': 'slimmedTaus',
    'photons': 'slimmedPhotons',
    'jets': 'slimmedJets',
    'pfmet': 'slimmedMETsModifiedMET',         # slimmedMETs, slimmedMETsNoHF (miniaodv2), slimmmedMETsPuppi (not correct in miniaodv1)
    'mvamet': 'fixme',              # produced later
    'puppimet': 'slimmmedMETsPuppi',
    'vertices': 'offlineSlimmedPrimaryVertices',
}

# add additional final states to ntuples with different parameters... work in progress... difficult with VID
additional_fs = {}



###############################
### Customize object inputs ###
###############################

# use metNoHF
if options.runMETNoHF:
    fs_daughter_inputs['pfmet'] = 'slimmedMETsNoHF'

# use puppi instead
if options.usePUPPI:
    fs_daughter_inputs['pfmet'] = 'slimmedMETsPuppi'
    fs_daughter_inputs['jets'] = 'slimmedJetsPuppi'

#####################
### Pileup Jet ID ###
#####################

process.load("RecoJets.JetProducers.PileupJetID_cfi")
process.pileupJetIdUpdated = process.pileupJetId.clone(
  jets=cms.InputTag("slimmedJets"),
  inputIsCorrected=True,
  applyJec=True,
  vertexes=cms.InputTag("offlineSlimmedPrimaryVertices")
)
#process.newPUjetID = cms.Path()
#process.newPUjetID += process.pileupJetIdUpdated
#process.schedule.append(process.newPUjetID)

##################
### JEC ##########
##################

from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
isData = not options.isMC
process.load ("CondCore.CondDB.CondDB_cfi")
#from CondCore.CondDB.CondDB_cfi import *


# Defaults to running correctly for Condor, you can
# pass flag to run locally just fine here with runningLocal=1

sqlitePath = '/{0}/src/FinalStateAnalysis/NtupleTools/data/{1}.db'.format(cmsswversion,'Autumn18_V16_MC' if options.isMC else 'Autumn18_RunABCD_V16_DATA')
if options.runningLocal :
    sqlitePath = '../data/{0}.db'.format('Autumn18_V16_MC' if options.isMC else 'Autumn18_RunABCD_V16_DATA' )

if options.era=="2017":
    sqlitePath = '/{0}/src/FinalStateAnalysis/NtupleTools/data/{1}.db'.format(cmsswversion,'Fall17_17Nov2017_V32_94X_MC' if options.isMC else 'Fall17_17Nov2017_V32_94X_DATA')
    if options.runningLocal :
        sqlitePath = '../data/{0}.db'.format('Fall17_17Nov2017_V32_94X_MC' if options.isMC else 'Fall17_17Nov2017_V32_94X_DATA' )

if options.era=="2016":
    sqlitePath = '/{0}/src/FinalStateAnalysis/NtupleTools/data/{1}.db'.format(cmsswversion,'Summer16_23Sep2016V4_MC' if options.isMC else 'Summer16_23Sep2016AllV4_DATA')
    if options.runningLocal :
        sqlitePath = '../data/{0}.db'.format('Summer16_23Sep2016V4_MC' if options.isMC else 'Summer16_23Sep2016AllV4_DATA' )

JECtag="JetCorrectorParametersCollection_Autumn18_RunABCD_V16_DATA_AK4PFchs"
if options.isMC:
    JECtag="JetCorrectorParametersCollection_Autumn18_V16_MC_AK4PFchs"

if options.era=="2017":
    JECtag="JetCorrectorParametersCollection_Fall17_17Nov2017_V32_94X_DATA_AK4PFchs"
    if options.isMC:
        JECtag="JetCorrectorParametersCollection_Fall17_17Nov2017_V32_94X_MC_AK4PFchs"

if options.era=="2016":
    JECtag="JetCorrectorParametersCollection_Summer16_23Sep2016AllV4_DATA_AK4PFchs"
    if options.isMC:
        JECtag="JetCorrectorParametersCollection_Summer16_23Sep2016V4_MC_AK4PFchs"

process.jec = cms.ESSource("PoolDBESSource",
         DBParameters = cms.PSet(messageLevel = cms.untracked.int32(0)),
         timetype = cms.string('runnumber'),
         toGet = cms.VPSet(cms.PSet(record = cms.string('JetCorrectionsRecord'),
                                    tag    = cms.string(JECtag),
                                    label  = cms.untracked.string('AK4PFchs')
                                    )
                 ),
         connect = cms.string('sqlite:'+sqlitePath)
    )
process.es_prefer_jec = cms.ESPrefer('PoolDBESSource','jec')

## https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#CorrPatJets
from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import updatedPatJetCorrFactors
process.patJetCorrFactorsReapplyJEC = updatedPatJetCorrFactors.clone(
src = cms.InputTag("slimmedJets"),
  levels = ['L1FastJet', 'L2Relative', 'L3Absolute'],
  payload = 'AK4PFchs' ) # Make sure to choose the appropriate levels and payload here!
from PhysicsTools.PatAlgos.producersLayer1.jetUpdater_cff import updatedPatJets
process.patJetsReapplyJEC = updatedPatJets.clone(
  jetSource = cms.InputTag("slimmedJets"),
  jetCorrFactorsSource = cms.VInputTag(cms.InputTag("patJetCorrFactorsReapplyJEC"))
  )
if(isData):
    process.patJetCorrFactorsReapplyJEC.levels = ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']

process.patJetsReapplyJEC.userData.userInts.src += ['pileupJetIdUpdated:fullId']
process.patJetsReapplyJEC.userData.userFloats.src += ['pileupJetIdUpdated:fullDiscriminant']

process.applyJEC = cms.Path()
process.applyJEC += process.pileupJetIdUpdated
process.applyJEC += process.patJetCorrFactorsReapplyJEC
process.applyJEC += process.patJetsReapplyJEC

#if options.isMC: # FIXME apply also to data when the data corrections are released
process.schedule.append(process.applyJEC) #FIXME when JEC need to be rerun
fs_daughter_inputs['jets'] = 'patJetsReapplyJEC' #FIXME when JEC need to be rerun


# Prefiring weights
prefiring_year='2016BtoH'
if options.era=="2018" or options.era=="2018prompt" or options.era=="2017":
   prefiring_year='2017BtoF'

process.prefiringweight = cms.EDProducer(
        "L1ECALPrefiringWeightProducer",
        DataEra=cms.string(prefiring_year),  # Use 2016BtoH for 2016
        UseJetEMPt=cms.bool(False),  # can be set to true to use jet prefiring maps parametrized vs pt(em) instead of pt
        PrefiringRateSystematicUncty=cms.double(0.2)  # Minimum relative prefiring uncty per object
)
process.add_prefiringweight = cms.Path()
process.add_prefiringweight += process.prefiringweight
process.schedule.append(process.add_prefiringweight)


######################
### Build Gen Taus ###
######################
if options.htt and (options.isMC or options.isEmbedded):

    # Build all gen taus
    process.tauGenJets = cms.EDProducer(
        "TauGenJetProducer",
        GenParticles =  cms.InputTag('prunedGenParticles'),
        includeNeutrinos = cms.bool( False ),
        verbose = cms.untracked.bool( False )
        )
    
    # Create filtered groups of tau decay paths
    process.tauGenJetsSelectorAllHadrons = cms.EDFilter("TauGenJetDecayModeSelector",
         src = cms.InputTag("tauGenJets"),
         select = cms.vstring('oneProng0Pi0', 
                              'oneProng1Pi0', 
                              'oneProng2Pi0', 
                              'oneProngOther',
                              'threeProng0Pi0', 
                              'threeProng1Pi0', 
                              'threeProngOther', 
                              'rare'),
         filter = cms.bool(False)
    )
    
    process.tauGenJetsSelectorElectrons = cms.EDFilter("TauGenJetDecayModeSelector",
         src = cms.InputTag("tauGenJets"),
         select = cms.vstring('electron'), 
         filter = cms.bool(False)
    )
    
    process.tauGenJetsSelectorMuons = cms.EDFilter("TauGenJetDecayModeSelector",
         src = cms.InputTag("tauGenJets"),
         select = cms.vstring('muon'), 
         filter = cms.bool(False)
    )

    process.buildGenTaus = cms.Path( 
        process.tauGenJets 
        * process.tauGenJetsSelectorAllHadrons
        * process.tauGenJetsSelectorElectrons
        * process.tauGenJetsSelectorMuons
    )
    process.schedule.append( process.buildGenTaus )





#############################################
### Add Rivet Tools to Ntuples            ###
### for simplified template cross section ###
#############################################

if options.htt and options.isMC :
    process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
    process.mergedGenParticles = cms.EDProducer("MergedGenParticleProducer",
        inputPruned = cms.InputTag("prunedGenParticles"),
        inputPacked = cms.InputTag("packedGenParticles"),
    )
    process.myGenerator = cms.EDProducer("GenParticles2HepMCConverter",
        genParticles = cms.InputTag("mergedGenParticles"),
        genEventInfo = cms.InputTag("generator"),
	signalParticlePdgIds = cms.vint32(25),
    )
    process.rivetProducerHTXS = cms.EDProducer('HTXSRivetProducer',
      HepMCCollection = cms.InputTag('myGenerator','unsmeared'),
      LHERunInfo = cms.InputTag('externalLHEProducer'),
      ProductionMode = cms.string('AUTO'),
      #ProductionMode = cms.string('GGF'), # For ggH NNLOPS sample
    )
    
    process.rivetMethods = cms.Path(
        process.mergedGenParticles
        * process.myGenerator
        * process.rivetProducerHTXS
    )
    process.schedule.append( process.rivetMethods )

################################################
### add filters (that wont make it into fsa) ###
################################################

# Add spurious muon filter (for ReReco 2016 data) tagger
# Contrary to above, the bad muon filters will
# simply tag an event, not actually filter them
# Standard MET filters are also tagged

# 2016 ReReco data spurious muon filters -> tagged
process.load('RecoMET.METFilters.badGlobalMuonTaggersMiniAOD_cff')
process.badGlobalMuonTaggerMAOD.taggingMode = cms.bool(True)
process.cloneGlobalMuonTaggerMAOD.taggingMode = cms.bool(True)
process.badGlobalMuonTaggerMAOD.verbose = cms.untracked.bool(False)
process.cloneGlobalMuonTaggerMAOD.verbose = cms.untracked.bool(False)

# Standard MET filters -> tagged
process.load('RecoMET.METFilters.BadPFMuonFilter_cfi')
process.BadPFMuonFilter.muons = cms.InputTag("slimmedMuons")
process.BadPFMuonFilter.PFCandidates = cms.InputTag("packedPFCandidates")

process.load('RecoMET.METFilters.BadChargedCandidateFilter_cfi')
process.BadChargedCandidateFilter.muons = cms.InputTag("slimmedMuons")
process.BadChargedCandidateFilter.PFCandidates = cms.InputTag("packedPFCandidates")


# Tagger which takes above processes as well as miniAOD filters
# as inputs
trigSource = "PAT" if options.isMC else "RECO"


if options.isEmbedded:
    process.load("FinalStateAnalysis.PatTools.finalStates.patFinalStateEventProducer_cfi")
    #Trigger
    process.patFinalStateEventProducer.trgResultsSrc= cms.InputTag("TriggerResults","","SIMembedding")
    process.patFinalStateEventProducer.trgResultsSrc2= cms.InputTag("TriggerResults","","MERGE")
    #GenInfo
    #process.patFinalStateEventProducer.genParticleSrc = cms.InputTag("prunedGenParticles", "", "MERGE")
    process.patFinalStateEventProducer.packedGenSrc = cms.InputTag("packedGenParticles", "", "MERGE")
    process.patFinalStateEventProducer.l1extraIsoTauSrc=cms.InputTag("caloStage2Digis","Tau","SIMembedding")
    process.patFinalStateEventProducer.isEmbedded = cms.bool(True)


    trigSource = "SIMembedding"


process.filterFlags = cms.EDProducer(
    "MiniAODBadMuonBadFilterEmbedder",
    badGlobalMuonTagger = cms.InputTag("badGlobalMuonTaggerMAOD","bad","Ntuples"),
    cloneGlobalMuonTagger = cms.InputTag("cloneGlobalMuonTaggerMAOD","bad","Ntuples"),
    BadChargedCandidateFilter = cms.InputTag("BadChargedCandidateFilter"),
    BadPFMuonFilter = cms.InputTag("BadPFMuonFilter"),
    triggerSrc = cms.InputTag("TriggerResults","",trigSource),
    #triggerSrc = cms.InputTag("TriggerResults","","RECO"),
    metFilterPaths = cms.vstring(
        "Flag_noBadMuons",
        "Flag_BadPFMuonFilter",
        "Flag_BadChargedCandidateFilter",
        "Flag_HBHENoiseFilter",
        "Flag_HBHENoiseIsoFilter", 
        "Flag_EcalDeadCellTriggerPrimitiveFilter"
        "Flag_goodVertices",
        "Flag_eeBadScFilter",
        "Flag_ecalBadCalibFilter",
        "Flag_globalTightHalo2016Filter",
        "Flag_globalSuperTightHalo2016Filter",
        "Flag_badMuonsFilter",
        "Flag_duplicateMuonsFilter",
    ),
    verbose = cms.untracked.bool(False),
)

process.load('RecoMET.METFilters.ecalBadCalibFilter_cfi')

baddetEcallist = cms.vuint32(
    [872439604,872422825,872420274,872423218,
     872423215,872416066,872435036,872439336,
     872420273,872436907,872420147,872439731,
     872436657,872420397,872439732,872439339,
     872439603,872422436,872439861,872437051,
     872437052,872420649,872422436,872421950,
     872437185,872422564,872421566,872421695,
     872421955,872421567,872437184,872421951,
     872421694,872437056,872437057,872437313])


process.ecalBadCalibReducedMINIAODFilter = cms.EDFilter(
    "EcalBadCalibFilter",
    EcalRecHitSource = cms.InputTag("reducedEgamma:reducedEERecHits"),
    ecalMinEt        = cms.double(50.),
    baddetEcal    = baddetEcallist, 
    taggingMode = cms.bool(True),
    debug = cms.bool(False)
    )


process.filterTagger = cms.Path(
    process.badGlobalMuonTaggerMAOD
    + process.cloneGlobalMuonTaggerMAOD
    + process.BadPFMuonFilter
    + process.BadChargedCandidateFilter
    + process.ecalBadCalibReducedMINIAODFilter 
    + process.filterFlags)

process.schedule.append( process.filterTagger )

if abs(options.runFSRFilter)>0:
    process.FSRFilter = cms.EDFilter("MiniAODGenLeptonFSRFilter",
        src = cms.InputTag("prunedGenParticles"),
        drCut = cms.double(0.05),
        #drCut = cms.double(0.4),
    )
    #if options.runFSRFilter<0:
    if options.runFSRFilter>0:
        process.FSRFilter.reverseDecision=cms.bool(True)
    filters += [process.FSRFilter]


#######################################
### MET Uncertainty and Corrections ###

#######################################

from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
#from PhysicsTools.PatAlgos.slimming.puppiForMET_cff import makePuppiesFromMiniAOD
#makePuppiesFromMiniAOD( process, True );

# If you only want to re-correct and get the proper uncertainties

if options.era=="2017":
    runMetCorAndUncFromMiniAOD(process,
       isData=isData,
       fixEE2017 = True,
       fixEE2017Params = {"userawPt": True, "ptThreshold":50.0, "minEtaThreshold":2.65, "maxEtaThreshold": 3.139} ,
       postfix = "ModifiedMET"
                        )

#    runMetCorAndUncFromMiniAOD(process,
#       isData=isData,
#       fixEE2017 = True,
#       fixEE2017Params = {"userawPt": True, "ptThreshold":50.0, "minEtaThreshold":2.65, "maxEtaThreshold": 3.139} ,
#       metType="Puppi",
#       jetFlavor="AK4PFPuppi",
#       postfix = "Puppi"
#                        )

else:
    runMetCorAndUncFromMiniAOD(process,
       isData=isData,
       postfix = "ModifiedMET"
                        )

#    runMetCorAndUncFromMiniAOD(process,
#       isData=isData,
#       metType="Puppi",
#       jetFlavor="AK4PFPuppi",
#       postfix = "Puppi"
#                        )

process.correctMET=cms.Path(process.fullPatMetSequenceModifiedMET)
process.schedule.append(process.correctMET)

#process.puppiNoLep.useExistingWeights = False
#process.puppi.useExistingWeights = True
#
#process.correctPuppi = cms.Path(
#                     process.egmPhotonIDSequence *
#                     process.puppiMETSequence *
#                     process.fullPatMetSequencePuppi
#                     )
#process.schedule.append(process.correctPuppi)

#########################################################
### embed some things we need before object selection ###
#########################################################

# HZZ id labels
electronMVAGeneralIDLabel = "BDTIDGeneral"
electronMVAHzzIDLabel = "BDTIDHzz"
#electronMVANonTrigIDLabel = "BDTIDNonTrig"
#electronMVATrigIDLabel = "BDTIDTrig"

#########################################
### calibrate electrons and embed ids ###
#########################################
from FinalStateAnalysis.NtupleTools.customization_electrons import preElectrons
fs_daughter_inputs['electrons'] = preElectrons(process,
                                               fs_daughter_inputs['electrons'],
                                               fs_daughter_inputs['vertices'],
                                               options.era,
					       bool(options.isEmbedded),
                                               electronMVAGeneralIDLabel=electronMVAGeneralIDLabel,
                                               electronMVAHzzIDLabel=electronMVAHzzIDLabel,
                                               applyEnergyCorrections=bool(options.eCalib),
                                               isMC=bool(options.isMC),
                                               isSync=bool(options.isSync),
                                               isLFV=bool(options.isLFV),
                                               )

for fs in additional_fs:
    additional_fs[fs]['electrons'] = preElectrons(process,
                                                  additional_fs[fs]['electrons'],
                                                  additional_fs[fs]['vertices'],
						  options.era,
                                                  electronMVAGeneralIDLabel=electronMVAGeneralIDLabel,
                                                  electronMVAHzzIDLabel=electronMVAHzzIDLabel,
                                                  applyEnergyCorrections=bool(options.eCalib),
                                                  isMC=bool(options.isMC),
                                                  isSync=bool(options.isSync),
                                                  postfix=fs,
                                                  )




#############################
###    Pairwise MVA MET   ###
#############################

if options.runMVAMET:
    from RecoMET.METPUSubtraction.MVAMETConfiguration_cff import runMVAMET
    
    mvametJetCollection = "slimmedJets"
    isData = not options.isMC
    if isData :
        mvametJetCollection = "patJetsReapplyJEC"

    from RecoMET.METPUSubtraction.jet_recorrections import recorrectJets
    recorrectJets(process, isData)
    
    runMVAMET( process, jetCollectionPF = mvametJetCollection )
    process.MVAMET.srcLeptons  = cms.VInputTag("slimmedMuons", "slimmedElectrons", "slimmedTaus")
    process.MVAMET.requireOS = cms.bool(False)
    process.MVAMETSequence = cms.Path(process.MVAMET)

    process.schedule.append(process.MVAMETSequence)

# Add met significane for normal RECO METs for svFit testing
# of MvaMet vs. Normas Mets
# Note, default uses slimmedMETs which is PF Met
process.load("RecoMET.METProducers.METSignificance_cfi")

process.METSigSeq = cms.Path(process.METSignificance)
process.schedule.append(process.METSigSeq)

######################
### embed muon IDs ###
######################


from FinalStateAnalysis.NtupleTools.customization_muons import preMuons
fs_daughter_inputs['muons'] = preMuons(process,
                                       bool(options.isEmbedded),
                                       fs_daughter_inputs['muons'],
                                       fs_daughter_inputs['vertices'])
for fs in additional_fs:
    additional_fs[fs]['muons'] = preMuons(process,
					  bool(options.isEmbedded),
                                          additional_fs[fs]['muons'],
                                          additional_fs[fs]['vertices'],
                                          postfix=fs)

#####################
### embed tau IDs ###
#####################
from FinalStateAnalysis.NtupleTools.customization_taus import preTaus
fs_daughter_inputs['taus'] = preTaus(process,
                                     bool(options.isEmbedded),
                                     fs_daughter_inputs['taus'],
                                     fs_daughter_inputs['vertices'],
                                     rerunMvaIDs=options.htt)
for fs in additional_fs:
    additional_fs[fs]['taus'] = preTaus(process,
	                                bool(options.isEmbedded),
                                        additional_fs[fs]['taus'],
                                        additional_fs[fs]['vertices'],
                                        postfix=fs,
                                        rerunMvaIDs=options.htt)

########################
### embed photon IDs ###
########################
from FinalStateAnalysis.NtupleTools.customization_photons import prePhotons
fs_daughter_inputs['photons'] = prePhotons(process,
                                           fs_daughter_inputs['photons'],
                                           fs_daughter_inputs['vertices'])
for fs in additional_fs:
    additional_fs[fs]['photons'] = prePhotons(process,
                                              additional_fs[fs]['photons'],
                                              additional_fs[fs]['vertices'],
                                              postfix=fs)

########################
### jet id embedding ###
########################
if options.era=="2018" or options.era=="2018prompt":
  from FinalStateAnalysis.NtupleTools.customization_jets import preJets
  from FinalStateAnalysis.NtupleTools.customization_metjets import preMETFromJES
if options.era=="2017":
  from FinalStateAnalysis.NtupleTools.customization_2017jets import preJets
  from FinalStateAnalysis.NtupleTools.customization_2017metjets import preMETFromJES
if options.era=="2016":
  from FinalStateAnalysis.NtupleTools.customization_2016jets import preJets
  from FinalStateAnalysis.NtupleTools.customization_2016metjets import preMETFromJES

fs_daughter_inputs['jets']  = preJets(process,
                                     fs_daughter_inputs['jets'],
                                     fs_daughter_inputs['vertices'],
                                     fs_daughter_inputs['pfmet'], 
                                     fs_daughter_inputs['muons'],
                                     fs_daughter_inputs['electrons'],
                                     doBTag=False,
                                     doFullJESUnc=options.fullJES,
                                     runningLocal=options.runningLocal,
                                     jType="AK4PFchs")

if options.fullJES and options.metShift:
    fs_daughter_inputs['pfmet'] = preMETFromJES(process,
                                     fs_daughter_inputs['jets'],
                                     fs_daughter_inputs['vertices'],
                                     fs_daughter_inputs['pfmet'],
                                     fs_daughter_inputs['muons'],
                                     fs_daughter_inputs['electrons'],
                                     doBTag=False,
                                     doFullJESUnc=options.fullJES,
                                     runningLocal=options.runningLocal,
                                     jType="AK4PFchs")

for fs in additional_fs:
    additional_fs[fs]['jets'] = preJets(process,
                                        additional_fs[fs]['jets'],
                                        additional_fs[fs]['vertices'],
                                        fs_daughter_inputs['pfmet'], 
                                        additional_fs[fs]['muons'],
                                        additional_fs[fs]['electrons'],
                                        jType="AK4PFchs",
                                        postfix=fs)   # why do we need to redo this?  the cleaning?
    
    additional_fs[fs]['pfmet'] = preMETFromJES(process,
                                        additional_fs[fs]['jets'],
                                        additional_fs[fs]['vertices'],
                                        fs_daughter_inputs['pfmet'],
                                        additional_fs[fs]['muons'],
                                        additional_fs[fs]['electrons'],
                                        jType="AK4PFchs",
                                        postfix=fs)   # why do we need to redo this?  the cleaning? 


########################################
### pre selection HZZ customizations ###
########################################
idCheatLabel = "HZZ4lIDPass" # Gets loose ID. For tight ID, append "Tight".
isoCheatLabel = "HZZ4lIsoPass"
if options.hzz:
    from FinalStateAnalysis.NtupleTools.customization_hzz import hzzCustomize
    hzzCustomize(process, fs_daughter_inputs, idCheatLabel, isoCheatLabel,
                 electronMVAHzzIDLabel , "dretFSRCand")
#                 electronMVANonTrigIDLabel, "dretFSRCand")
    # fs_daughter_inputs entries for electrons, muons, jets, and fsr are automatically 
    # set by hzzCustomize()



###########################
### object preselection ###
###########################
if options.passThru:
    preselections = {}
else:
    preselections = parameters.get('preselection',{})

from FinalStateAnalysis.NtupleTools.object_parameter_selector import setup_selections
process.preselectionSequence = setup_selections(
    process, 
    "Preselection",
    fs_daughter_inputs,
    preselections,
    )
process.FSAPreselection = cms.Path(process.preselectionSequence)
process.schedule.append(process.FSAPreselection)

for fs in additional_fs:
    preSeqName = 'preselectionSequence{0}'.format(fs)
    preSeq = setup_selections(
        process,
        "Preselection",
        additional_fs[fs],
        preselections,
        postfix=fs,
        )
    setattr(process,preSeqName,preSeq)
    for ob in preselections:
        additional_fs[fs][getName(ob)+'s'] = getName(ob)+"Preselection{0}".format(fs)
    setattr(process,'FSAPreselection{0}'.format(fs),cms.Path(getattr(process,preSeqName)))
    process.schedule.append(getattr(process,'FSAPreselection{0}'.format(fs)))



###########################################################################
### The following is embedding that must be done after object selection ###
###########################################################################

###################################
### post electron customization ###
###################################

from FinalStateAnalysis.NtupleTools.customization_electrons import postElectrons
fs_daughter_inputs['electrons'] = postElectrons(process,fs_daughter_inputs['electrons'],fs_daughter_inputs['jets'])

for fs in additional_fs:
    additional_fs[fs]['electrons'] = postElectrons(process,additional_fs[fs]['electrons'],additional_fs[fs]['jets'],postfix=fs)


###############################
### post muon customization ###
###############################
from FinalStateAnalysis.NtupleTools.customization_muons import postMuons
fs_daughter_inputs['muons'] = postMuons(process,fs_daughter_inputs['muons'],fs_daughter_inputs['jets'])
for fs in additional_fs:
    additional_fs[fs]['muons'] = postMuons(process,additional_fs[fs]['muons'],additional_fs[fs]['jets'],postfix=fs)

##############################
### post tau customization ###
##############################
from FinalStateAnalysis.NtupleTools.customization_taus import postTaus
fs_daughter_inputs['taus'] = postTaus(process,fs_daughter_inputs['taus'],fs_daughter_inputs['jets'])
for fs in additional_fs:
    additional_fs[fs]['taus'] = postTaus(process,additional_fs[fs]['taus'],additional_fs[fs]['jets'],postfix=fs)

#################################
### post photon customization ###
#################################
from FinalStateAnalysis.NtupleTools.customization_photons import postPhotons
fs_daughter_inputs['photons'] = postPhotons(process,fs_daughter_inputs['photons'],fs_daughter_inputs['jets'])
for fs in additional_fs:
    additional_fs[fs]['photons'] = postTaus(process,additional_fs[fs]['photons'],additional_fs[fs]['jets'],postfix=fs)







############################
### Now do the FSA stuff ###
############################

# Make a list of collections to save (in case we're saving 
# collections instead of flat ntuples)
# Note that produce_final_states adds the PATFinalStateEvent and
# the collections it used to build the final states, but not the final
# states themselves, because that fills the file up with unwanted stuff
output_to_keep = []

# Eventually, set buildFSAEvent to False, currently working around bug
# in pat tuples.
produce_final_states(process, 
                     fs_daughter_inputs, 
                     output_to_keep, 
                     process.buildFSASeq,
                     'puTagDoesntMatter', 
                     options.channels,
                     isLFV=bool(options.isLFV),
                     isMC=bool(options.isMC),
                     buildFSAEvent=True,
                     noTracks=True, 
                     runMVAMET=False,
                     hzz=options.hzz, 
                     rochCor=options.rochCor,
                     eleCor=options.eleCor, 
                     **parameters)
process.buildFSAPath = cms.Path(process.buildFSASeq)
# Don't crash if some products are missing (like tracks)
process.patFinalStateEventProducer.forbidMissing = cms.bool(False)
process.schedule.append(process.buildFSAPath)

for fs in additional_fs:
    setattr(process,'buildFSASeq{0}'.format(fs),cms.Sequence())
    produce_final_states(process, 
                         additional_fs[fs], 
                         output_to_keep, 
                         getattr(process,'buildFSASeq{0}'.format(fs)),
                         'puTagDoesntMatter', 
                         options.channels,
                         buildFSAEvent=True,
                         noTracks=True, 
                         runMVAMET=False,
                         hzz=options.hzz, 
                         rochCor=options.rochCor,
                         eleCor=options.eleCor, 
                         postfix=fs, 
                         **parameters)
    setattr(process,'buildFSAPath{0}'.format(fs), cms.Path(getattr(process,'buildFSASeq{0}'.format(fs))))
    getattr(process,'patFinalStateEventProducer{0}'.format(fs)).forbidMissing = cms.bool(False)
    process.schedule.append(getattr(process,'buildFSAPath{0}'.format(fs)))

# Drop the old stuff. (do we still need this?)
process.source.inputCommands = cms.untracked.vstring(
    'keep *',
    'drop PATFinalStatesOwned_finalState*_*_*',
    'drop *_patFinalStateEvent*_*_*'
)

suffix = '' # most analyses don't need to modify the final states

# turn options.channels into actual channels
from FinalStateAnalysis.NtupleTools.channel_handling import parseChannels, \
    get_channel_suffix

#if options.hzz:
#    process.embedHZZSeq = cms.Sequence()
#    # Embed matrix elements in relevant final states
#    suffix = "HZZ"
#    for ch in parseChannels(options.channels):
#        prodSuffix = get_channel_suffix(ch)
#        oldName = "finalState%s"%prodSuffix
#        newName = oldName + suffix
#
#        if len(ch) == 4:
#            # 4l final states might be higgses, so do some higgs analysis
#            embedCategoryProducer = cms.EDProducer(
#                "MiniAODHZZCategoryEmbedder",
#                src = cms.InputTag(oldName),
#                tightLepCut = cms.string('userFloat("HZZ4lIDPassTight") > 0.5 && userFloat("HZZ4lIsoPass") > 0.5'),
#                bDiscriminator = cms.string("pfCombinedInclusiveSecondaryVertexV2BJetTags"),
#                bDiscriminantCut = cms.double(0.89),
#                )
#            # give the FS collection an intermediate name, with an identifying suffix
#            intermediateName = oldName + "HZZCategory"
#            setattr(process, intermediateName, embedCategoryProducer)
#            process.embedHZZSeq += embedCategoryProducer
#            
#            embedMEProducer = cms.EDProducer(
#                "MiniAODHZZMEEmbedder%s"%prodSuffix,
#                src = cms.InputTag(intermediateName),
#                processes = cms.vstring("p0plus_VAJHU",
#                                        "p0minus_VAJHU",
#                                        "Dgg10_VAMCFM",
#                                        "bkg_VAMCFM",
#                                        "phjj_VAJHU",
#                                        "pvbf_VAJHU",
#                                        ),
#                fsrLabel = cms.string("dretFSRCand"),
#                )
#            # give the FS collection the same name as before, but with an identifying suffix
#            setattr(process, newName, embedMEProducer)
#            process.embedHZZSeq += embedMEProducer
#        else:
#            # Copy the other final states to keep naming consistent
#            copier = cms.EDProducer(
#                "PATFinalStateCopier",
#                src = cms.InputTag(oldName),
#                )
#            setattr(process, newName, copier)
#            process.embedHZZSeq += copier
#            
#    process.embedHZZ = cms.Path(process.embedHZZSeq)
#    process.schedule.append(process.embedHZZ)
        

#Cecile vertex fitting

#process.embedVFSeq = cms.Sequence()
## Embed matrix elements in relevant final states
#suffix = "HZZ"
#for ch in parseChannels(options.channels):
#     prodSuffix = get_channel_suffix(ch)
#     oldName = "finalState%s"%prodSuffix
#     newName = oldName + suffix
#     embedVFProducer = cms.EDProducer(
#             "MiniAODVertexFittingEmbedder",
#             src = cms.InputTag(oldName)
#             )
#     # give the FS collection an intermediate name, with an identifying suffix
#     intermediateName = oldName + "VFCategory"
#     setattr(process, newName, embedVFProducer)
#     process.embedVFSeq += embedVFProducer
#
#process.embedVF = cms.Path(process.embedVFSeq)
#process.schedule.append(process.embedVF)


# run dqm
if options.runDQM: options.channels = 'dqm'
print process.schedule


if options.keepPat:
    print "Saving final physics objects instead of making ntuples"

    # Clean unwanted final states (otherwise happens at flat ntuple creation)
    from FinalStateAnalysis.NtupleTools.uniqueness_cut_generator import uniqueness_cuts

    ptCuts = parameters.get('ptCuts', {'e':'0','m':'0','t':'0','g':'0','j':'0'})
    etaCuts = parameters.get('etaCuts', {'e':'10','m':'10','t':'10','g':'10','j':'10'})
    skimCuts = parameters.get('skimCuts', [])

    if options.passThru:
        output_to_keep.append('*')
    else:
        process.finalStateCleaning = cms.Sequence()

        for fs in parseChannels(options.channels):
            fsCuts = cms.vstring()
            for name, cut in uniqueness_cuts(fs, ptCuts, etaCuts, 
                                             skimCuts=skimCuts,
                                             hzz=options.hzz, 
                                             dblH=options.dblhMode).iteritems():
                fsCuts.append(cut)
                
            fsCleaner = cms.EDProducer(
                "PATFinalStateSelector",
                src = cms.InputTag("finalState%s%s"%(get_channel_suffix(fs), suffix)),
                cuts = fsCuts,
                )
            
            # give the producer a good name so it's easy to find the output
            cleanerName = 'cleanedFinalState%s'%get_channel_suffix(fs)
            setattr(process, cleanerName, fsCleaner)
            process.finalStateCleaning += fsCleaner
            
            # and keep the output in the final file
            output_to_keep.append('*_%s_*_*'%cleanerName)

        process.cleanFinalStates = cms.Path(process.finalStateCleaning)
        process.schedule.append(process.cleanFinalStates)

    # keep final object collections (final states and associated collections already saved)
    for name, label in fs_daughter_inputs.iteritems():
        output_to_keep.append('*_%s_*_*'%label)

    # keep important gen particles
    output_to_keep.append('*_prunedGenParticles_*_*')
    if options.keepPat >= 2:
        print "... Including packedGenParticles"
        output_to_keep.append('*_packedGenParticles_*_*')
        if options.keepPat >= 3:
            print "... Including packedPFCandidates"
            output_to_keep.append('*_packedPFCandidates_*_*')
    output_commands = cms.untracked.vstring('drop *')

    for product in output_to_keep:
        output_commands.append('keep %s'%product)

    process.out = cms.OutputModule(
        "PoolOutputModule",
        fileName=cms.untracked.string(options.outputFile),
        # Drop per-event meta data from dropped objects
        dropMetaData=cms.untracked.string("ALL"),
        outputCommands=output_commands,
        )
    
    process.save = cms.EndPath(process.out)
    process.schedule.append(process.save)
else:
    print "Building ntuple for final states: %s" % ", ".join(x.strip() for x in options.channels.split(','))
    for final_state in parseChannels(options.channels):
        if additional_fs: print 'Adding ntuple {0}'.format(final_state)
        extraJets = options.nExtraJets
        analyzer = make_ntuple(*final_state, 
                                svFit=options.svFit, 
                                dblhMode=options.dblhMode,
                                runTauSpinner=options.runTauSpinner, 
                                runMVAMET=False,
                                fullJES=options.fullJES,
                                skimCuts=options.skimCuts, 
                                suffix=suffix,
                                hzz=options.hzz, 
                                zh=options.zh,
                                nExtraJets=extraJets, 
                                isMC=options.isMC,
                                isShiftedMet=bool(options.metShift),
                                miniAODName=options.miniAODName,
                                **parameters)
        add_ntuple(final_state, analyzer, process,
                   process.schedule, options.eventView, filters)
        for fs in additional_fs:
            print "Adding additional ntuple with postfix {0}".format(fs)
            analyzer = make_ntuple(*final_state,
                                    svFit=options.svFit, 
                                    dblhMode=options.dblhMode,
                                    runTauSpinner=options.runTauSpinner,
                                    runMVAMET=False,
                                    fullJES=options.fullJES,
                                    skimCuts=options.skimCuts, 
                                    suffix=suffix,
                                    hzz=options.hzz, 
                                    nExtraJets=extraJets,
                                    isMC=options.isMC,
                                    isShiftedMet=bool(options.metShift),
                                    postfix=fs,
                                    **parameters)
            add_ntuple(final_state+fs, analyzer, process,
                       process.schedule, options.eventView, filters)


if options.passThru:
    set_passthru(process)

if options.dump:
    print process.dumpPython()


process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.MessageLogger.cerr.FwkReport.reportEvery = options.reportEvery
process.MessageLogger.categories.append('FSAEventMissingProduct')
process.MessageLogger.categories.append('UndefinedPreselectionInfo')
process.MessageLogger.categories.append('GsfElectronAlgo')
process.MessageLogger.categories.append('MiniAODJetFullSystematicsEmbedder')

# Don't go nuts if there are a lot of missing products.
process.MessageLogger.cerr.FSAEventMissingProduct = cms.untracked.PSet(
    limit=cms.untracked.int32(10)
)
# process.MessageLogger.suppresssWarning = cms.untracked.vstring("GsfElectronAlgo","UndefinedPreselectionInfo")
process.MessageLogger.cerr.GsfElectronAlgo = cms.untracked.PSet(
    limit = cms.untracked.int32(0)
)
process.MessageLogger.cerr.UndefinedPreselectionInfo = cms.untracked.PSet(
    limit = cms.untracked.int32(0)
)

if options.verbose:
    process.options.wantSummary = cms.untracked.bool(True)
if options.passThru:
    set_passthru(process)

if options.dump:
    print process.dumpPython()




