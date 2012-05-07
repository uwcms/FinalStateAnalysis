import FWCore.ParameterSet.Config as cms

customizeMuonSequence = cms.Sequence()

from FinalStateAnalysis.PatTools.muons.muTrackCandidates_cfi import trackCandidates
customizeMuonSequence += trackCandidates

from FinalStateAnalysis.PatTools.muons.patMuonRhoEmbedding_cfi import \
        patMuonRhoEmbedding
customizeMuonSequence += patMuonRhoEmbedding

from FinalStateAnalysis.PatTools.muons.patMuonIdEmbedding_cfi import \
        patMuonsEmbedWWId, patVBTFMuonMatch
customizeMuonSequence += patMuonsEmbedWWId
customizeMuonSequence += patVBTFMuonMatch

from FinalStateAnalysis.PatTools.muons.patMuonPFMuonEmbedding_cfi import \
        patMuonPFMuonEmbedding
customizeMuonSequence += patMuonPFMuonEmbedding

from FinalStateAnalysis.PatTools.muons.patMuonIpEmbedding_cfi import patMuonsEmbedIp
customizeMuonSequence += patMuonsEmbedIp

from FinalStateAnalysis.PatTools.muons.patMuonEmbedJetInfo_cfi import \
        patMuonsEmbedJetInfo
customizeMuonSequence += patMuonsEmbedJetInfo

from FinalStateAnalysis.PatTools.muons.patMuonMVAIdIsoEmbedding_cfi import \
        patMuonMVAIdIsoEmbedding
customizeMuonSequence += patMuonMVAIdIsoEmbedding

from FinalStateAnalysis.PatTools.muons.muonSystematics_cfi import \
        poolDBESSourceMuScleFitCentralValue, \
        poolDBESSourceMuScleFitShiftUp, \
        poolDBESSourceMuScleFitShiftDown, \
        patMuonsEmbedSystematics
customizeMuonSequence += patMuonsEmbedSystematics

#from FinalStateAnalysis.PatTools.muons.triggerMatch_cfi import triggeredPatMuons
#customizeMuonSequence += triggeredPatMuons
