import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.version import cmssw_major_version

customizeMuonSequence = cms.Sequence()

from FinalStateAnalysis.PatTools.muons.muTrackCandidates_cfi \
     import trackCandidates
customizeMuonSequence += trackCandidates

from FinalStateAnalysis.PatTools.muons.patMuonRhoEmbedding_cfi import \
        patMuonRhoEmbedding, patMuonZZRhoEmbedding, patMuonZZ2012RhoEmbedding,\
	patMuonHZG2011RhoEmbedding, patMuonHZG2012RhoEmbedding

customizeMuonSequence += patMuonRhoEmbedding
customizeMuonSequence += patMuonZZRhoEmbedding
customizeMuonSequence += patMuonHZG2011RhoEmbedding
if cmssw_major_version() == 5:
	customizeMuonSequence += patMuonZZ2012RhoEmbedding
	customizeMuonSequence += patMuonHZG2012RhoEmbedding

from FinalStateAnalysis.PatTools.muons.patMuonIdEmbedding_cfi import \
        patMuonsEmbedWWId, patMuonsEmbedWWId2011, patVBTFMuonMatch, \
	patMuonsEmbedHZG2011, patMuonsEmbedHZG2012

customizeMuonSequence += patMuonsEmbedWWId
customizeMuonSequence += patMuonsEmbedWWId2011
customizeMuonSequence += patVBTFMuonMatch
customizeMuonSequence += patMuonsEmbedHZG2011
customizeMuonSequence += patMuonsEmbedHZG2012

from FinalStateAnalysis.PatTools.muons.patMuonEAEmbedding_cfi import \
     patMuonEAEmbedder

customizeMuonSequence += patMuonEAEmbedder

from FinalStateAnalysis.PatTools.muons.patMuonPFMuonEmbedding_cfi import \
        patMuonPFMuonEmbedding
customizeMuonSequence += patMuonPFMuonEmbedding

from FinalStateAnalysis.PatTools.muons.patMuonIpEmbedding_cfi \
     import patMuonsEmbedIp
customizeMuonSequence += patMuonsEmbedIp

from FinalStateAnalysis.PatTools.muons.patMuonEmbedJetInfo_cfi import \
        patMuonsEmbedJetInfo
customizeMuonSequence += patMuonsEmbedJetInfo

# This depends on a lot of stuff, so it should go last.
from FinalStateAnalysis.PatTools.muons.patMuonTightIdEmbedding_cfi import \
        patMuonTightIDEmbedding
customizeMuonSequence += patMuonTightIDEmbedding

from FinalStateAnalysis.PatTools.muons.patMuonRochesterCorrectionEmbedding_cfi import \
     patMuonRochesterCorrectionEmbedder
customizeMuonSequence += patMuonRochesterCorrectionEmbedder

#from FinalStateAnalysis.PatTools.muons.triggerMatch_cfi import triggeredPatMuons
#customizeMuonSequence += triggeredPatMuons
