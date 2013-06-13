'''

Algorithms to identify jets coming from PU.

See: https://twiki.cern.ch/twiki/bin/view/CMS/PileupJetID

'''

import FWCore.ParameterSet.Config as cms
import sys

from RecoJets.JetProducers.PileupJetID_cfi import pileupJetIdProducer
# The path to the residuals must exist, even if we don't use it.
pileupJetIdProducer.residualsTxt = \
        "FinalStateAnalysis/PatTools/data/readme.txt"

# Module to embed the IDs
patJetsPUID = cms.EDProducer(
    "PATJetPUIDEmbedder",
    src=cms.InputTag('fixme'),
    discriminants=cms.VInputTag(),
    ids=cms.VInputTag()
)

for algo in pileupJetIdProducer.algos:
    label = algo.label.value()
    patJetsPUID.discriminants.append(cms.InputTag(
        "pileupJetIdProducer", label + "Discriminant"))
    patJetsPUID.ids.append(cms.InputTag(
        "pileupJetIdProducer", label + "Id"))
