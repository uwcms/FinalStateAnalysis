'''

Embed working point cuts into pat::Electrons

See:

https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorking2012#Object_ID_AN1

'''
import FWCore.ParameterSet.Config as cms

patElectronMVAIDWPEmbedding = cms.EDProducer(
    "PATElectronWorkingPointEmbedder",
    src=cms.InputTag("fixme"),
    userIntLabel=cms.string('mvaidwp'),
    categories=cms.VPSet(
        cms.PSet(
            category=cms.string('pt < 20 & abs(superCluster.eta) < 0.8'),
            cut=cms.string('electronID("mvaNonTrigV0") > 0.925')
        ),
        cms.PSet(
            category=cms.string(
                'pt < 20 & '
                'abs(superCluster.eta) >= 0.8 &'
                'abs(superCluster.eta) < 1.479'),
            cut=cms.string('electronID("mvaNonTrigV0") > 0.915')
        ),
        cms.PSet(
            category=cms.string('pt < 20 & abs(superCluster.eta) >= 1.479'),
            cut=cms.string('electronID("mvaNonTrigV0") > 0.965')
        ),
        cms.PSet(
            category=cms.string('pt >= 20 & abs(superCluster.eta) < 0.8'),
            cut=cms.string('electronID("mvaNonTrigV0") > 0.905')
        ),
        cms.PSet(
            category=cms.string(
                'pt >= 20 & '
                'abs(superCluster.eta) >= 0.8 & '
                'abs(superCluster.eta) < 1.479'),
            cut=cms.string('electronID("mvaNonTrigV0") > 0.955')
        ),
        cms.PSet(
            category=cms.string('pt >= 20 & abs(superCluster.eta) >= 1.479'),
            cut=cms.string('electronID("mvaNonTrigV0") > 0.975')
        ),
    )
)


"""
Electron MVA ID for HZZ4L

https://twiki.cern.ch/twiki/bin/viewauth/CMS/HiggsZZ4l2013Moriond#Electrons
"""
patElectronMVAIDZZEmbedding = cms.EDProducer(
    "PATElectronWorkingPointEmbedder",
    src             = cms.InputTag("fixme"),
    userIntLabel    = cms.string('mvaidzz'),
    categories      = cms.VPSet(
        cms.PSet(
            category    = cms.string(
                    '5 < pt & pt < 10 &'
                    'abs(superCluster.eta) < 0.8'),
            cut         = cms.string(
                    'electronID("mvaNonTrigV0") > 0.47')
            ),
        cms.PSet(
            category    = cms.string(
                    '5 < pt & pt < 10 &'
                    'abs(superCluster.eta) > 0.8 &'
                    'abs(superCluster.eta) < 1.479'),
            cut         = cms.string(
                    'electronID("mvaNonTrigV0") > 0.004')
            ),
        cms.PSet(
            category    = cms.string(
                    '5 < pt & pt < 10 &'
                    'abs(superCluster.eta) > 1.479'),
            cut         = cms.string(
                    'electronID("mvaNonTrigV0") > 0.295')
            ),
        cms.PSet(
            category    = cms.string(
                    'pt > 10 &'
                    'abs(superCluster.eta) < 0.8'),
            cut         = cms.string(
                    'electronID("mvaNonTrigV0") > 0.5')
            ),
        cms.PSet(
            category    = cms.string(
                    'pt > 10 &'
                    'abs(superCluster.eta) > 0.8 &'
                    'abs(superCluster.eta) < 1.479'),
            cut         = cms.string(
                    'electronID("mvaNonTrigV0") > 0.12')
            ),
        cms.PSet(
            category    = cms.string(
                    'pt > 10 &'
                    'abs(superCluster.eta) > 1.479'),
            cut         = cms.string(
                    'electronID("mvaNonTrigV0") > 0.6')
            )
        )
    )

