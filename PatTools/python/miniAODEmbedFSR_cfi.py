import FWCore.ParameterSet.Config as cms

#########################################################################
##                                                                     ##
##  Embed FSR photons in muons and electrons as userCands              ##
##                                                                     ##
##  Requires the other lepton collection (e.g. muons if you're         ##
##  embedding in electrons as a stupid hack to make a photon is only   ##
##  embedded in its favorite lepton. Requires lots of cuts that will   ##
##  be part of the final selectrions because FML.                      ##
##                                                                     ##
#########################################################################


src                          = cms.InputTag("fixme_primaryLeptons")
srcAlt                       = cms.InputTag("fixme_otherLeptonCollection")
srcPho                       = cms.InputTag("fixme_FSRPhotons")
srcVeto                      = cms.InputTag("fixme_electrons")
srcVtx                       = cms.InputTag("selectedPrimaryVertex")
# userLabel                    = cms.InputTag("you could change this if you wanted to (default: FSRCand)")
isoLabels                    = cms.vstring(
                                           'fsrPhotonPFIsoChHadPUNoPU03pt02',
                                           'fsrPhotonPFIsoNHadPhoton03',
                                           )
dRInner                      = cms.double(0.07)
dROuter                      = cms.double(0.5)
isoInner                     = cms.double(999.9)
isoOuter                     = cms.double(1.)
ptInner                      = cms.double(2.)
ptOuter                      = cms.double(4.)
maxEta                       = cms.double(2.4)
vetoDR                       = cms.double(0.15)
vetoDPhi                     = cms.double(2.)
vetoDEta                     = cms.double(0.05)
idDecisionLabel              = cms.string("fixme")




embedFSRInMuons = cms.EDProducer(
    "MiniAODMuonFSREmbedder",
    src                          = src,
    srcAlt                       = srcAlt,
    srcVeto                      = srcVeto,
    srcVtx                       = srcVtx,
    isoLabels                    = isoLabels,                                   
    dRInner                      = dRInner,
    dROuter                      = dROuter,
    isoInner                     = isoInner,
    isoOuter                     = isoOuter,
    ptInner                      = ptInner,
    ptOuter                      = ptOuter,
    maxEta                       = maxEta,
    vetoDR                       = vetoDR,
    vetoDPhi                     = vetoDPhi,
    vetoDEta                     = vetoDEta,
    idDecisionLabel              = idDecisionLabel,
)


embedFSRInElectrons = cms.EDProducer(
    "MiniAODElectronFSREmbedder",
    src                          = src,
    srcAlt                       = srcAlt,
    srcVeto                      = srcVeto,
    srcVtx                       = srcVtx,
    isoLabels                    = isoLabels,                                   
    dRInner                      = dRInner,
    dROuter                      = dROuter,
    isoInner                     = isoInner,
    isoOuter                     = isoOuter,
    ptInner                      = ptInner,
    ptOuter                      = ptOuter,
    maxEta                       = maxEta,
    vetoDR                       = vetoDR,
    vetoDPhi                     = vetoDPhi,
    vetoDEta                     = vetoDEta,
    idDecisionLabel              = idDecisionLabel,
)


