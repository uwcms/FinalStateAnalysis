###################################################################################################################
###    miniAOD_fsrPhotons_cff.py                                                                                ###
###    Copied from https://github.com/VBF-HZZ/UFHZZAnalysisRun2/blob/csa14/FSRPhotons/python/fsrPhotons_cff.py  ###
###          I take no credit for it                                                                            ###
###################################################################################################################

import FWCore.ParameterSet.Config as cms

## PF Photons
fsrPhotons = cms.EDProducer("MiniAODFSRPhotonProducer",
    srcCands = cms.InputTag("packedPFCandidates"),
    muons = cms.InputTag("slimmedMuons"), 
    ptThresh = cms.double(1.0), ## will tighten to 2 at analysis level
    extractMuonFSR = cms.bool(False),
)

## vetos as per muons 
fsrPhotonPFIsoChHad04 = cms.EDProducer("PhotonPFIsoCalculator",
    photonLabel = cms.InputTag("fsrPhotons"),
    pfLabel     = cms.InputTag("packedPFCandidates"), 
    pfSelection = cms.string("charge != 0 && abs(pdgId) == 211 && (!fromPV) "), # charged hadrons
    deltaR     = cms.double(0.4), # radius
    deltaRself = cms.double(0.0001), # self-veto 0.0001
    vetoConeEndcaps = cms.double(0.0), # no special veto in the endcaps
    directional = cms.bool(False),
    debug       = cms.untracked.bool(False)
)
# Separate version with Patrick's threshold
fsrPhotonPFIsoChHad04pt02 = fsrPhotonPFIsoChHad04.clone(
    pfSelection = cms.string("charge != 0 && abs(pdgId) == 211 && (!fromPV) && pt>0.2")
)
fsrPhotonPFIsoNHad04 = fsrPhotonPFIsoChHad04.clone(
    pfSelection = cms.string("charge==0 && abs(pdgId)==130 && (!fromPV) && pt>0.5"), # neutral hadrons
    deltaRself  = 0.01, # larger veto cone for neutrals
)
fsrPhotonPFIsoPhoton04 = fsrPhotonPFIsoChHad04.clone(
    pfSelection = cms.string("charge==0 && abs(pdgId)==22 && (!fromPV) && pt>0.5"), # photons
    deltaRself  = 0.01, # larger veto cone for neutrals
)
# for deltaBeta corrections
fsrPhotonPFIsoChHadPU04 = fsrPhotonPFIsoChHad04.clone(
    pfSelection = cms.string("charge!=0 && abs(pdgId)==211 && (fromPV) ") # charged hadrons 
)
fsrPhotonPFIsoChHadPU04pt02 = fsrPhotonPFIsoChHad04.clone(
    pfSelection = cms.string("charge!=0 && abs(pdgId)==211 && (fromPV) && pt>0.2")
)

## deltaR = 0.3 copy
fsrPhotonPFIsoChHad03       = fsrPhotonPFIsoChHad04.clone(deltaR = 0.3)
fsrPhotonPFIsoChHad03pt02   = fsrPhotonPFIsoChHad04pt02.clone(deltaR = 0.3)
fsrPhotonPFIsoNHad03        = fsrPhotonPFIsoNHad04.clone(deltaR = 0.3)
fsrPhotonPFIsoPhoton03      = fsrPhotonPFIsoPhoton04.clone(deltaR = 0.3)
fsrPhotonPFIsoChHadPU03     = fsrPhotonPFIsoChHadPU04.clone(deltaR = 0.3)
fsrPhotonPFIsoChHadPU03pt02 = fsrPhotonPFIsoChHadPU04pt02.clone(deltaR = 0.3)



# fsrPhotonPFIsoChHad03pt02 + fsrPhotonPFIsoChHadPU03pt02
fsrPhotonPFIsoChHadPUNoPU03pt02 = cms.EDProducer("PhotonPFIsoCalculator",
    photonLabel = cms.InputTag("fsrPhotons"),
    pfLabel     = cms.InputTag("packedPFCandidates"),
    pfSelection = cms.string("charge!=0 && abs(pdgId)==211 && pt>0.2"),
    deltaR = cms.double(0.3),
    deltaRself = cms.double(0.0001),
    vetoConeEndcaps = cms.double(0.0),
    directional = cms.bool(False),
    debug       = cms.untracked.bool(False)
)

# fsrPhotonPFIsoNHad03 + fsrPhotonPFIsoPhoton03
fsrPhotonPFIsoNHadPhoton03 = cms.EDProducer("PhotonPFIsoCalculator",
    photonLabel = cms.InputTag("fsrPhotons"),
    pfLabel     = cms.InputTag("packedPFCandidates"),
    pfSelection = cms.string("charge==0 && (abs(pdgId)==22||abs(pdgId)==130) && pt>0.5"), 
    deltaR = cms.double(0.3),
    deltaRself  = cms.double(0.01),
    vetoConeEndcaps = cms.double(0.0),
    directional = cms.bool(False),
    debug       = cms.untracked.bool(False) 
)

import PhysicsTools.PatAlgos.producersLayer1.pfParticleProducer_cfi 
boostedFsrPhotons = PhysicsTools.PatAlgos.producersLayer1.pfParticleProducer_cfi.patPFParticles.clone(
    pfCandidateSource = 'fsrPhotons'
)
boostedFsrPhotons.userData.userFloats.src = cms.VInputTag(
    #cms.InputTag("fsrPhotonPFIsoChHad04"),
    #cms.InputTag("fsrPhotonPFIsoChHad04pt02"),
    #cms.InputTag("fsrPhotonPFIsoNHad04"),
    #cms.InputTag("fsrPhotonPFIsoPhoton04"),
    #cms.InputTag("fsrPhotonPFIsoChHadPU04"),
    #cms.InputTag("fsrPhotonPFIsoChHadPU04pt02"),
    #cms.InputTag("fsrPhotonPFIsoChHad03"),
    ##cms.InputTag("fsrPhotonPFIsoChHad03pt02"),
    ##cms.InputTag("fsrPhotonPFIsoNHad03"),
    ##cms.InputTag("fsrPhotonPFIsoPhoton03"),
    #cms.InputTag("fsrPhotonPFIsoChHadPU03"),
    ##cms.InputTag("fsrPhotonPFIsoChHadPU03pt02"),
    cms.InputTag("fsrPhotonPFIsoChHadPUNoPU03pt02"),
    cms.InputTag("fsrPhotonPFIsoNHadPhoton03")
)

fsrPhotonSequence = cms.Sequence(
    fsrPhotons 
    +
    #fsrPhotonPFIsoChHad04 + 
    #fsrPhotonPFIsoChHad04pt02 + 
    #fsrPhotonPFIsoNHad04 + 
    #fsrPhotonPFIsoPhoton04 + 
    #fsrPhotonPFIsoChHadPU04 + 
    #fsrPhotonPFIsoChHadPU04pt02 + 
    #fsrPhotonPFIsoChHad03 + 
    ##fsrPhotonPFIsoChHad03pt02 + 
    ##fsrPhotonPFIsoNHad03 + 
    ##fsrPhotonPFIsoPhoton03 + 
    #fsrPhotonPFIsoChHadPU03 + 
    ##fsrPhotonPFIsoChHadPU03pt02 + 
    fsrPhotonPFIsoChHadPUNoPU03pt02 +
    fsrPhotonPFIsoNHadPhoton03 +
    boostedFsrPhotons
)

