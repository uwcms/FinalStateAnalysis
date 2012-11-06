'''

Run extra electron ID algorithms.

Original author: M. Bachtis

'''

import FWCore.ParameterSet.Config as cms
import sys

recoElectronID = cms.Sequence()

try:
    from EGamma.EGammaAnalysisTools.electronIdMVAProducer_cfi import \
            mvaTrigV0, mvaNonTrigV0

    recoElectronID += mvaTrigV0
    recoElectronID += mvaNonTrigV0
except ImportError:
    # Don't crash if not installed
    sys.stderr.write(__file__ +
                     ": EG MVA ID dependency not installed, will not be run!\n")
# For PAT
electronIDSources = cms.PSet(
	cicLoose = cms.InputTag("eidLoose"),
	cicTight = cms.InputTag("eidTight"),
    mvaTrigV0 = cms.InputTag("mvaTrigV0"),
    mvaNonTrigV0 = cms.InputTag("mvaNonTrigV0"),
)
