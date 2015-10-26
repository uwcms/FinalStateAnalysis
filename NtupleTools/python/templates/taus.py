
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

    objectAgainstElectronLoose  = '{object}.tauID("againstElectronLoose")',
    objectAgainstElectronMedium = '{object}.tauID("againstElectronMedium")',
    objectAgainstElectronTight  = '{object}.tauID("againstElectronTight")',

    # Against Muon
    objectAgainstMuonLoose = '{object}.tauID("againstMuonLoose")',
    objectAgainstMuonLoose2 = '{object}.tauID("againstMuonLoose2")',
    objectAgainstMuonLoose3 = '{object}.tauID("againstMuonLoose3")',
    objectAgainstMuonLooseMVA = '{object}.tauID("againstMuonLooseMVA")',

    objectAgainstMuonMedium = '{object}.tauID("againstMuonMedium")',
    objectAgainstMuonMedium2 = '{object}.tauID("againstMuonMedium2")',
    objectAgainstMuonMediumMVA = '{object}.tauID("againstMuonMediumMVA")',

    objectAgainstMuonTight = '{object}.tauID("againstMuonTight")',
    objectAgainstMuonTight2 = '{object}.tauID("againstMuonTight2")',
    objectAgainstMuonTight3 = '{object}.tauID("againstMuonTight3")',
    objectAgainstMuonTightMVA = '{object}.tauID("againstMuonTightMVA")',

    objectAgainstMuonMVAraw = '{object}.tauID("againstMuonMVAraw")',
    
    # combined isolation DB corr 3 hits
    objectByLooseCombinedIsolationDeltaBetaCorr3Hits = '{object}.tauID("byLooseCombinedIsolationDeltaBetaCorr3Hits")',
    objectByMediumCombinedIsolationDeltaBetaCorr3Hits = '{object}.tauID("byMediumCombinedIsolationDeltaBetaCorr3Hits")', 
    objectByTightCombinedIsolationDeltaBetaCorr3Hits = '{object}.tauID("byTightCombinedIsolationDeltaBetaCorr3Hits")',
    objectByCombinedIsolationDeltaBetaCorrRaw3Hits = '{object}.tauID("byCombinedIsolationDeltaBetaCorrRaw3Hits")',
    
    # BDT based tau ID discriminator based on isolation Pt sums plus tau lifetime information, trained on 1-prong, "2-prong" and 3-prong tau candidates 
    objectByVLooseIsolationMVA3newDMwLT = '{object}.tauID("byVLooseIsolationMVA3newDMwLT")',
    objectByVLooseIsolationMVA3newDMwoLT = '{object}.tauID("byVLooseIsolationMVA3newDMwoLT")',
    objectByLooseIsolationMVA3newDMwLT = '{object}.tauID("byLooseIsolationMVA3newDMwLT")',
    objectByLooseIsolationMVA3newDMwoLT = '{object}.tauID("byLooseIsolationMVA3newDMwoLT")',
    objectByMediumIsolationMVA3newDMwLT = '{object}.tauID("byMediumIsolationMVA3newDMwLT")', 
    objectByMediumIsolationMVA3newDMwoLT = '{object}.tauID("byMediumIsolationMVA3newDMwoLT")', 
    objectByTightIsolationMVA3newDMwLT = '{object}.tauID("byTightIsolationMVA3newDMwLT")',
    objectByTightIsolationMVA3newDMwoLT = '{object}.tauID("byTightIsolationMVA3newDMwoLT")',
    objectByVTightIsolationMVA3newDMwLT = '{object}.tauID("byVTightIsolationMVA3newDMwLT")', 
    objectByVTightIsolationMVA3newDMwoLT = '{object}.tauID("byVTightIsolationMVA3newDMwoLT")', 
    objectByVVTightIsolationMVA3newDMwLT = '{object}.tauID("byVVTightIsolationMVA3newDMwLT")', 
    objectByVVTightIsolationMVA3newDMwoLT = '{object}.tauID("byVVTightIsolationMVA3newDMwoLT")', 
    objectByIsolationMVA3newDMwLTraw = '{object}.tauID("byIsolationMVA3newDMwLTraw")',
    objectByIsolationMVA3newDMwoLTraw = '{object}.tauID("byIsolationMVA3newDMwoLTraw")',
    
    # BDT based tau ID discriminator based on isolation Pt sums plus tau lifetime information, trained on 1-prong and 3-prong tau candidates 
    objectByVLooseIsolationMVA3oldDMwLT = '{object}.tauID("byVLooseIsolationMVA3oldDMwLT")', 
    objectByVLooseIsolationMVA3oldDMwoLT = '{object}.tauID("byVLooseIsolationMVA3oldDMwoLT")', 
    objectByLooseIsolationMVA3oldDMwLT = '{object}.tauID("byLooseIsolationMVA3oldDMwLT")', 
    objectByLooseIsolationMVA3oldDMwoLT = '{object}.tauID("byLooseIsolationMVA3oldDMwoLT")', 
    objectByMediumIsolationMVA3oldDMwLT = '{object}.tauID("byMediumIsolationMVA3oldDMwLT")', 
    objectByMediumIsolationMVA3oldDMwoLT = '{object}.tauID("byMediumIsolationMVA3oldDMwoLT")', 
    objectByTightIsolationMVA3oldDMwLT = '{object}.tauID("byTightIsolationMVA3oldDMwLT")', 
    objectByTightIsolationMVA3oldDMwoLT = '{object}.tauID("byTightIsolationMVA3oldDMwoLT")', 
    objectByVTightIsolationMVA3oldDMwLT = '{object}.tauID("byVTightIsolationMVA3oldDMwLT")', 
    objectByVTightIsolationMVA3oldDMwoLT = '{object}.tauID("byVTightIsolationMVA3oldDMwoLT")', 
    objectByVVTightIsolationMVA3oldDMwLT = '{object}.tauID("byVVTightIsolationMVA3oldDMwLT")',
    objectByVVTightIsolationMVA3oldDMwoLT = '{object}.tauID("byVVTightIsolationMVA3oldDMwoLT")',
    objectByIsolationMVA3oldDMwLTraw = '{object}.tauID("byIsolationMVA3oldDMwLTraw")', 
    objectByIsolationMVA3oldDMwoLTraw = '{object}.tauID("byIsolationMVA3oldDMwoLTraw")', 

    # DecayModeFinding
    objectDecayModeFinding       = '{object}.tauID("decayModeFinding")',
    objectDecayModeFindingNewDMs = '{object}.tauID("decayModeFindingNewDMs")',

    objectNeutralIsoPtSum = '{object}.tauID("neutralIsoPtSum")',
    objectChargedIsoPtSum = '{object}.tauID("chargedIsoPtSum")',
    objectPuCorrPtSum     = '{object}.tauID("puCorrPtSum")',

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

    objectGenStatus = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef.status : -2 ',
    objectGenPdgId = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef.pdgId : -2 ',
    objectGenEta = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef.eta : -2 ',
    objectGenPhi = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef.phi : -2 ',
    objectGenPt = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef.pt : -2 ',
    objectGenEnergy = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef.energy : -2 ',
    objectGenCharge = '? {object}.genParticleRef.isNonnull?  {object}.genParticleRef.charge : -2 ',

    objectComesFromHiggs = 'comesFromHiggsRef({object_idx})',




)


