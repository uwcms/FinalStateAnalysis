import FWCore.ParameterSet.Config as cms

'''

Snippet to add h2tau ntuple production to the process

'''

def add_h2tau_ntuples(process, schedule):
    process.load("FinalStateAnalysis.Higgs.et_ntuple")
    process.load("FinalStateAnalysis.Higgs.em_ntuple")
    process.load("FinalStateAnalysis.Higgs.mt_ntuple")

    process.etaupath = cms.Path(process.etau)
    process.emupath = cms.Path(process.emu)
    process.mutaupath = cms.Path(process.mutau)

    schedule.append(process.etaupath)
    schedule.append(process.mutaupath)
    schedule.append(process.emupath)
