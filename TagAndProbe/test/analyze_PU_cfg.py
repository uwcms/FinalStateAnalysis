import FWCore.ParameterSet.Config as cms
import FinalStateAnalysis.Selectors.plotting.plotting as plotting
import FinalStateAnalysis.Selectors.selectors.selectors as selectors
from FinalStateAnalysis.Utilities.PSetTemplate import PSetTemplate

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
options = TauVarParsing.TauVarParsing(
    skipEvents=0, # For debugging
)

options.outputFile="pu.root"
options.parseArguments()

process = cms.Process("PUStudy")

# Input in FWLITE mode
process.fwliteInput = cms.PSet(fileNames = cms.vstring(options.inputFiles))
process.fwliteOutput = cms.PSet(fileName = cms.string(options.outputFile))

process.steering = cms.PSet(
    analyzers = cms.vstring(
        'wjets', 'ztt'
    ),
    reportAfter = cms.uint32(100),
    ignored_cuts = cms.vstring()
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents))

# Common among all analyzers
process.common = cms.PSet(
    weights = cms.VInputTag(
        cms.InputTag("lumiWeights", "3bx")
    ),
    skimCounter = cms.InputTag("eventCount", "", "TUPLE"),
)

leg1 = {
    'name' : 'Mu', 'getter' :'daughter(0).', 'nicename' : 'Muon',
}
leg2 = {
    'name' : 'Tau', 'getter' :'daughter(1).', 'nicename' : 'Tau',
}

process.selectWjets = cms.VPSet(
    PSetTemplate(selectors.trigger.hlt).replace(
        name = 'IsoMu24', nicename = 'Final State',
        hlt_path = "HLT_IsoMu24_v*",),
    # Select muon leg 1 pt
    PSetTemplate(selectors.candidate.pt).replace(
        threshold = '25', **leg1),
    # Select muon leg 1 eta
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.1', **leg1),
    PSetTemplate(selectors.muons.id).replace(
        muID = 'WWID', **leg1),
    PSetTemplate(selectors.muons.reliso).replace(
        threshold = '0.2', **leg1),
    # Enhance W+jets
    PSetTemplate(selectors.topology.mtMetCut).replace(
        index = 1, threshold = 50, **leg1).clone(invert = True),
    # Select tau pt
    PSetTemplate(selectors.taus.jetpt).replace(
        threshold = '20', index=1, **leg2),
    ## Select tau eta
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.5', **leg2),
    PSetTemplate(selectors.taus.id).replace(
        tauID = 'againstElectronTight', **leg2),
    PSetTemplate(selectors.taus.id).replace(
        tauID = 'againstMuonTight', **leg2),

)

process.selectZtautau = cms.VPSet(
    # Select muon leg 1 pt
    PSetTemplate(selectors.candidate.pt).replace(
        threshold = '10', **leg1),
    # Select muon leg 1 eta
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.5', **leg1),
    PSetTemplate(selectors.muons.reliso).replace(
        threshold = '0.3', **leg1),
    # Select tau pt
    PSetTemplate(selectors.taus.jetpt).replace(
        threshold = '10', index=1, **leg2),
    ## Select tau eta
    PSetTemplate(selectors.candidate.eta).replace(
        threshold = '2.5', **leg2),
    PSetTemplate(selectors.taus.id).replace(
        tauID = 'againstElectronTight', **leg2),
    PSetTemplate(selectors.taus.id).replace(
        tauID = 'againstMuonTight', **leg2),
    PSetTemplate(selectors.taus.isTrueTau).replace(**leg2),
)

ntuple = cms.PSet(
    pt = cms.string('daughter(1).pt'),
    eta = cms.string('daughter(1).eta'),
    jetpt = cms.string('daughterUserCand(1, "patJet").pt'),
    rho = cms.string('evt().rho()'),
    nReco = cms.string('evt().recoVertices().size()'),
    nSim = cms.string('? evt().puInfo().size() ? evt().puInfo().at(0).getPU_NumInteractions() : - 1'),
    pdgId = cms.string(
        "? daughter(1).genParticleRef().isNonnull ? abs(daughter(1).genParticleRef().pdgId()) : -1"),
    genDecayMode = cms.string('daughter(1).userInt("genDecayMode")'),
    byVLooseCombinedIsolationDeltaBetaCorr = cms.string('daughter(1).tauID("byVLooseCombinedIsolationDeltaBetaCorr")'),
    byLooseCombinedIsolationDeltaBetaCorr = cms.string('daughter(1).tauID("byLooseCombinedIsolationDeltaBetaCorr")'),
    byMediumCombinedIsolationDeltaBetaCorr = cms.string('daughter(1).tauID("byMediumCombinedIsolationDeltaBetaCorr")'),
    byTightCombinedIsolationDeltaBetaCorr = cms.string('daughter(1).tauID("byTightCombinedIsolationDeltaBetaCorr")'),
    byVLooseIsolation = cms.string('daughter(1).tauID("byVLooseIsolation")'),
    byLooseIsolation = cms.string('daughter(1).tauID("byLooseIsolation")'),
    byMediumIsolation = cms.string('daughter(1).tauID("byMediumIsolation")'),
    byTightIsolation = cms.string('daughter(1).tauID("byTightIsolation")'),
)

process.wjets = cms.PSet(
    process.common,
    src = cms.InputTag('finalStateMuTau'),
    splitRuns = cms.bool(True),
    analysis = cms.PSet(
        ignore = process.steering.ignored_cuts,
        final = cms.PSet(
            sort = cms.string('daughter(1).pt'),
            take = cms.uint32(1),
            plot = cms.PSet(
                ntuple = ntuple,
                histos=cms.VPSet()
            ),
        ),
        selections = process.selectWjets
    )
)

process.ztt = cms.PSet(
    process.common,
    src = cms.InputTag('finalStateMuTau'),
    splitRuns = cms.bool(False),
    analysis = cms.PSet(
        ignore = process.steering.ignored_cuts,
        final = cms.PSet(
            sort = cms.string('daughter(1).pt'),
            take = cms.uint32(1),
            plot = cms.PSet(
                ntuple = ntuple,
                histos=cms.VPSet()
            ),
        ),
        selections = process.selectZtautau
    )
)

