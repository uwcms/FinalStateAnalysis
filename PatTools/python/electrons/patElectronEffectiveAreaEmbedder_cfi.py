'''

Embeds the "Effective Area" into pat::Electrons

See: EGamma/EGammaAnalysisTools/interface/EGammaCutBasedEleId.h

Slides about the method:

https://indico.cern.ch/getFile.py/access?contribId=1&resId=0&materialId=slides&confId=188494

'''

import FWCore.ParameterSet.Config as cms

patElectronEffectiveAreaEmbedder = cms.EDProducer(
    "PATElectronEffectiveAreaEmbedder",
    src = cms.InputTag('fixme'),
    # Available targets: Fal11MC, Summer11MC, 2011Data, 2012Data
    target = cms.string('fixme'),
)
