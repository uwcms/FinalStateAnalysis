'''

Run extra electron ID algorithms.

Original author: M. Bachtis

'''

import FWCore.ParameterSet.Config as cms

from RecoEgamma.ElectronIdentification.\
        cutsInCategoriesElectronIdentificationV06_DataTuning_cfi import \
        eidVeryLoose, eidLoose, eidMedium, eidTight, \
        eidSuperTight, eidHyperTight1, eidHyperTight2, \
        eidHyperTight3, eidHyperTight4


from EGamma.EGammaAnalysisTools.electronIdMVAProducer_cfi import \
        mvaTrigV0, mvaNonTrigV0

recoElectronID = cms.Sequence(
	eidVeryLoose + eidLoose + eidMedium + eidTight +
	eidSuperTight + eidHyperTight1 + eidHyperTight2 +
    eidHyperTight3 + eidHyperTight4
    #+ mvaTrigV0 + mvaNonTrigV0
)

# For PAT
electronIDSources = cms.PSet(
	cicVeryLoose = cms.InputTag("eidVeryLoose"),
	cicLoose = cms.InputTag("eidLoose"),
	cicMedium = cms.InputTag("eidMedium"),
	cicTight = cms.InputTag("eidTight"),
	cicSuperTight = cms.InputTag("eidSuperTight"),
	cicHyperTight1 = cms.InputTag("eidHyperTight1"),
	cicHyperTight2 = cms.InputTag("eidHyperTight2"),
	cicHyperTight3 = cms.InputTag("eidHyperTight3"),
	cicHyperTight4 = cms.InputTag("eidHyperTight4"),
    #mvaTrigV0 = cms.InputTag("mvaTrigV0"),
    #mvaNonTrigV0 = cms.InputTag("mvaNonTrigV0"),
)
