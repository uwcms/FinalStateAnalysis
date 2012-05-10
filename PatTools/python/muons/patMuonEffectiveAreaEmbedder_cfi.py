'''

Embeds the "Effective Area" into pat::Muons

See: Muon/MuonAnalysisTools/interface/MuonEffectiveArea.h

Slides about the method:

https://indico.cern.ch/getFile.py/access?contribId=1&resId=0&materialId=slides&confId=188494

'''

import FWCore.ParameterSet.Config as cms

patMuonEffectiveAreaEmbedder = cms.EDProducer(
    "PATMuonEffectiveAreaEmbedder",
    src = cms.InputTag('fixme'),
    # Available targets: Fal11MC, Summer11MC, 2011Data, 2012Data
    target = cms.string('fixme'),
)
