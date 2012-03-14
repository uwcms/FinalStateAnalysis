import FWCore.ParameterSet.Config as cms

'''

Snippet to add TNP dilepton ntuple production to the process

'''

def add_tnp_ntuples(process, schedule):
    process.load("FinalStateAnalysis.Higgs.ee_ntuple")
    process.load("FinalStateAnalysis.Higgs.mm_ntuple")

    process.eepath = cms.Path(process.ee)
    process.mumupath = cms.Path(process.mumu)

    schedule.append(process.eepath)
    schedule.append(process.mumupath)
