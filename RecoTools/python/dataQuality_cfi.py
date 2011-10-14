import FWCore.ParameterSet.Config as cms

'''
Original author: Christian Veelken
'''

#--------------------------------------------------------------------------------
# select pp collision events in "good" runs
# ( following recommendations given at https://twiki.cern.ch/twiki/bin/view/CMS/Collisions2010Recipes )
#--------------------------------------------------------------------------------

# veto events not recorded during periods of "physics declared"
from HLTrigger.special.hltPhysicsDeclared_cfi import hltPhysicsDeclared
hltPhysicsDeclared.L1GtReadoutRecordTag = 'gtDigis'

#veto events in which not all subdetectors were "on"
#
# NOTE: the DCS partitions for which "on"/"off" status is recorded separately are:
#
#  "EBp", "EBm", "EEp", "EEm", "HBHEa", "HBHEb", "HBHEc", "HF", "HO", "RPC"
#  "DT0", "DTp", "DTm", "CSCp", "CSCm", "CASTOR", "TIBTID", "TOB", "TECp", "TECm"
#  "BPIX", "FPIX", "ESp", "ESm"
#
from DPGAnalysis.Skims.DetStatus_cfi import dcsstatus
dcsstatus.DetectorType = cms.vstring(
    'EBp', 'EBm', 'EEp', 'EEm',
    ##'ESp', 'ESm',
    'HBHEa', 'HBHEb', 'HBHEc',
    ##'HF', 'HO',
    'DT0', 'DTp', 'DTm', 'CSCp', 'CSCm',
    'TIBTID', 'TOB', 'TECp', 'TECm',
    'BPIX', 'FPIX'
)
dcsstatus.ApplyFilter = cms.bool(True)
dcsstatus.DebugOn = cms.untracked.bool(False)
dcsstatus.AndOr = cms.bool(True)

# veto "scraping" beam events
# (identified by small percentage "good" tracks fitted to primary event vertex)
scrapingBeamsFilter = cms.EDFilter("FilterOutScraping",
    applyfilter = cms.untracked.bool(True),
    debugOn = cms.untracked.bool(False),
    numtrack = cms.untracked.uint32(10),
    thresh = cms.untracked.double(0.25)
)

# veto events without a "good" primary vertex
# ( see http://indico.cern.ch/getFile.py/access?subContId=0&contribId=2&resId=0&materialId=slides&confId=83613 )
primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
    vertexCollection = cms.InputTag('offlinePrimaryVertices'),
    minimumNDOF = cms.uint32(4),
    maxAbsZ = cms.double(15),
    maxd0 = cms.double(2)
)

# veto events with significant RBX/HPD noise activity
# ( see https://twiki.cern.ch/twiki/bin/view/CMS/HcalDPGAnomalousSignals )
from CommonTools.RecoAlgos.HBHENoiseFilter_cfi import HBHENoiseFilter

dataQualityFilters = cms.Sequence(
    hltPhysicsDeclared
   * dcsstatus
   * scrapingBeamsFilter
   * primaryVertexFilter
   * HBHENoiseFilter
)
