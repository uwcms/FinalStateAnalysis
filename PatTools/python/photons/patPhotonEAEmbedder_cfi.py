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

from FinalStateAnalysis.PatTools.photons.effective_areas_cff import \
     photon_eas

ea_list = deepcopy(photon_eas)

patPhotonEAEmbedder = cms.EDProducer(
    'PATPhotonEAEmbedder',
    src = cms.InputTag("fixme"),
    effective_areas = ea_list,
    applied_effective_areas = cms.vstring('PhotonEA_pfchg',
                                          'PhotonEA_pfneut',
                                          'PhotonEA_pfpho')
    )
