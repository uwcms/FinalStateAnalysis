import FWCore.ParameterSet.Config as cms

from JetMETCorrections.Type1MET.correctionTermsCaloMet_cff import *
muonCaloMETcorr.src = cms.InputTag('muons')
from JetMETCorrections.Type1MET.correctionTermsPfMetType1Type2_cff import *
#process.corrPfMetType1.jetCorrLabel = cms.string("ak5PFL1FastL2L3")
corrPfMetType1.jetCorrLabel = cms.string("ak5PFL1FastL2L3Residual")
from JetMETCorrections.Type1MET.correctionTermsPfMetType0PFCandidate_cff import *
from JetMETCorrections.Type1MET.correctionTermsPfMetType0RecoTrack_cff import *
from JetMETCorrections.Type1MET.correctionTermsPfMetShiftXY_cff import *
#process.corrPfMetShiftXY.parameter = pfMEtSysShiftCorrParameters_2012runABCDvsNvtx_mc
corrPfMetShiftXY.parameter = pfMEtSysShiftCorrParameters_2012runABCDvsNvtx_data
from JetMETCorrections.Type1MET.correctedMet_cff import *

# Import both so provenance tracks it
from FinalStateAnalysis.PatTools.met.metSystematics_cfi import \
        metTypeCategorization, \
        systematicsMET

# Have to import all this stuff so it appears in namespace
from FinalStateAnalysis.PatTools.met.pfMETSignficiance_cfi import \
        metSignficanceSequence, \
        metSigDecentMuons, \
        metSigDecentElectrons, \
        metSigDecentTausUnclean, \
        metSigDecentTaus, \
        metSigJetsDirty, \
        metSigJetsNoMuons, \
        metSigJetsNoElectrons, \
        metSigJetsClean, \
        metSigGetPFJets, \
        pfCandsNotInSelectedJets, \
        pfMEtSignCovMatrix

customizeMETSequence = cms.Sequence(systematicsMET + metSignficanceSequence)
