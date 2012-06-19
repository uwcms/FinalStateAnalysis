'''

Pileup distributions used by PileupWeighting.h

This uses the "truth" 1-D reweighting.

See https://twiki.cern.ch/twiki/bin/view/CMS/PileupMCReweightingUtilities

Author: Evan K. Friis, UW Madison

'''

import FWCore.ParameterSet.Config as cms

pileup_distributions = cms.PSet(
    # MC distributions
    S6 = cms.FileInPath("FinalStateAnalysis/DataAlgos/data/pu/fall11_mc_truth.root"),
    S7 = cms.FileInPath("FinalStateAnalysis/DataAlgos/data/pu/summer12_mc_truth.root"),
    # Data distributions
    data2011A = cms.FileInPath("FinalStateAnalysis/DataAlgos/data/pu/allData_2011A_pileupTruth_v2.root"),
    data2011B = cms.FileInPath("FinalStateAnalysis/DataAlgos/data/pu/allData_2011B_pileupTruth_v2.root"),
    data2011AB = cms.FileInPath("FinalStateAnalysis/DataAlgos/data/pu/allData_2011AB_pileupTruth_v2.root"),
    data2012A = cms.FileInPath("FinalStateAnalysis/DataAlgos/data/pu/data_2012_190456-194479.root"),
    data2012AB_195947 = cms.FileInPath("FinalStateAnalysis/DataAlgos/data/pu/data_2012_190456-195947.root"),
)
