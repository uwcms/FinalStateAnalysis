import FWCore.ParameterSet.Config as cms

mvaTrigNoIPPAT = cms.EDProducer(
    "ElectronPATIdMVAProducer",
    verbose = cms.untracked.bool(False),
    electronTag = cms.InputTag('fixme'),
    method = cms.string("BDT"),
    Rho = cms.InputTag("kt6PFJets", "rho"),
    mvaWeightFile = cms.vstring(
        "EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigNoIPV0_2012_Cat1.weights.xml",
        "EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigNoIPV0_2012_Cat2.weights.xml",
        "EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigNoIPV0_2012_Cat3.weights.xml",
        "EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigNoIPV0_2012_Cat4.weights.xml",
        "EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigNoIPV0_2012_Cat5.weights.xml",
        "EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigNoIPV0_2012_Cat6.weights.xml",
        ),
    ## Trig = cms.bool(True),
    ## NoIP = cms.bool(True),
    )

patElectrons2013MVAID = cms.EDProducer(
    "PATElectronValueMapEmbedder",
    src  = cms.InputTag('fixme'),
    maps = cms.VPSet(
        cms.PSet(
            src   = cms.InputTag('mvaTrigNoIPPAT'),
            label = cms.string('mvaTrigNoIP'),
            ),
        ),
)

runAndEmbedSummer13Id = cms.Sequence(mvaTrigNoIPPAT * patElectrons2013MVAID)
