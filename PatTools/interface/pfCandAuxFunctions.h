#ifndef TauAnalysis_CandidateTools_pfCandAuxFunctions_h
#define TauAnalysis_CandidateTools_pfCandAuxFunctions_h

#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/BeamSpot/interface/BeamSpot.h"

#include <vector>

std::vector<const reco::PFCandidate*> getPFCandidatesOfType(const reco::PFCandidateCollection&, reco::PFCandidate::ParticleType);
void getPileUpPFCandidates(const std::vector<const reco::PFCandidate*>&, const std::vector<const reco::Track*>&,
			   const reco::VertexCollection&, double, const reco::BeamSpot&,
			   std::vector<const reco::PFCandidate*>&, std::vector<const reco::PFCandidate*>&);
const reco::Vertex* findVertex(const reco::Track*, const reco::VertexCollection&, double, const reco::BeamSpot&);

#endif
