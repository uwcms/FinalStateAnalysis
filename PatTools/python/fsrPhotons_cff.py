#shamelessly taken from http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/UserCode/Mangano/WWAnalysis/Tools/python/fsrPhotons_cff.py?revision=1.2&view=markup

import FWCore.ParameterSet.Config as cms

## PF Photons
fsrPhotonCands = cms.EDProducer(
    "FSRPhotonProducer",
    src = cms.InputTag("particleFlow")
)

# http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/UserCode/Mangano/WWAnalysis/Tools/python/fsrPhotons_cff.py?revision=1.2&view=markup

## vetos as per muons
fsrPhotonPFIsoChHad04 = cms.EDProducer(
    "LeptonPFIsoFromStep1",
    leptonLabel = cms.InputTag("fsrPhotonCands"),
    pfLabel     = cms.InputTag("pfNoPileUpIso"),
    pfSelection = cms.string("charge != 0 && abs(pdgId) == 211"), # neutral hadrons
    deltaR     = cms.double(0.4), # radius
    deltaRself = cms.double(0.0001), # self-veto 0.0001
    vetoConeEndcaps = cms.double(0.0), # no special veto in the endcaps
    directional = cms.bool(False),
)
# Separate version with Patrick's threshold
fsrPhotonPFIsoChHad04pt02 = fsrPhotonPFIsoChHad04.clone(
    pfSelection = fsrPhotonPFIsoChHad04.pfSelection.value() + " && pt > 0.2"
)
fsrPhotonPFIsoNHad04 = fsrPhotonPFIsoChHad04.clone(
    pfSelection = "charge == 0 && abs(pdgId) == 130 && pt > 0.5", # neutral hadrons
    deltaRself  = 0.01, # larger veto cone for neutrals
)
fsrPhotonPFIsoPhoton04 = fsrPhotonPFIsoChHad04.clone(
    pfSelection = "charge == 0 && abs(pdgId) == 22 && pt > 0.5", # photons
    deltaRself  = 0.01, # larger veto cone for neutrals
)
# for deltaBeta corrections
fsrPhotonPFIsoChHadPU04 = fsrPhotonPFIsoChHad04.clone(pfLabel = 'pfPileUpIso')
fsrPhotonPFIsoChHadPU04pt02 = fsrPhotonPFIsoChHad04pt02.clone(pfLabel = 'pfPileUpIso')

## deltaR = 0.3 copy
fsrPhotonPFIsoChHad03       = fsrPhotonPFIsoChHad04.clone(deltaR = 0.3)
fsrPhotonPFIsoChHad03pt02   = fsrPhotonPFIsoChHad04pt02.clone(deltaR = 0.3)
fsrPhotonPFIsoNHad03        = fsrPhotonPFIsoNHad04.clone(deltaR = 0.3)
fsrPhotonPFIsoPhoton03      = fsrPhotonPFIsoPhoton04.clone(deltaR = 0.3)
fsrPhotonPFIsoChHadPU03     = fsrPhotonPFIsoChHadPU04.clone(deltaR = 0.3)
fsrPhotonPFIsoChHadPU03pt02 = fsrPhotonPFIsoChHadPU04pt02.clone(deltaR = 0.3)


boostedFsrPhotons = cms.EDProducer("PATPFParticleProducerUser",
    # General configurables
    pfCandidateSource = cms.InputTag("fsrPhotonCands"),

    # MC matching configurables
    addGenMatch = cms.bool(False),
    genParticleMatch = cms.InputTag(""),   ## particles source to be used for the MC matching
    ## must be an InputTag or VInputTag to a product of
    ## type edm::Association<reco::GenParticleCollection>
    embedGenMatch = cms.bool(False),       ## embed gen match inside the object instead of storing the ref

    # add user data
    userData = cms.PSet(
        # add custom classes here
        userClasses = cms.PSet(
            src = cms.VInputTag('')
            ),
        # add doubles here
        userFloats = cms.PSet(
            src = cms.VInputTag('')
            ),
        # add ints here
        userInts = cms.PSet(
            src = cms.VInputTag('')
            ),
        # add candidate ptrs here
        userCands = cms.PSet(
            src = cms.VInputTag('')
            ),
        # add "inline" functions here
        userFunctions = cms.vstring(),
        userFunctionLabels = cms.vstring()
        ),

    # Efficiencies
    addEfficiencies = cms.bool(False),
    efficiencies    = cms.PSet(),

    # resolution
    addResolutions  = cms.bool(False),
    resolutions     = cms.PSet(),
    )
boostedFsrPhotons.userData.userFloats.src = cms.VInputTag(
    cms.InputTag("fsrPhotonPFIsoChHad04"),
    cms.InputTag("fsrPhotonPFIsoChHad04pt02"),
    cms.InputTag("fsrPhotonPFIsoNHad04"),
    cms.InputTag("fsrPhotonPFIsoPhoton04"),
    cms.InputTag("fsrPhotonPFIsoChHadPU04"),
    cms.InputTag("fsrPhotonPFIsoChHadPU04pt02"),
    cms.InputTag("fsrPhotonPFIsoChHad03"),
    cms.InputTag("fsrPhotonPFIsoChHad03pt02"),
    cms.InputTag("fsrPhotonPFIsoNHad03"),
    cms.InputTag("fsrPhotonPFIsoPhoton03"),
    cms.InputTag("fsrPhotonPFIsoChHadPU03"),
    cms.InputTag("fsrPhotonPFIsoChHadPU03pt02"),
)

fsrPhotonSequence = cms.Sequence(
    fsrPhotonCands +
    fsrPhotonPFIsoChHad04 +
    fsrPhotonPFIsoChHad04pt02 +
    fsrPhotonPFIsoNHad04 +
    fsrPhotonPFIsoPhoton04 +
    fsrPhotonPFIsoChHadPU04 +
    fsrPhotonPFIsoChHadPU04pt02 +
    fsrPhotonPFIsoChHad03 +
    fsrPhotonPFIsoChHad03pt02 +
    fsrPhotonPFIsoNHad03 +
    fsrPhotonPFIsoPhoton03 +
    fsrPhotonPFIsoChHadPU03 +
    fsrPhotonPFIsoChHadPU03pt02 +
    boostedFsrPhotons
)
