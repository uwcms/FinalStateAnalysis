
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
    

    #Deep ID
    objectDeepTau2017v2p1VSmuraw = '? {object}.hasUserFloat("byDeepTau2017v2p1VSmuraw") ? {object}.userFloat("byDeepTau2017v2p1VSmuraw") : -10',
    objectVLooseDeepTau2017v2p1VSmu = '? {object}.hasUserFloat("byVLooseDeepTau2017v2p1VSmu") ? {object}.userFloat("byVLooseDeepTau2017v2p1VSmu") : -10',
    objectLooseDeepTau2017v2p1VSmu = '? {object}.hasUserFloat("byLooseDeepTau2017v2p1VSmu") ? {object}.userFloat("byLooseDeepTau2017v2p1VSmu") : -10',
    objectMediumDeepTau2017v2p1VSmu = '? {object}.hasUserFloat("byMediumDeepTau2017v2p1VSmu") ? {object}.userFloat("byMediumDeepTau2017v2p1VSmu") : -10',
    objectTightDeepTau2017v2p1VSmu = '? {object}.hasUserFloat("byTightDeepTau2017v2p1VSmu") ? {object}.userFloat("byTightDeepTau2017v2p1VSmu") : -10',
    objectVTightDeepTau2017v2p1VSmu = '? {object}.hasUserFloat("byVTightDeepTau2017v2p1VSmu") ? {object}.userFloat("byVTightDeepTau2017v2p1VSmu") : -10',
    objectVVTightDeepTau2017v2p1VSmu = '? {object}.hasUserFloat("byVVTightDeepTau2017v2p1VSmu") ? {object}.userFloat("byVVTightDeepTau2017v2p1VSmu") : -10',

    objectDeepTau2017v2p1VSeraw = '? {object}.hasUserFloat("byDeepTau2017v2p1VSeraw") ? {object}.userFloat("byDeepTau2017v2p1VSeraw") : -10',
    objectVVVLooseDeepTau2017v2p1VSe = '? {object}.hasUserFloat("byVVVLooseDeepTau2017v2p1VSe") ? {object}.userFloat("byVVVLooseDeepTau2017v2p1VSe") : -10',
    objectVVLooseDeepTau2017v2p1VSe = '? {object}.hasUserFloat("byVVLooseDeepTau2017v2p1VSe") ? {object}.userFloat("byVVLooseDeepTau2017v2p1VSe") : -10',
    objectVLooseDeepTau2017v2p1VSe = '? {object}.hasUserFloat("byVLooseDeepTau2017v2p1VSe") ? {object}.userFloat("byVLooseDeepTau2017v2p1VSe") : -10',
    objectLooseDeepTau2017v2p1VSe = '? {object}.hasUserFloat("byLooseDeepTau2017v2p1VSe") ? {object}.userFloat("byLooseDeepTau2017v2p1VSe") : -10',
    objectMediumDeepTau2017v2p1VSe = '? {object}.hasUserFloat("byMediumDeepTau2017v2p1VSe") ? {object}.userFloat("byMediumDeepTau2017v2p1VSe") : -10',
    objectTightDeepTau2017v2p1VSe = '? {object}.hasUserFloat("byTightDeepTau2017v2p1VSe") ? {object}.userFloat("byTightDeepTau2017v2p1VSe") : -10',
    objectVTightDeepTau2017v2p1VSe = '? {object}.hasUserFloat("byVTightDeepTau2017v2p1VSe") ? {object}.userFloat("byVTightDeepTau2017v2p1VSe") : -10',
    objectVVTightDeepTau2017v2p1VSe = '? {object}.hasUserFloat("byVVTightDeepTau2017v2p1VSe") ? {object}.userFloat("byVVTightDeepTau2017v2p1VSe") : -10',

    objectDeepTau2017v2p1VSjetraw = '? {object}.hasUserFloat("byDeepTau2017v2p1VSjetraw") ? {object}.userFloat("byDeepTau2017v2p1VSjetraw") : -10',
    objectVVVLooseDeepTau2017v2p1VSjet = '? {object}.hasUserFloat("byVVVLooseDeepTau2017v2p1VSjet") ? {object}.userFloat("byVVVLooseDeepTau2017v2p1VSjet") : -10',
    objectVVLooseDeepTau2017v2p1VSjet = '? {object}.hasUserFloat("byVVLooseDeepTau2017v2p1VSjet") ? {object}.userFloat("byVVLooseDeepTau2017v2p1VSjet") : -10',
    objectVLooseDeepTau2017v2p1VSjet = '? {object}.hasUserFloat("byVLooseDeepTau2017v2p1VSjet") ? {object}.userFloat("byVLooseDeepTau2017v2p1VSjet") : -10',
    objectLooseDeepTau2017v2p1VSjet = '? {object}.hasUserFloat("byLooseDeepTau2017v2p1VSjet") ? {object}.userFloat("byLooseDeepTau2017v2p1VSjet") : -10',
    objectMediumDeepTau2017v2p1VSjet = '? {object}.hasUserFloat("byMediumDeepTau2017v2p1VSjet") ? {object}.userFloat("byMediumDeepTau2017v2p1VSjet") : -10',
    objectTightDeepTau2017v2p1VSjet = '? {object}.hasUserFloat("byTightDeepTau2017v2p1VSjet") ? {object}.userFloat("byTightDeepTau2017v2p1VSjet") : -10',
    objectVTightDeepTau2017v2p1VSjet = '? {object}.hasUserFloat("byVTightDeepTau2017v2p1VSjet") ? {object}.userFloat("byVTightDeepTau2017v2p1VSjet") : -10',
    objectVVTightDeepTau2017v2p1VSjet = '? {object}.hasUserFloat("byVVTightDeepTau2017v2p1VSjet") ? {object}.userFloat("byVVTightDeepTau2017v2p1VSjet") : -10',

    
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


