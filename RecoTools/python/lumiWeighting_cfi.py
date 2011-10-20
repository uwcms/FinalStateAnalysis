import FWCore.ParameterSet.Config as cms

'''

Put weights for different PU scenarios in simulation and data

Name code:

    lumiWeights[MC SCENARIO][DATA_PERIODS][MAXRUN]

NB WHEN THIS IS UPDATED YOU SHOULD UPDATE PATFinalStateEventProducer_cfi

'''

simPUScenarios = cms.PSet(
    PU_S4 = cms.vdouble(
        0.104109, 0.0703573, 0.0698445, 0.0698254, 0.0697054, 0.0697907,
        0.0696751, 0.0694486, 0.0680332, 0.0651044, 0.0598036, 0.0527395,
        0.0439513, 0.0352202, 0.0266714, 0.019411, 0.0133974, 0.00898536,
        0.0057516, 0.00351493, 0.00212087, 0.00122891, 0.00070592,
        0.000384744, 0.000219377
    )
)

lumiWeightsS42011A = cms.EDProducer(
    "LumiWeightProducer",
    monteCarlo = simPUScenarios.PU_S4,
    data = cms.PSet(
        fileName = cms.FileInPath(
            "FinalStateAnalysis/RecoTools/data/allData_2011A_173692.root"),
        pathToHist = cms.string("pileup"),
    ),
    autoPad = cms.bool(True),
)

lumiWeightsS42011B178078 = cms.EDProducer(
    "LumiWeightProducer",
    monteCarlo = simPUScenarios.PU_S4,
    data = cms.PSet(
        fileName = cms.FileInPath(
            "FinalStateAnalysis/RecoTools/data/allData_2011B_178078.root"),
        pathToHist = cms.string("pileup"),
    ),
    autoPad = cms.bool(True),
)

lumiWeightsS42011AB178078 = cms.EDProducer(
    "LumiWeightProducer",
    monteCarlo = simPUScenarios.PU_S4,
    data = cms.PSet(
        fileName = cms.FileInPath(
            "FinalStateAnalysis/RecoTools/data/allData_2011AB_178078.root"),
        pathToHist = cms.string("pileup"),
    ),
    autoPad = cms.bool(True),
)

lumiWeights = cms.Sequence(
    lumiWeightsS42011A
    + lumiWeightsS42011B178078
    + lumiWeightsS42011AB178078
)
