import FWCore.ParameterSet.Config as cms

lumiWeights = cms.EDProducer(
    "LumiWeightProducer",
    monteCarlo = cms.vdouble(),
    data = cms.PSet(
        fileName = cms.FileInPath("FinalStateAnalysis/RecoTools/data/Pileup_2011_EPS_8_jul.root"),
        pathToHist = cms.string("pileup"),
    ),
    autoPad = cms.bool(True),
)

lumiWeights.monteCarlo = cms.vdouble(
    0.104109,
    0.0703573,
    0.0698445,
    0.0698254,
    0.0697054,
    0.0697907,
    0.0696751,
    0.0694486,
    0.0680332,
    0.0651044,
    0.0598036,
    0.0527395,
    0.0439513,
    0.0352202,
    0.0266714,
    0.019411,
    0.0133974,
    0.00898536,
    0.0057516,
    0.00351493,
    0.00212087,
    0.00122891,
    0.00070592,
    0.000384744,
    0.000219377
)
