'''

Run extra electron ID algorithms.

Original author: M. Bachtis

'''

import FWCore.ParameterSet.Config as cms
import sys

recoElectronID42X = cms.Sequence()
recoElectronID5YX = cms.Sequence()

try:
    from EGamma.EGammaAnalysisTools.electronIdMVAProducer_cfi import \
            mvaTrigV0, mvaNonTrigV0

    from FinalStateAnalysis.PatTools.electrons.electronMVAID2012_config_cfi import \
         mvaTrigIDISOV0

    recoElectronID5YX += mvaTrigV0
    recoElectronID5YX += mvaNonTrigV0
    recoElectronID5YX += mvaTrigIDISOV0

    recoElectronID42X += mvaTrigV0
    recoElectronID42X += mvaNonTrigV0
    
except ImportError:
    # Don't crash if not installed
    sys.stderr.write(__file__ +
                     ": EG MVA ID dependency not installed, will not be run!\n")
# For PAT
electronIDSources42X = cms.PSet(
	cicLoose = cms.InputTag("eidLoose"),
	cicTight = cms.InputTag("eidTight"),
        mvaTrigV0 = cms.InputTag("mvaTrigV0"),
        mvaNonTrigV0 = cms.InputTag("mvaNonTrigV0")
)

electronIDSources5YX = cms.PSet(
	cicLoose = cms.InputTag("eidLoose"),
	cicTight = cms.InputTag("eidTight"),
        mvaTrigV0 = cms.InputTag("mvaTrigV0"),
        mvaNonTrigV0 = cms.InputTag("mvaNonTrigV0"),
        mvaTrigIDISOV0 = cms.InputTag("mvaTrigIDISOV0")
)
