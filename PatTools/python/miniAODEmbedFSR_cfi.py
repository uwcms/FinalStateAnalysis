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
label                        = cms.InputTag("you could change this if you wanted to (default: FSRCand)")
isoLabels                    = cms.VInputTag(
                                             cms.InputTag("fsrPhotonPFIsoChHadPUNoPU03pt02"),
                                             cms.InputTag("fsrPhotonPFIsoNHadPhoton03"),
                                             ),
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
electronPt                   = cms.double(7.)
electronMaxEta               = cms.double(2.5)
electronSIP                  = cms.double(4.)
electronPVDXY                = cms.double(0.5)
electronPVDZ                 = cms.double(1.)
electronIDPtThr              = cms.double(10.)
electronIDEtaThrLow          = cms.double(0.8)
electronIDEtaThrHigh         = cms.double(1.479)
electronIDCutLowPtLowEta     = cms.double(0.47)
electronIDCutLowPtMedEta     = cms.double(0.004)
electronIDCutLowPtHighEta    = cms.double(0.295)
electronIDCutHighPtLowEta    = cms.double(-0.34)
electronIDCutHighPtMedEta    = cms.double(-0.65)
electronIDCutHighPtHighEta   = cms.double(0.6)
electronIDLabel              = cms.string("MVANonTrigCSA14")
muonPt                       = cms.double(5.)
muonMaxEta                   = cms.double(2.4)
muonSIP                      = cms.double(4.)
muonPVDXY                    = cms.double(0.5)
muonPVDZ                     = cms.double(1.)





embedFSRInMuons = cms.EDProducer(
    "MiniAODMuonFSREmbedder",
    src                          = src,
    srcAlt                       = srcAlt,
    srcVeto                      = srcVeto,
    srcVtx                       = srcVtx,
    label                        = label,
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
    electronPt                   = electronPt,
    electronMaxEta               = electronMaxEta,
    electronSIP                  = electronSIP,
    electronPVDXY                = electronPVDXY,
    electronPVDZ                 = electronPVDZ,
    electronIDPtThr              = electronIDPtThr,
    electronIDEtaThrLow          = electronIDEtaThrLow,
    electronIDEtaThrHigh         = electronIDEtaThrHigh,
    electronIDCutLowPtLowEta     = electronIDCutLowPtLowEta,
    electronIDCutLowPtMedEta     = electronIDCutLowPtMedEta,
    electronIDCutLowPtHighEta    = electronIDCutLowPtHighEta,
    electronIDCutHighPtLowEta    = electronIDCutHighPtLowEta,
    electronIDCutHighPtMedEta    = electronIDCutHighPtMedEta,
    electronIDCutHighPtHighEta   = electronIDCutHighPtHighEta,
    electronIDLabel              = electronIDLabel,
    muonPt                       = muonPt,
    muonMaxEta                   = muonMaxEta,
    muonSIP                      = muonSIP,
    muonPVDXY                    = muonPVDXY,
    muonPVDZ                     = muonPVDZ,
)


embedFSRInElectrons = cms.EDProducer(
    "MiniAODElectronFSREmbedder",
    src                          = src,
    srcAlt                       = srcAlt,
    srcVeto                      = srcVeto,
    srcVtx                       = srcVtx,
    label                        = label,
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
    electronPt                   = electronPt,
    electronMaxEta               = electronMaxEta,
    electronSIP                  = electronSIP,
    electronPVDXY                = electronPVDXY,
    electronPVDZ                 = electronPVDZ,
    electronIDPtThr              = electronIDPtThr,
    electronIDEtaThrLow          = electronIDEtaThrLow,
    electronIDEtaThrHigh         = electronIDEtaThrHigh,
    electronIDCutLowPtLowEta     = electronIDCutLowPtLowEta,
    electronIDCutLowPtMedEta     = electronIDCutLowPtMedEta,
    electronIDCutLowPtHighEta    = electronIDCutLowPtHighEta,
    electronIDCutHighPtLowEta    = electronIDCutHighPtLowEta,
    electronIDCutHighPtMedEta    = electronIDCutHighPtMedEta,
    electronIDCutHighPtHighEta   = electronIDCutHighPtHighEta,
    electronIDLabel              = electronIDLabel,
    muonPt                       = muonPt,
    muonMaxEta                   = muonMaxEta,
    muonSIP                      = muonSIP,
    muonPVDXY                    = muonPVDXY,
    muonPVDZ                     = muonPVDZ,
)


