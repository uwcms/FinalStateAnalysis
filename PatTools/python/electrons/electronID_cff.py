'''

Run extra electron ID algorithms.

Original author: M. Bachtis

'''

import FWCore.ParameterSet.Config as cms
import sys

recoElectronID42X = cms.Sequence()
recoElectronID5YX = cms.Sequence()

from EgammaAnalysis.ElectronTools.electronIdMVAProducer_cfi import \
        mvaTrigV0, mvaNonTrigV0

recoElectronID5YX += mvaTrigV0
recoElectronID5YX += mvaNonTrigV0

recoElectronID42X += mvaTrigV0
recoElectronID42X += mvaNonTrigV0

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
)
