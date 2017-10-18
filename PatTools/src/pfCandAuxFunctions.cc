#include "FinalStateAnalysis/PatTools/interface/pfCandAuxFunctions.h"

#include <TMath.h>

const double epsilon = 0.01;

std::vector<const reco::PFCandidate*> getPFCandidatesOfType(const reco::PFCandidateCollection& pfCandidates,
							    reco::PFCandidate::ParticleType pfParticleType)
{
  std::vector<const reco::PFCandidate*> retVal;

  for ( reco::PFCandidateCollection::const_iterator pfCandidate = pfCandidates.begin();
	pfCandidate != pfCandidates.end(); ++pfCandidate ) {
    if ( pfCandidate->particleId() == pfParticleType ) retVal.push_back(&(*pfCandidate));
  }

  return retVal;
}

void getPileUpPFCandidates(const std::vector<const reco::PFCandidate*>& pfCandidates,
			   const std::vector<const reco::Track*>& signalTracks,
			   const reco::VertexCollection& vertices, double deltaZ, const reco::BeamSpot& bs,
			   std::vector<const reco::PFCandidate*>& pfNoPileUpCandidates,
			   std::vector<const reco::PFCandidate*>& pfPileUpCandidates)
{
  std::vector<const reco::Vertex*> signalVertices;
  for ( std::vector<const reco::Track*>::const_iterator signalTrack = signalTracks.begin();
	signalTrack != signalTracks.end(); ++signalTrack ) {
    const reco::Vertex* signalVertex = findVertex(*signalTrack, vertices, deltaZ, bs);
    //std::cout << "signalVertex = " << signalVertex;
    //if ( signalVertex != 0 ) std::cout << ", z = " << signalVertex->z() << std::endl;
    //std::cout << std::endl;
    if ( signalVertex != 0 ) signalVertices.push_back(signalVertex);
  }

  //std::cout << " #signalVertices = " << signalVertices.size() << std::endl;

  //std::cout << " #pfCandidates = " << pfCandidates.size() << std::endl;

  for ( std::vector<const reco::PFCandidate*>::const_iterator pfCandidate = pfCandidates.begin();
	pfCandidate != pfCandidates.end(); ++pfCandidate ) {
    reco::TrackRef pfCandidateTrack = (*pfCandidate)->trackRef();
    if ( pfCandidateTrack.isNonnull() ) {
      const reco::Vertex* pfCandidateVertex = findVertex(pfCandidateTrack.get(), vertices, deltaZ, bs);
      //std::cout << "pfCandidateVertex = " << pfCandidateVertex;
      //if ( pfCandidateVertex != 0 ) std::cout << ", z = " << pfCandidateVertex->z() << std::endl;
      //std::cout << std::endl;

      bool isSignalVtx_associated = false;
      for ( std::vector<const reco::Vertex*>::const_iterator signalVertex = signalVertices.begin();
	    signalVertex != signalVertices.end(); ++signalVertex ) {
	if ( pfCandidateVertex == (*signalVertex) || (pfCandidateVertex->z() - (*signalVertex)->z()) < epsilon ) {
	  isSignalVtx_associated = true;
	  break;
	}
      }

      //std::cout << "--> isSignalVtx_associated = " << isSignalVtx_associated << ": pt = " << (*pfCandidate)->pt() << std::endl;

      if ( isSignalVtx_associated ) {
	pfNoPileUpCandidates.push_back(*pfCandidate);
      } else {
	pfPileUpCandidates.push_back(*pfCandidate);
      }
    }
  }
}

const reco::Vertex* findVertex(const reco::Track* signalTrack, const reco::VertexCollection& vertices,
			       double deltaZ, const reco::BeamSpot& bs)
{
// CV: this code has been taken from PhysicsTools/PFCandProducer/src/PFPileUp.cc (04/05/2011)

  //std::cout << "<findVertex>:" << std::endl;

  const reco::Vertex* retVal = 0;

  if ( !signalTrack ) return retVal;

  //std::cout << " signalTrack: pt = " << signalTrack->pt() << ","
  //	      << " eta = " << signalTrack->eta() << ", phi = " << signalTrack->phi() << ","
  //	      << " dz = " << (signalTrack->dz(bs.position()) + bs.position().z()) << std::endl;

//--- find vertex associated to track
  for ( reco::VertexCollection::const_iterator vertex = vertices.begin();
	vertex != vertices.end(); ++vertex ) {
    //std::cout << " vertex: z = " << vertex->z() << std::endl;
    for ( reco::Vertex::trackRef_iterator vtxAssocTrack = vertex->tracks_begin();
	  vtxAssocTrack != vertex->tracks_end(); ++vtxAssocTrack ) {
      //std::cout << "  vtxAssocTrack: pt = " << (*vtxAssocTrack)->pt() << ","
      //	  << " eta = " << (*vtxAssocTrack)->eta() << ", phi = " << (*vtxAssocTrack)->phi() << ","
      //	  << " dz = " << (*vtxAssocTrack)->dz(vertex->position()) << std::endl;
      if ( TMath::Abs((*vtxAssocTrack)->eta() - signalTrack->eta()) < epsilon                     &&
	   TMath::Abs((*vtxAssocTrack)->phi() - signalTrack->phi()) < epsilon                     &&
	   TMath::Abs((*vtxAssocTrack)->pt()  - signalTrack->pt())  < (epsilon*signalTrack->pt()) ) {
	//std::cout << "--> found match !!" << std::endl;
	retVal = &(*vertex);
	return retVal;
      }
    }
  }

//--- no vertex associated to track found,
//    find vertex best matching signalTrack by deltaZ
  double minDeltaZ = 1.e+3;
  double refZ = (signalTrack->dz(bs.position()) + bs.position().z());
  for ( reco::VertexCollection::const_iterator vertex = vertices.begin();
	vertex != vertices.end(); ++vertex ) {
    double deltaZ = TMath::Abs(vertex->z() - refZ);
    if ( retVal == 0 || deltaZ < minDeltaZ ) {
      retVal = &(*vertex);
      minDeltaZ = deltaZ;
    }
  }

  //std::cout << "minDeltaZ = " << minDeltaZ << std::endl;

  return retVal;
}
