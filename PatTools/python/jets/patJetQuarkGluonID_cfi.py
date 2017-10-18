'''

Algorithms to identify jets as quark or gluon jet.

See: https://twiki.cern.ch/twiki/bin/viewauth/CMS/GluonTag

'''

import FWCore.ParameterSet.Config as cms
import sys

try:
    from QuarkGluonTagger.EightTeV.QGTagger_RecoJets_cff import *
except ImportError:
    sys.stderr.write(__file__ +
                     ": Gluon Jet ID dependency not installed, will not run!\n")

QGTagger.srcJets  = cms.InputTag('fixme')
QGTagger.isPatJet = cms.untracked.bool(True) 
QGTagger.jec      = cms.untracked.string('')

# Module to embed the IDs
patJetsQGID = cms.EDProducer(
    "PATJetValueMapEmbedder",
    src  =cms.InputTag('fixme'),
    maps =cms.VPSet(
        cms.PSet(
            src   = cms.InputTag('QGTagger','qgMLP'),
            label = cms.string('QuarkGluonMVAID'),
            ),
        cms.PSet(
            src   = cms.InputTag('QGTagger','qgLikelihood'),
            label = cms.string('QuarkGluonLikelihoodID'),
            ),
        ),
)

embedQGJetID = cms.Sequence(
    QuarkGluonTagger *
    patJetsQGID
    )
