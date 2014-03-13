#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "RecoBTag/SecondaryVertex/interface/TrackKinematics.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/BTauReco/interface/TrackIPTagInfo.h"
#include "DataFormats/BTauReco/interface/SecondaryVertexTagInfo.h"
#include "RecoBTag/SecondaryVertex/interface/TrackSelector.h"
#include "RecoBTag/SecondaryVertex/interface/TrackSorting.h"
#include "RecoBTag/SecondaryVertex/interface/SecondaryVertex.h"
#include "RecoBTag/SecondaryVertex/interface/VertexFilter.h"
#include "RecoBTag/SecondaryVertex/interface/VertexSorting.h"


class PATCSVJetEmbedder : public edm::EDProducer {
    public:

        PATCSVJetEmbedder(const edm::ParameterSet& pset);
        virtual ~PATCSVJetEmbedder(){}
        void produce(edm::Event& evt, const edm::EventSetup& es);
    private:
        edm::InputTag jet_;

};

PATCSVJetEmbedder::PATCSVJetEmbedder(
        const edm::ParameterSet& pset):
        jet_(pset.getParameter<edm::InputTag>("src"))
            {
             produces<pat::JetCollection>();
    }

void PATCSVJetEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  edm::Handle<pat::JetCollection> jets;
  evt.getByLabel(jet_, jets);

  std::auto_ptr<pat::JetCollection> out(new pat::JetCollection);
  out->reserve(jets->size());

  for(unsigned int i=0;i!=jets->size();++i){
        pat::Jet jet = jets->at(i);

        const reco::SecondaryVertexTagInfo* secInfo = jet.tagInfoSecondaryVertex("secondaryVertex");
        double sumVertexMass=0, sumWeightedVertexMass=0;
        double sumVertexPt=0, sumWeightedVertexPt=0;
        double quality=-1;
        double sumWeights=0;
        double numberTracks=0;
        double vertexPt2=0;
        double correctedVertexMass=0;

        if (secInfo && secInfo->nVertices() > 0) {


                const reco::Vertex &vertex = secInfo->secondaryVertex(0);
                GlobalVector dir = secInfo->flightDirection(0);
                reco::TrackKinematics vertexKinematics(vertex);

                math::XYZTLorentzVector weightedVertexSum = vertexKinematics.weightedVectorSum();
                sumWeightedVertexMass = weightedVertexSum.M();
                sumWeightedVertexPt = weightedVertexSum.Pt();
                sumWeights=vertexKinematics.sumOfWeights();
                numberTracks=vertexKinematics.numberOfTracks();

                math::XYZTLorentzVector vertexSum = vertexKinematics.vectorSum();
                sumVertexMass = vertexSum.M();
                sumVertexPt = vertexSum.Pt();

                quality=vertex.normalizedChi2();

                vertexPt2 =math::XYZVector(dir.x(), dir.y(), dir.z()).Cross(weightedVertexSum).Mag2() / dir.mag2();
                correctedVertexMass=std::sqrt(sumWeightedVertexMass*sumWeightedVertexMass+vertexPt2) + std::sqrt(vertexPt2);
         }
        jet.addUserFloat("mass_SV_unweighted",sumVertexMass);
        jet.addUserFloat("mass_SV_weighted",sumWeightedVertexMass);
        jet.addUserFloat("pt_SV_unweighted",sumVertexPt);
        jet.addUserFloat("pt_SV_weighted",sumWeightedVertexPt);
        jet.addUserFloat("normChi2_SV",quality);
        jet.addUserFloat("sumOfWeights_SV",sumWeights);
        jet.addUserFloat("nTracks_SV",numberTracks);
        jet.addUserFloat("mass_SV_corrected",correctedVertexMass);
        jet.addUserFloat("mass_SV_correctin",vertexPt2);

        out->push_back(jet);

   }
  evt.put(out);
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATCSVJetEmbedder);
