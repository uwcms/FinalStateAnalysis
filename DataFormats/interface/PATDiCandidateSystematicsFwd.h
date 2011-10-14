#ifndef FinalStateAnalysis_DataFormats_PATDICandiSysFwd_h
#define FinalStateAnalysis_DataFormats_PATDICandiSysFwd_h

#include "FinalStateAnalysis/DataFormats/interface/PATDiCandidateSystematics.h"

#include "DataFormats/Common/interface/Ref.h"
#include "DataFormats/Common/interface/Ptr.h"
#include "DataFormats/Common/interface/RefProd.h"
#include "DataFormats/Common/interface/RefVector.h"

#include <vector>

/// collection of CPATMuTauSystematics objects
typedef std::vector<PATMuTauSystematics> PATMuTauSystematicsCollection;
typedef edm::Ref<PATMuTauSystematicsCollection> PATMuTauSystematicsRef;
typedef edm::RefProd<PATMuTauSystematicsCollection> PATMuTauSystematicsRefProd;
typedef edm::RefVector<PATMuTauSystematicsCollection> PATMuTauSystematicsRefVector;
typedef edm::Ptr<PATMuTauSystematics> PATMuTauSystematicsPtr;

#endif
