##
#
# Configuration file for effective area isolation
#
# Relevant link for values:
# http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/UserCode/EGamma/EGammaAnalysisTools/interface/ElectronEffectiveArea.h?revision=1.3&view=markup
#
##
import FWCore.ParameterSet.Config as cms
from copy import deepcopy

from FinalStateAnalysis.PatTools.electrons.effective_areas_cff import \
     available_eas

ea_list = deepcopy(available_eas)

patElectronEAEmbedder = cms.EDProducer(
    'PATElectronEAEmbedder',
    src = cms.InputTag("fixme"),
    effective_areas = ea_list,
    applied_effective_areas = cms.vstring('ea_comb_Data2012_iso04_kt6PFJ',
                                          'ea_comb_Data2011_iso04_kt6PFJ',
                                          'ea_comb_Fall11MC_iso04_kt6PFJ',
                                          'ea_comb_NoCorr_iso04_kt6PFJ')
    )
