##
#
# Configuration file for effective area isolation
#
# Relevant link for values:
# https://indico.cern.ch/getFile.py/access?contribId=1&resId=0&materialId=slides&confId=188494
#
##
import FWCore.ParameterSet.Config as cms
from copy import deepcopy

from FinalStateAnalysis.PatTools.muons.effective_areas_cff import \
     eas_kt6PFJetsCentralNeutral_th05, eas_kt6PFJetsCentral_th05

ea_list = deepcopy(eas_kt6PFJetsCentralNeutral_th05)
ea_list += eas_kt6PFJetsCentral_th05

patMuonEAEmbedder = cms.EDProducer(
    'PATMuonEAEmbedder',
    src = cms.InputTag("fixme"),
    effective_areas = ea_list,
    applied_effective_areas = cms.vstring('ea_comb_iso04_kt6PFJCNth05',
                                          'ea_comb_iso04_kt6PFJCth05')
    )
