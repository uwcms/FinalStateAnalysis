/*
 * Since PATFinalStateEvent does not inherit from reco::Candidate,
 * we can't use the CandViewHistoAnalyzer.  This is its replacment.
 *
 * Author: Evan K. Friis, UW Madison
 *
 */

#include "FWCore/Framework/interface/MakerMacros.h"
#include "CommonTools/UtilAlgos/interface/HistoAnalyzer.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEventFwd.h"

typedef HistoAnalyzer<PATFinalStateEventCollection> PATFinalStateEventHistoAnalyzer;

DEFINE_FWK_MODULE( PATFinalStateEventHistoAnalyzer );
