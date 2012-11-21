import FWCore.ParameterSet.Config as cms

def set_passthru(process):
    #remove all preselection cuts
    process.ee.selections = cms.VPSet()
    process.mm.selections = cms.VPSet()

    process.eeg.selections = cms.VPSet()
    process.mmg.selections = cms.VPSet()
    
