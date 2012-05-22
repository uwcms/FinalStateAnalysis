'''

Run extra electron ID algorithms.

Original author: M. Bachtis

'''

import FWCore.ParameterSet.Config as cms

from EGamma.EGammaAnalysisTools.electronIdMVAProducer_cfi import \
        mvaTrigV0, mvaNonTrigV0

recoElectronID = cms.Sequence(
    mvaTrigV0 + mvaNonTrigV0
)

# For PAT
electronIDSources = cms.PSet(
	cicLoose = cms.InputTag("eidLoose"),
	cicTight = cms.InputTag("eidTight"),
    mvaTrigV0 = cms.InputTag("mvaTrigV0"),
    mvaNonTrigV0 = cms.InputTag("mvaNonTrigV0"),
)
