
'''

Ntuple branch template sets for tau objects.

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Muon
i.e. daughter(1) or somesuch.

Author: Evan K. Friis

'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

info = PSet(
    objectGenDecayMode = '{object}.userInt("genDecayMode")',  # how can this be working?
    objectLeadTrackPt = '{object}.userFloat("ps_ldTrkPt")',
    objectDecayMode = '{object}.decayMode',
    objectTNPId = '{object}.userInt("ps_sel_nom")',
)


# ID and isolation
id = PSet(
    # updated for what is included in miniaodv2
    # Against Electron
    objectAgainstElectronVLooseMVA5 = '{object}.tauID("againstElectronVLooseMVA5")', 
    objectAgainstElectronLooseMVA5  = '{object}.tauID("againstElectronLooseMVA5")',
    objectAgainstElectronMediumMVA5 = '{object}.tauID("againstElectronMediumMVA5")',
    objectAgainstElectronTightMVA5  = '{object}.tauID("againstElectronTightMVA5")',
    objectAgainstElectronVTightMVA5 = '{object}.tauID("againstElectronVTightMVA5")',
    
    objectAgainstElectronMVA5category = '{object}.tauID("againstElectronMVA5category")',
    objectAgainstElectronMVA5raw      = '{object}.tauID("againstElectronMVA5raw")',

    # Against Muon
    objectAgainstMuonLoose3 = '{object}.tauID("againstMuonLoose3")',
    objectAgainstMuonTight3 = '{object}.tauID("againstMuonTight3")',
    
    # combined isolation DB corr 3 hits
    objectByLooseCombinedIsolationDeltaBetaCorr3Hits = '{object}.tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits")',
    objectByMediumCombinedIsolationDeltaBetaCorr3Hits = '{object}.tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits")', 
    objectByTightCombinedIsolationDeltaBetaCorr3Hits = '{object}.tauID("byTightCombinedIsolationDeltaBetaCorr3Hits")',
    objectByCombinedIsolationDeltaBetaCorrRaw3Hits = '{object}.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")',
    
    # BDT based tau ID discriminator based on isolation Pt sums plus tau lifetime information, trained on 1-prong, "2-prong" and 3-prong tau candidates 
    objectByVLooseIsolationMVA3newDMwLT = '{object}.tauID("byVLooseIsolationMVA3newDMwLT")',
    objectByLooseIsolationMVA3newDMwLT = '{object}.tauID("byLooseIsolationMVA3newDMwLT")',
    objectByMediumIsolationMVA3newDMwLT = '{object}.tauID("byMediumIsolationMVA3newDMwLT")', 
    objectByTightIsolationMVA3newDMwLT = '{object}.tauID("byTightIsolationMVA3newDMwLT")',
    objectByVTightIsolationMVA3newDMwLT = '{object}.tauID("byVTightIsolationMVA3newDMwLT")', 
    objectByVVTightIsolationMVA3newDMwLT = '{object}.tauID("byVVTightIsolationMVA3newDMwLT")', 
    objectByIsolationMVA3newDMwLTraw = '{object}.tauID("byIsolationMVA3newDMwLTraw")',
    
    # BDT based tau ID discriminator based on isolation Pt sums plus tau lifetime information, trained on 1-prong and 3-prong tau candidates 
    objectByVLooseIsolationMVA3oldDMwLT = '{object}.tauID("byVLooseIsolationMVA3oldDMwLT")', 
    objectByLooseIsolationMVA3oldDMwLT = '{object}.tauID("byLooseIsolationMVA3oldDMwLT")', 
    objectByMediumIsolationMVA3oldDMwLT = '{object}.tauID("byMediumIsolationMVA3oldDMwLT")', 
    objectByTightIsolationMVA3oldDMwLT = '{object}.tauID("byTightIsolationMVA3oldDMwLT")', 
    objectByVTightIsolationMVA3oldDMwLT = '{object}.tauID("byVTightIsolationMVA3oldDMwLT")', 
    objectByVVTightIsolationMVA3oldDMwLT = '{object}.tauID("byVVTightIsolationMVA3oldDMwLT")',
    objectByIsolationMVA3oldDMwLTraw = '{object}.tauID("byIsolationMVA3oldDMwLTraw")', 
    
#    objectByPileupWeightedIsolationRaw3Hits = '{object}.tauID("byPileupWeightedIsolationRaw3Hits")',
#    objectByLoosePileupWeightedIsolation3Hits = '{object}.tauID("byLoosePileupWeightedIsolation3Hits")',
#    objectByMediumPileupWeightedIsolation3Hits = '{object}.tauID("byMediumPileupWeightedIsolation3Hits")',
#    objectByTightPileupWeightedIsolation3Hits = '{object}.tauID("byTightPileupWeightedIsolation3Hits")',
#    objectByPhotonPtSumOutsideSignalCone = '{object}.tauID("byPhotonPtSumOutsideSignalCone")',
#    objectPhotonPtSumOutsideSignalCone = '{object}.tauID("photonPtSumOutsideSignalCone")',

    # DecayModeFinding
    objectDecayModeFinding       = '{object}.tauID("decayModeFinding")',
    objectDecayModeFindingNewDMs = '{object}.tauID("decayModeFindingNewDMs")',

#    objectFootprintCorrection = '{object}.tauID("footprintCorrection")',
#    objectNeutralIsoPtSum = '{object}.tauID("neutralIsoPtSum")',
#    objectNeutralIsoPtSumWeight = '{object}.tauID("neutralIsoPtSumWeight")',
#    objectChargedIsoPtSum = '{object}.tauID("chargedIsoPtSum")',
#    objectPuCorrPtSum     = '{object}.tauID("puCorrPtSum")',
    # closest Z mass
    objectNearestZMass = 'closestZTau({object_idx},"")',
    # lowest invariant mass
    objectLowestMll = 'smallestMtt({object_idx},"")',

    objectGenEnergy      = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).energy() : -999',
    objectGenPt          = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).pt() : -999',
    objectGenPx          = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).px() : -999',
    objectGenPy          = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).py() : -999',
    objectGenPz          = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).pz() : -999',
    objectGenEta         = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).eta() : -999',
    objectGenPhi         = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).phi() : -999',

    objectGenMotherPdgId = '? (getDaughterGenParticleMotherSmart({object_idx}, 15, 0).isAvailable && getDaughterGenParticleMotherSmart({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticleMotherSmart({object_idx}, 15, 0).pdgId() : -999',

    objectGenMotherPt =  '? (getDaughterGenParticleMotherSmart({object_idx}, 15, 0).isAvailable && getDaughterGenParticleMotherSmart({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticleMotherSmart({object_idx}, 15, 0).pt() : -999', 
    objectGenMotherEnergy =  '? (getDaughterGenParticleMotherSmart({object_idx}, 15, 0).isAvailable && getDaughterGenParticleMotherSmart({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticleMotherSmart({object_idx}, 15, 0).energy() : -999', 
    objectGenMotherEta =  '? (getDaughterGenParticleMotherSmart({object_idx}, 15, 0).isAvailable && getDaughterGenParticleMotherSmart({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticleMotherSmart({object_idx}, 15, 0).eta() : -999', 
    objectGenMotherPhi =  '? (getDaughterGenParticleMotherSmart({object_idx}, 15, 0).isAvailable && getDaughterGenParticleMotherSmart({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticleMotherSmart({object_idx}, 15, 0).phi() : -999', 

    objectComesFromHiggs = 'comesFromHiggs({object_idx}, 15, 1)',
    objectGenPdgId       = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).pdgId() : -999',
    objectGenCharge      = '? (getDaughterGenParticle({object_idx}, 15, 0).isAvailable && getDaughterGenParticle({object_idx}, 15, 0).isNonnull) ? getDaughterGenParticle({object_idx}, 15, 0).charge() : -999',



)


