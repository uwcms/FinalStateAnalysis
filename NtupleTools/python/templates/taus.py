
'''

Ntuple branch template sets for tau objects.

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Muon
i.e. daughter(1) or somesuch.

Author: Evan K. Friis

'''

from FinalStateAnalysis.Utilities.cfgtools import PSet

info = PSet(
    objectGenDecayMode = '{object}.userInt("genDecayMode")',  
    objectLeadTrackPt = '{object}.leadCand().pt()',
    objectDecayMode = '{object}.decayMode',
    #objectTNPId = '{object}.userInt("ps_sel_nom")',
    objectNSignalCands = '{object}.signalCands().size()',
    objectNChrgHadrSignalCands = '{object}.signalChargedHadrCands().size()',
    objectNGammaSignalCands = '{object}.signalGammaCands().size()',
    objectNNeutralHadrSignalCands = '{object}.signalNeutrHadrCands().size()',
)


# ID and isolation
id = PSet(
    # updated for what is included in miniaodv2
    # Against Electron
#    objectAgainstElectronVLooseMVA5 = '{object}.tauID("againstElectronVLooseMVA5")', 
  #  objectAgainstElectronLooseMVA5  = '{object}.tauID("againstElectronLooseMVA5")',
#    objectAgainstElectronMediumMVA5 = '{object}.tauID("againstElectronMediumMVA5")',
#    objectAgainstElectronTightMVA5  = '{object}.tauID("againstElectronTightMVA5")',
#    objectAgainstElectronVTightMVA5 = '{object}.tauID("againstElectronVTightMVA5")',

    objectAgainstElectronVLooseMVA6 = '{object}.tauID("againstElectronVLooseMVA6")', 
    objectAgainstElectronLooseMVA6  = '{object}.tauID("againstElectronLooseMVA6")',
    objectAgainstElectronMediumMVA6 = '{object}.tauID("againstElectronMediumMVA6")',
    objectAgainstElectronTightMVA6  = '{object}.tauID("againstElectronTightMVA6")',
    objectAgainstElectronVTightMVA6 = '{object}.tauID("againstElectronVTightMVA6")',
    
    objectAgainstElectronMVA6category = '{object}.tauID("againstElectronMVA6category")',
#    objectAgainstElectronMVA5category = '{object}.tauID("againstElectronMVA5category")',
#    objectAgainstElectronMVA5raw      = '{object}.tauID("againstElectronMVA5raw")',
    objectAgainstElectronMVA6Raw      = '{object}.tauID("againstElectronMVA6Raw")',
  #  objectAgainstElectronMVA6Raw='{object}.tauID("againstElectronMVA6raw")' 
    # Against Muon
    objectAgainstMuonLoose3 = '{object}.tauID("againstMuonLoose3")',
    objectAgainstMuonTight3 = '{object}.tauID("againstMuonTight3")',
    

    #  PileupWeighted cut-based isolation discriminators
#    objectByLoosePileupWeightedIsolation3Hits = '{object}.tauID("byLoosePileupWeightedIsolation3Hits")',#mark
#    objectByMediumPileupWeightedIsolation3Hits = '{object}.tauID("byMediumPileupWeightedIsolation3Hits")', #mark
#    objectByTightPileupWeightedIsolation3Hits = '{object}.tauID("byTightPileupWeightedIsolation3Hits")',#mark
    # And the raw values of the isolation:
#    objectByPileupWeightedIsolationRaw3Hits = '{object}.tauID("byPileupWeightedIsolationRaw3Hits")',#mark
    objectNeutralIsoPtSumWeight = '{object}.tauID("neutralIsoPtSumWeight")',
    objectNeutralIsoPtSumWeightdR03 = '{object}.tauID("neutralIsoPtSumWeightdR03")',
    objectFootprintCorrection = '{object}.tauID("footprintCorrection")',
    objectFootprintCorrectiondR03 = '{object}.tauID("footprintCorrectiondR03")',
    objectByPhotonPtSumOutsideSignalCone = '{object}.tauID("byPhotonPtSumOutsideSignalCone")',
    objectPhotonPtSumOutsideSignalCone = '{object}.tauID("photonPtSumOutsideSignalCone")',
    objectPhotonPtSumOutsideSignalConedR03 = '{object}.tauID("photonPtSumOutsideSignalConedR03")',

    objectNeutralIsoPtSum = '{object}.tauID("neutralIsoPtSum")',
    objectNeutralIsoPtSumdR03 = '{object}.tauID("neutralIsoPtSumdR03")',
    objectChargedIsoPtSum = '{object}.tauID("chargedIsoPtSum")',
    objectChargedIsoPtSumdR03 = '{object}.tauID("chargedIsoPtSumdR03")',
    objectPuCorrPtSum     = '{object}.tauID("puCorrPtSum")',


    # combined isolation DB corr 3 hits
    objectByLooseCombinedIsolationDeltaBetaCorr3Hits = '{object}.tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits")',
    objectByMediumCombinedIsolationDeltaBetaCorr3Hits = '{object}.tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits")', 
    objectByTightCombinedIsolationDeltaBetaCorr3Hits = '{object}.tauID("byTightCombinedIsolationDeltaBetaCorr3Hits")',
    objectByCombinedIsolationDeltaBetaCorrRaw3Hits = '{object}.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")',
    # New Tau Isolation Discriminators with cone size DeltaR = 0.3 7_6_x
#    objectByLooseCombinedIsolationDeltaBetaCorr3HitsdR03 = '{object}.tauID("byLooseCombinedIsolationDeltaBetaCorr3HitsdR03")',#real
#    objectByMediumCombinedIsolationDeltaBetaCorr3HitsdR03 = '{object}.tauID("byMediumCombinedIsolationDeltaBetaCorr3HitsdR03")', 
#    objectByTightCombinedIsolationDeltaBetaCorr3HitsdR03 = '{object}.tauID("byTightCombinedIsolationDeltaBetaCorr3HitsdR03")',###here
    
    # BDT based tau ID discriminator based on isolation Pt sums plus tau lifetime information, trained on 1-prong, "2-prong" and 3-prong tau candidates 
#    objectByVLooseIsolationMVA3newDMwLT = '{object}.tauID("byVLooseIsolationMVA3newDMwLT")',
#    objectByLooseIsolationMVA3newDMwLT = '{object}.tauID("byLooseIsolationMVA3newDMwLT")',
#    objectByMediumIsolationMVA3newDMwLT = '{object}.tauID("byMediumIsolationMVA3newDMwLT")', 
#    objectByTightIsolationMVA3newDMwLT = '{object}.tauID("byTightIsolationMVA3newDMwLT")',
#    objectByVTightIsolationMVA3newDMwLT = '{object}.tauID("byVTightIsolationMVA3newDMwLT")', 
#    objectByVVTightIsolationMVA3newDMwLT = '{object}.tauID("byVVTightIsolationMVA3newDMwLT")', 
#    objectByIsolationMVA3newDMwLTraw = '{object}.tauID("byIsolationMVA3newDMwLTraw")',
    
    # BDT based tau ID discriminator based on isolation Pt sums plus tau lifetime information, trained on 1-prong and 3-prong tau candidates 
#    objectByVLooseIsolationMVA3oldDMwLT = '{object}.tauID("byVLooseIsolationMVA3oldDMwLT")',#mark 
#    objectByLooseIsolationMVA3oldDMwLT = '{object}.tauID("byLooseIsolationMVA3oldDMwLT")',#mark 
#    objectByMediumIsolationMVA3oldDMwLT = '{object}.tauID("byMediumIsolationMVA3oldDMwLT")',#mark 
#    objectByTightIsolationMVA3oldDMwLT = '{object}.tauID("byTightIsolationMVA3oldDMwLT")',#mark 
#    objectByVTightIsolationMVA3oldDMwLT = '{object}.tauID("byVTightIsolationMVA3oldDMwLT")',#mark 
#    objectByVVTightIsolationMVA3oldDMwLT = '{object}.tauID("byVVTightIsolationMVA3oldDMwLT")',#mark
#    objectByIsolationMVA3oldDMwLTraw = '{object}.tauID("byIsolationMVA3oldDMwLTraw")',#real 
    
    # MVA based tau isolation discriminators new 7_6_x
    # With Old Decay Mode reconstruction:
    objectByVLooseIsolationMVArun2v1DBoldDMwLT = '{object}.tauID("byVLooseIsolationMVArun2v1DBoldDMwLT")',
    objectByLooseIsolationMVArun2v1DBoldDMwLT = '{object}.tauID("byLooseIsolationMVArun2v1DBoldDMwLT")',
    objectByMediumIsolationMVArun2v1DBoldDMwLT = '{object}.tauID("byMediumIsolationMVArun2v1DBoldDMwLT")',
    objectByTightIsolationMVArun2v1DBoldDMwLT = '{object}.tauID("byTightIsolationMVArun2v1DBoldDMwLT")',
    objectByVTightIsolationMVArun2v1DBoldDMwLT = '{object}.tauID("byVTightIsolationMVArun2v1DBoldDMwLT")',
    objectByVVTightIsolationMVArun2v1DBoldDMwLT = '{object}.tauID("byVVTightIsolationMVArun2v1DBoldDMwLT")',
    objectByIsolationMVArun2v1DBoldDMwLTraw = '{object}.tauID("byIsolationMVArun2v1DBoldDMwLTraw")',#real 
    # Same but with Iso dR = 0.3
    objectByVLooseIsolationMVArun2v1DBdR03oldDMwLT = '{object}.tauID("byVLooseIsolationMVArun2v1DBdR03oldDMwLT")',
    objectByLooseIsolationMVArun2v1DBdR03oldDMwLT = '{object}.tauID("byLooseIsolationMVArun2v1DBdR03oldDMwLT")',
    objectByMediumIsolationMVArun2v1DBdR03oldDMwLT = '{object}.tauID("byMediumIsolationMVArun2v1DBdR03oldDMwLT")',
    objectByTightIsolationMVArun2v1DBdR03oldDMwLT = '{object}.tauID("byTightIsolationMVArun2v1DBdR03oldDMwLT")',
    objectByVTightIsolationMVArun2v1DBdR03oldDMwLT = '{object}.tauID("byVTightIsolationMVArun2v1DBdR03oldDMwLT")',
    objectByVVTightIsolationMVArun2v1DBdR03oldDMwLT = '{object}.tauID("byVVTightIsolationMVArun2v1DBdR03oldDMwLT")',
    objectByIsolationMVArun2v1DBdR03oldDMwLTraw = '{object}.tauID("byIsolationMVArun2v1DBdR03oldDMwLTraw")',
    
    #With New Decay Mode Reconstruction:
    objectByVLooseIsolationMVArun2v1DBnewDMwLT = '{object}.tauID("byVLooseIsolationMVArun2v1DBnewDMwLT")',
    objectByLooseIsolationMVArun2v1DBnewDMwLT = '{object}.tauID("byLooseIsolationMVArun2v1DBnewDMwLT")',
    objectByMediumIsolationMVArun2v1DBnewDMwLT = '{object}.tauID("byMediumIsolationMVArun2v1DBnewDMwLT")',
    objectByTightIsolationMVArun2v1DBnewDMwLT = '{object}.tauID("byTightIsolationMVArun2v1DBnewDMwLT")',
    objectByVTightIsolationMVArun2v1DBnewDMwLT = '{object}.tauID("byVTightIsolationMVArun2v1DBnewDMwLT")',
    objectByVVTightIsolationMVArun2v1DBnewDMwLT = '{object}.tauID("byVVTightIsolationMVArun2v1DBnewDMwLT")',
    objectByIsolationMVArun2v1DBnewDMwLTraw = '{object}.tauID("byIsolationMVArun2v1DBnewDMwLTraw")',
    
    #MVA tau ID using Pileup Weighted isolation: new 7_6_x
    #With Old Decay Mode reconstruction:
    objectByVLooseIsolationMVArun2v1PWoldDMwLT = '{object}.tauID("byVLooseIsolationMVArun2v1PWoldDMwLT")',
    objectByLooseIsolationMVArun2v1PWoldDMwLT = '{object}.tauID("byLooseIsolationMVArun2v1PWoldDMwLT")',
    objectByMediumIsolationMVArun2v1PWoldDMwLT = '{object}.tauID("byMediumIsolationMVArun2v1PWoldDMwLT")',
    objectByTightIsolationMVArun2v1PWoldDMwLT = '{object}.tauID("byTightIsolationMVArun2v1PWoldDMwLT")',
    objectByVTightIsolationMVArun2v1PWoldDMwLT = '{object}.tauID("byVTightIsolationMVArun2v1PWoldDMwLT")',
    objectByVVTightIsolationMVArun2v1PWoldDMwLT = '{object}.tauID("byVVTightIsolationMVArun2v1PWoldDMwLT")',
    objectByIsolationMVArun2v1PWoldDMwLTraw = '{object}.tauID("byIsolationMVArun2v1PWoldDMwLTraw")',
    #With new  Decay Mode reconstruction:
    objectByVLooseIsolationMVArun2v1PWnewDMwLT = '{object}.tauID("byVLooseIsolationMVArun2v1PWnewDMwLT")',
    objectByLooseIsolationMVArun2v1PWnewDMwLT = '{object}.tauID("byLooseIsolationMVArun2v1PWnewDMwLT")',
    objectByMediumIsolationMVArun2v1PWnewDMwLT = '{object}.tauID("byMediumIsolationMVArun2v1PWnewDMwLT")',
    objectByTightIsolationMVArun2v1PWnewDMwLT = '{object}.tauID("byTightIsolationMVArun2v1PWnewDMwLT")',
    objectByVTightIsolationMVArun2v1PWnewDMwLT = '{object}.tauID("byVTightIsolationMVArun2v1PWnewDMwLT")',
    objectByVVTightIsolationMVArun2v1PWnewDMwLT = '{object}.tauID("byVVTightIsolationMVArun2v1PWnewDMwLT")',
    objectByIsolationMVArun2v1PWnewDMwLTraw = '{object}.tauID("byIsolationMVArun2v1PWnewDMwLTraw")',
    # Same but with Iso dR = 0.3
    objectByVLooseIsolationMVArun2v1PWdR03oldDMwLT = '{object}.tauID("byVLooseIsolationMVArun2v1PWdR03oldDMwLT")',
    objectByLooseIsolationMVArun2v1PWdR03oldDMwLT = '{object}.tauID("byLooseIsolationMVArun2v1PWdR03oldDMwLT")',
    objectByMediumIsolationMVArun2v1PWdR03oldDMwLT = '{object}.tauID("byMediumIsolationMVArun2v1PWdR03oldDMwLT")',
    objectByTightIsolationMVArun2v1PWdR03oldDMwLT = '{object}.tauID("byTightIsolationMVArun2v1PWdR03oldDMwLT")',
    objectByVTightIsolationMVArun2v1PWdR03oldDMwLT = '{object}.tauID("byVTightIsolationMVArun2v1PWdR03oldDMwLT")',
    objectByVVTightIsolationMVArun2v1PWdR03oldDMwLT = '{object}.tauID("byVVTightIsolationMVArun2v1PWdR03oldDMwLT")',
    objectByIsolationMVArun2v1PWdR03oldDMwLTraw = '{object}.tauID("byIsolationMVArun2v1PWdR03oldDMwLTraw")',
    

    # DecayModeFinding
    objectDecayModeFinding       = '{object}.tauID("decayModeFinding")',
    objectDecayModeFindingNewDMs = '{object}.tauID("decayModeFindingNewDMs")',

    # closest Z mass
    objectNearestZMass = 'closestZTau({object_idx},"")',
    # lowest invariant mass
    objectLowestMll = 'smallestMtt({object_idx},"")',

    objectGenMotherPdgId = '? (getDaughterGenParticleMotherSmartRef({object_idx}).isAvailable && getDaughterGenParticleMotherSmartRef({object_idx}).isNonnull) ? getDaughterGenParticleMotherSmartRef({object_idx}).pdgId() : -999',
    objectGenMotherPt =  '? (getDaughterGenParticleMotherSmartRef({object_idx}).isAvailable && getDaughterGenParticleMotherSmartRef({object_idx}).isNonnull) ? getDaughterGenParticleMotherSmartRef({object_idx}).pt() : -999', 
    objectGenMotherEnergy =  '? (getDaughterGenParticleMotherSmartRef({object_idx}).isAvailable && getDaughterGenParticleMotherSmartRef({object_idx}).isNonnull) ? getDaughterGenParticleMotherSmartRef({object_idx}).energy() : -999', 
    objectGenMotherEta =  '? (getDaughterGenParticleMotherSmartRef({object_idx}).isAvailable && getDaughterGenParticleMotherSmartRef({object_idx}).isNonnull) ? getDaughterGenParticleMotherSmartRef({object_idx}).eta() : -999', 
    objectGenMotherPhi =  '? (getDaughterGenParticleMotherSmartRef({object_idx}).isAvailable && getDaughterGenParticleMotherSmartRef({object_idx}).isNonnull) ? getDaughterGenParticleMotherSmartRef({object_idx}).phi() : -999', 

    objectGenJetPt = '{object}.userFloat("genJetPt")',    
    objectGenJetEta = '{object}.userFloat("genJetEta")',  

    objectGenStatus = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef.status : -999 ',
    objectGenPdgId = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef.pdgId : -999 ',
    objectGenEta = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef.eta : -999 ',
    objectGenPhi = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef.phi : -999 ',
    objectGenPt = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef.pt : -999 ',
    objectGenEnergy = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef.energy : -999 ',
    objectGenCharge = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef.charge : -999 ',

    objectComesFromHiggs = 'comesFromHiggsRef({object_idx})',

    objectPt_TauEnUp = '? daughterHasUserCand({object_idx}, "tesUpTaus") ? daughterAsTau({object_idx}).userCand("tesUpTaus").pt : -999.',
    objectEta_TauEnUp = '? daughterHasUserCand({object_idx}, "tesUpTaus") ? daughterAsTau({object_idx}).userCand("tesUpTaus").eta : -999.',
    objectPhi_TauEnUp = '? daughterHasUserCand({object_idx}, "tesUpTaus") ? daughterAsTau({object_idx}).userCand("tesUpTaus").phi : -999.',
    objectMass_TauEnUp = '? daughterHasUserCand({object_idx}, "tesUpTaus") ? daughterAsTau({object_idx}).userCand("tesUpTaus").mass : -999.',

    objectPt_TauEnDown = '? daughterHasUserCand({object_idx}, "tesDownTaus") ? daughterAsTau({object_idx}).userCand("tesDownTaus").pt : -999.',
    objectEta_TauEnDown = '? daughterHasUserCand({object_idx}, "tesDownTaus") ? daughterAsTau({object_idx}).userCand("tesDownTaus").eta : -999.',
    objectPhi_TauEnDown = '? daughterHasUserCand({object_idx}, "tesDownTaus") ? daughterAsTau({object_idx}).userCand("tesDownTaus").phi : -999.',
    objectMass_TauEnDown = '? daughterHasUserCand({object_idx}, "tesDownTaus") ? daughterAsTau({object_idx}).userCand("tesDownTaus").mass : -999.',




)


