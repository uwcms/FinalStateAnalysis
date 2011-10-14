#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FinalStateAnalysis/DataFormats/interface/PATDiCandidateSystematics.h"

#include "RecoVertex/KalmanVertexFit/interface/KalmanVertexFitter.h"
#include "RecoVertex/VertexPrimitives/interface/TransientVertex.h"

#include "TrackingTools/IPTools/interface/IPTools.h"
#include "TrackingTools/Records/interface/TransientTrackRecord.h"
#include "TrackingTools/TransientTrack/interface/TransientTrack.h"
#include "TrackingTools/TransientTrack/interface/TransientTrackBuilder.h"

#include "TrackingTools/PatternTools/interface/TwoTrackMinimumDistance.h"
#include "RecoVertex/KinematicFitPrimitives/interface/KinematicParticleFactoryFromTransientTrack.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/GsfTrackReco/interface/GsfTrack.h"
#include "DataFormats/GeometryCommonDetAlgo/interface/Measurement1D.h"
#include "Math/SMatrix.h"
#include "Math/SVector.h"

namespace {
  // Get the track with the best chi2/NDF
  reco::TrackBaseRef bestTrack(const std::vector<reco::TrackBaseRef>& input) {
    reco::TrackBaseRef bestSoFar;
    double bestChi2Ndf = -1;
    for (size_t i = 0; i < input.size(); ++i) {
      const reco::TrackBaseRef& trk = input.at(i);
      if (bestSoFar.isNull() || trk->normalizedChi2() < bestChi2Ndf) {
        bestSoFar = trk;
        bestChi2Ndf = trk->normalizedChi2();
      }
    }
    return bestSoFar;
  }

  // Build a transient track correctly
  reco::TransientTrack transTrack(const reco::TrackBaseRef& baseRef,
      const TransientTrackBuilder* trkBuilder) {
    reco::TransientTrack output;
    reco::TrackRef trkRef = baseRef.castTo<reco::TrackRef>();
    if (trkRef.isNull()) {
      reco::GsfTrackRef gsfRef = baseRef.castTo<reco::GsfTrackRef>();
      output = trkBuilder->build(gsfRef);
    } else {
      output = trkBuilder->build(trkRef);
    }
    return output;
  }

  // Compute the error in the covariance matrix projected along the displacement
  // direction.
  Measurement1D computeError3D(const GlobalVector& displacement,
      const GlobalError& error) {

    double errValues[9] = {
      error.cxx(), error.cyx(), error.czx(),
      error.cyx(), error.cyy(), error.czy(),
      error.czx(), error.czy(), error.czz() };
    ROOT::Math::SMatrix<double,3,3> fastError(errValues, 9);

    double dispValues[3] = {
      displacement.x(), displacement.y(), displacement.z()};
    ROOT::Math::SVector<double, 3> fastDisp(dispValues, 3);

    // from RecoBTag/SecondaryVertex/src/SecondaryVertex.cc
    double dist = ROOT::Math::Mag(fastDisp);
    double error1D = ROOT::Math::Similarity(fastError, fastDisp);

    if (error1D > 0.0 && dist > 1.0e-9)
      error1D = std::sqrt(error1D) / dist;
    else
      error1D = -1.0;

    return Measurement1D(dist, error1D);
  }

  // Compute the error in the covariance matrix projected along the displacement
  // direction (transverse only).
  Measurement1D computeError2D(const GlobalVector& displacement,
      const GlobalError& error) {

    double errValues[4] = {
      error.cxx(), error.cyx(),
      error.cyx(), error.cyy() };
    ROOT::Math::SMatrix<double, 2,2> fastError(errValues, 4);

    double dispValues[2] = {displacement.x(), displacement.y()};
    ROOT::Math::SVector<double, 2> fastDisp(dispValues, 2);

    // from RecoBTag/SecondaryVertex/src/SecondaryVertex.cc
    double dist = ROOT::Math::Mag(fastDisp);
    double error1D = ROOT::Math::Similarity(fastError, fastDisp);

    if (error1D > 0.0 && dist > 1.0e-9)
      error1D = std::sqrt(error1D) / dist;
    else
      error1D = -1.0;

    return Measurement1D(dist, error1D);
  }
}

template<typename T1, typename T2>
class PATDiCandidateIPInfoEmbedder : public edm::EDProducer {
  public:
    typedef PATDiCandidateSystematics<T1,T2> DiCandidate;
    typedef std::vector<DiCandidate> DiCandidateCollection;

    PATDiCandidateIPInfoEmbedder(const edm::ParameterSet& pset);
    virtual ~PATDiCandidateIPInfoEmbedder(){}
    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::InputTag src_;
    std::string d1DirTag_;
    std::string d2DirTag_;
    const TransientTrackBuilder *builder_;
};

template<typename T1, typename T2>
PATDiCandidateIPInfoEmbedder<T1, T2>::PATDiCandidateIPInfoEmbedder(
    const edm::ParameterSet& pset) {
  src_ = pset.getParameter<edm::InputTag>("src");
  d1DirTag_ = pset.getParameter<std::string>("d1DirTag");
  d2DirTag_ = pset.getParameter<std::string>("d2DirTag");
  produces<DiCandidateCollection>();
}

template<typename T1, typename T2>
void PATDiCandidateIPInfoEmbedder<T1,T2>::produce(edm::Event& evt, const edm::EventSetup& es) {
  // Get transient track builder.
  edm::ESHandle<TransientTrackBuilder> myTransientTrackBuilder;
  es.get<TransientTrackRecord>().get("TransientTrackBuilder", myTransientTrackBuilder);
  builder_= myTransientTrackBuilder.product();

  std::auto_ptr<DiCandidateCollection> output(new DiCandidateCollection);

  edm::Handle<edm::View<DiCandidate> > input;
  evt.getByLabel(src_, input);

  output->reserve(input->size());

  for (size_t i = 0; i < input->size(); ++i) {
    const DiCandidate& diCand = input->at(i);
    // Make a copy
    DiCandidate outputCand = diCand;
    // Get the daughters
    const T1& d1 = *diCand.daughter1();
    const T2& d2 = *diCand.daughter2();
    //const reco::Vertex& vtx = *diCand.vertexObject();

    reco::TrackBaseRef track1(d1.track());
    reco::CandidatePtr cand2 = d2.userCand("leadPFCH");
    reco::TrackBaseRef track2;
    if (cand2.isNonnull()) {
      track2 = reco::TrackBaseRef(
          edm::Ptr<reco::PFCandidate>(cand2)->trackRef());
    }

    // impact parameters
    double trk1_TIPVtx = -999;
    double trk2_TIPVtx = -999;
    double trk1_IPVtx = -999;
    double trk2_IPVtx = -999;

    // IP significance
    double trk1_TIPSVtx = -999;
    double trk2_TIPSVtx = -999;
    double trk1_IPSVtx = -999;
    double trk2_IPSVtx = -999;

    // Figure out IP stuff for first track
    if (track1.isNonnull()) {
      const reco::TransientTrack ttrack = transTrack(track1, builder_);
      assert(ttrack.isValid());
      assert(ttrack.field());

      const reco::Candidate& directionCand = *d1.userCand(d1DirTag_);

      GlobalVector direction(directionCand.px(), directionCand.py(),
          directionCand.pz());

      /*
      // Figure IP stuff out for first leg
      std::pair<bool,Measurement1D> ip3D =
        IPTools::signedImpactParameter3D(ttrack, direction, vtx);

      if (ip3D.first) {
        trk1_IPVtx = ip3D.second.value();
        trk1_IPSVtx = ip3D.second.significance();
      }

      std::pair<bool,Measurement1D> tip =
        IPTools::signedTransverseImpactParameter(ttrack, direction, vtx);

      if (tip.first) {
        trk1_TIPVtx = tip.second.value();
        trk1_TIPSVtx = tip.second.significance();
      }
      */
    }

    // Figure out IP stuff for second track
    if (track2.isNonnull()) {
      const reco::TransientTrack ttrack = transTrack(track2, builder_);
      assert(ttrack.isValid());
      assert(ttrack.field());

      const reco::Candidate& directionCand = *d2.userCand(d2DirTag_);

      GlobalVector direction(directionCand.px(), directionCand.py(),
          directionCand.pz());

      /*
      // Figure IP stuff out for first leg
      std::pair<bool,Measurement1D> ip3D =
        IPTools::signedImpactParameter3D(ttrack, direction, vtx);

      if (ip3D.first) {
        trk2_IPVtx = ip3D.second.value();
        trk2_IPSVtx = ip3D.second.significance();
      }

      std::pair<bool,Measurement1D> tip =
        IPTools::signedTransverseImpactParameter(ttrack, direction, vtx);

      if (tip.first) {
        trk2_TIPVtx = tip.second.value();
        trk2_TIPSVtx = tip.second.significance();
      }
      */
    }

    outputCand.addUserFloat("trk1_TIPVtx", trk1_TIPVtx);
    outputCand.addUserFloat("trk2_TIPVtx", trk2_TIPVtx);
    outputCand.addUserFloat("trk1_IPVtx", trk1_IPVtx);
    outputCand.addUserFloat("trk2_IPVtx", trk2_IPVtx);

    outputCand.addUserFloat("trk1_TIPSVtx", trk1_TIPSVtx);
    outputCand.addUserFloat("trk2_TIPSVtx", trk2_TIPSVtx);
    outputCand.addUserFloat("trk1_IPSVtx", trk1_IPSVtx);
    outputCand.addUserFloat("trk2_IPSVtx", trk2_IPSVtx);

    // Track-track quantities
    double dca3D = -1;
    double dca2D = -1;

    double errLeg13D = -1;
    double errLeg23D = -1;
    double sigLeg13D = -1;
    double sigLeg23D = -1;

    double errLeg12D = -1;
    double errLeg22D = -1;
    double sigLeg12D = -1;
    double sigLeg22D = -1;

    //double combinedErr2D = -1;
    //double combinedErr3D = -1;
    double combinedSig2D = -1;
    double combinedSig3D = -1;

    // InterDCA significance
    if (track1.isNonnull() && track2.isNonnull() && track1 != track2) {
      //std::cout << "track1: " << track1.key() << std::endl;
      //std::cout << "track2: " << track2.key() << std::endl;
      const reco::TransientTrack ttrack1 = transTrack(track1, builder_);
      const reco::TransientTrack ttrack2 = transTrack(track2, builder_);

      // Code provided by Alexei Raspereza
      FreeTrajectoryState state1 = ttrack1.impactPointTSCP().theState();
      FreeTrajectoryState state2 = ttrack2.impactPointTSCP().theState();
      //std::cout << "s1: " << state1 << std::endl;
      //std::cout << "s2: " << state2 << std::endl;
      TwoTrackMinimumDistance minDist;
      minDist.calculate(state1, state2);
      assert(minDist.status());

      typedef ROOT::Math::SVector<double, 3> SVector3;
      typedef ROOT::Math::SMatrix<double, 3, 3, ROOT::Math::MatRepSym<double, 3> > SMatrixSym3D;

      std::pair<GlobalPoint,GlobalPoint> pcaMuons = minDist.points();
      GlobalPoint posPCA = pcaMuons.first;
      GlobalPoint negPCA = pcaMuons.second;

      ParticleMass muon_mass = 0.105658;
      float muon_sigma = muon_mass*1.e-6;

      //Creating a KinematicParticleFactory
      KinematicParticleFactoryFromTransientTrack pFactory;

      //initial chi2 and ndf before kinematic fits.
      float chi = 0.;
      float ndf = 0.;
      RefCountedKinematicParticle posMuonPart = pFactory.particle(ttrack1, d1.mass(),chi,ndf,muon_sigma);
      RefCountedKinematicParticle negMuonPart = pFactory.particle(ttrack2, d2.mass(),chi,ndf,muon_sigma);

      SVector3 distanceVector(posPCA.x()-negPCA.x(),
          posPCA.y()-negPCA.y(),
          posPCA.z()-negPCA.z());

      dca3D = ROOT::Math::Mag(distanceVector);

      std::vector<float> vvv(6);

      vvv[0] = posMuonPart->stateAtPoint(posPCA).kinematicParametersError().matrix()(0,0);
      vvv[1] = posMuonPart->stateAtPoint(posPCA).kinematicParametersError().matrix()(0,1);
      vvv[2] = posMuonPart->stateAtPoint(posPCA).kinematicParametersError().matrix()(1,1);
      vvv[3] = posMuonPart->stateAtPoint(posPCA).kinematicParametersError().matrix()(0,2);
      vvv[4] = posMuonPart->stateAtPoint(posPCA).kinematicParametersError().matrix()(1,2);
      vvv[5] = posMuonPart->stateAtPoint(posPCA).kinematicParametersError().matrix()(2,2);

      SMatrixSym3D posPCACov(vvv.begin(),vvv.end());

      vvv[0] = negMuonPart->stateAtPoint(negPCA).kinematicParametersError().matrix()(0,0);
      vvv[1] = negMuonPart->stateAtPoint(negPCA).kinematicParametersError().matrix()(0,1);
      vvv[2] = negMuonPart->stateAtPoint(negPCA).kinematicParametersError().matrix()(1,1);
      vvv[3] = negMuonPart->stateAtPoint(negPCA).kinematicParametersError().matrix()(0,2);
      vvv[4] = negMuonPart->stateAtPoint(negPCA).kinematicParametersError().matrix()(1,2);
      vvv[5] = negMuonPart->stateAtPoint(negPCA).kinematicParametersError().matrix()(2,2);

      SMatrixSym3D negPCACov(vvv.begin(),vvv.end());

      SMatrixSym3D totCov = posPCACov + negPCACov;

      errLeg13D = sqrt(ROOT::Math::Similarity(posPCACov, distanceVector))/dca3D;
      errLeg23D = sqrt(ROOT::Math::Similarity(negPCACov, distanceVector))/dca3D;
      sigLeg13D = dca3D/errLeg13D;
      sigLeg23D = dca3D/errLeg23D;

      double combined3DE = sqrt(ROOT::Math::Similarity(totCov, distanceVector))/dca3D;
      combinedSig3D = dca3D/combined3DE;

      // do 2D
      distanceVector(2) = 0.0;
      dca2D = ROOT::Math::Mag(distanceVector);

      errLeg12D = sqrt(ROOT::Math::Similarity(posPCACov, distanceVector))/dca2D;
      errLeg22D = sqrt(ROOT::Math::Similarity(negPCACov, distanceVector))/dca2D;
      sigLeg12D = dca2D/errLeg12D;
      sigLeg22D = dca2D/errLeg22D;

      double combined2DE = sqrt(ROOT::Math::Similarity(totCov, distanceVector))/dca2D;
      combinedSig2D = dca2D/combined2DE;

    }

    outputCand.addUserFloat("dca3D", dca3D);
    outputCand.addUserFloat("dca2D", dca2D);
    outputCand.addUserFloat("dcaSig13D", sigLeg13D);
    outputCand.addUserFloat("dcaSig23D", sigLeg23D);
    outputCand.addUserFloat("dcaSig3D", combinedSig3D);

    outputCand.addUserFloat("dcaSig12D", sigLeg12D);
    outputCand.addUserFloat("dcaSig22D", sigLeg22D);
    outputCand.addUserFloat("dcaSig2D", combinedSig2D);

    output->push_back(outputCand);
  }

  evt.put(output);
}

typedef PATDiCandidateIPInfoEmbedder<pat::Muon, pat::Tau> PATMuTauIPInfoEmbedder;

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATMuTauIPInfoEmbedder);
