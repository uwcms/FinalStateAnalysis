'''

Algorithms to identify jets coming from PU.

See: https://twiki.cern.ch/twiki/bin/view/CMS/PileupJetID

'''

import FWCore.ParameterSet.Config as cms
import sys

from RecoJets.JetProducers.PileupJetID_cfi import pileupJetIdProducer
# The path to the residuals must exist, even if we don't use it.
pileupJetIdProducer.residualsTxt = \
        cms.FileInPath("FinalStateAnalysis/PatTools/data/readme.txt")
pileupJetIdProducer.jets = cms.InputTag("ak5PFJets")
pileupJetIdProducer.applyJec = cms.bool(True)

# Module to embed the IDs
patJetsPUID = cms.EDProducer(
    "PATJetPUIDEmbedder",
    src=cms.InputTag('patJets'),
    discriminants=cms.VInputTag(),
    ids=cms.VInputTag()
)

for algo in pileupJetIdProducer.algos:
    label = algo.label.value()
    patJetsPUID.discriminants.append(cms.InputTag(
        "pileupJetIdProducer", label + "Discriminant"))
    patJetsPUID.ids.append(cms.InputTag(
        "pileupJetIdProducer", label + "Id"))

# Embed loose medium and tight official PFJet IDs into pat::Jets
# (see https://twiki.cern.ch/twiki/bin/view/CMS/JetID)
patJetId = cms.EDProducer(
    "PATJetIdEmbedder",
    src = cms.InputTag('patJetsPUID')
)
