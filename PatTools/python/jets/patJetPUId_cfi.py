'''

Algorithms to identify jets coming from PU.

See: https://twiki.cern.ch/twiki/bin/view/CMS/PileupJetID

NB that you must change the "jets" input tag for puJetId and puJetMVA
to point to the correct collection!

External sequence name: puJetIdSequence

The embedded pat::Jets are produced w/ label: patJetsPUID

'''

import FWCore.ParameterSet.Config as cms
import sys

try:
    from CMGTools.External.pujetidsequence_cff import \
            puJetIdSqeuence, puJetId, puJetMva # sic
except ImportError:
    sys.stderr.write(__file__ +
                     ": PU Jet ID dependency not installed, will not be run!\n")

# Module to embed the IDs
patJetsPUID = cms.EDProducer(
    "PATJetPUIDEmbedder",
    src = cms.InputTag('fixme'),
    discriminants = cms.VInputTag(
        cms.InputTag("puJetMva", "fullDiscriminant"),
        cms.InputTag("puJetMva", "cutbasedDiscriminant"),
        cms.InputTag("puJetMva", "simpleDiscriminant"),
    ),
    ids = cms.VInputTag(
        cms.InputTag("puJetMva", "fullId"),
        cms.InputTag("puJetMva", "cutbasedId"),
        cms.InputTag("puJetMva", "simpleId"),
    )
)
