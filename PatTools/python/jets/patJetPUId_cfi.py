'''

Algorithms to identify jets coming from PU.

See: https://twiki.cern.ch/twiki/bin/view/CMS/PileupJetID

'''

import FWCore.ParameterSet.Config as cms
import sys

try:
    from RecoJets.JetProducers.PileupJetID_cfi import pileupJetIdProducer
    # The path to the residuals must exist, even if we don't use it.
    pileupJetIdProducer.residualsTxt = \
        "FinalStateAnalysis/PatTools/data/readme.txt"
except ImportError:
    sys.stderr.write(__file__ +
                     ": PU Jet ID dependency not installed, will not run!\n")

# Module to embed the IDs
patJetsPUID = cms.EDProducer(
    "PATJetPUIDEmbedder",
    src=cms.InputTag('fixme'),
    discriminants=cms.VInputTag(
        cms.InputTag("pileupJetIdProducer", "fullDiscriminant"),
        cms.InputTag("pileupJetIdProducer", "cutbasedDiscriminant"),
        #cms.InputTag("pileupJetIdProducer", "simpleDiscriminant"),
    ),
    ids=cms.VInputTag(
        cms.InputTag("pileupJetIdProducer", "fullId"),
        cms.InputTag("pileupJetIdProducer", "cutbasedId"),
        #cms.InputTag("pileupJetIdProducer", "simpleId"),
    )
)
