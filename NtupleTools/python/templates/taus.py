
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
    objectNSignalCands = '{object}.signalCands().size()',
    objectNChrgHadrSignalCands = '{object}.signalChargedHadrCands().size()',
    objectNChrgHadrIsolationCands = '{object}.isolationChargedHadrCands().size()',
    objectNGammaSignalCands = '{object}.signalGammaCands().size()',
    objectNNeutralHadrSignalCands = '{object}.signalNeutrHadrCands().size()',
)


# ID and isolation
id = PSet(

    objectAgainstElectronVLooseMVA6 = '{object}.tauID("againstElectronVLooseMVA6")', 
    objectAgainstElectronLooseMVA6  = '{object}.tauID("againstElectronLooseMVA6")',
    objectAgainstElectronMediumMVA6 = '{object}.tauID("againstElectronMediumMVA6")',
    objectAgainstElectronTightMVA6  = '{object}.tauID("againstElectronTightMVA6")',
    objectAgainstElectronVTightMVA6 = '{object}.tauID("againstElectronVTightMVA6")',
    
    objectAgainstElectronMVA6category = '{object}.tauID("againstElectronMVA6category")',
    objectAgainstElectronMVA6Raw      = '{object}.tauID("againstElectronMVA6Raw")',
    objectAgainstMuonLoose3 = '{object}.tauID("againstMuonLoose3")',
    objectAgainstMuonTight3 = '{object}.tauID("againstMuonTight3")',
    

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

)


