import FWCore.ParameterSet.Config as cms

'''

Snippet to add trilepton ntuple production to the process

'''

def add_trilepton_ntuples(process, schedule):
    process.load("FinalStateAnalysis.Higgs.emt_ntuple")
    process.load("FinalStateAnalysis.Higgs.mmt_ntuple")
    process.load("FinalStateAnalysis.Higgs.mmm_ntuple")
    process.load("FinalStateAnalysis.Higgs.emm_ntuple")

    process.emutaupath = cms.Path(process.emutau)
    process.mumutaupath = cms.Path(process.mumutau)
    process.mumumupath = cms.Path(process.mumumu)
    process.emumupath = cms.Path(process.emumu)

    schedule.append(process.emutaupath)
    schedule.append(process.mumutaupath)
    schedule.append(process.mumumupath)
    schedule.append(process.emumupath)
