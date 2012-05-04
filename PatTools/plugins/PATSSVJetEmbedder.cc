// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/BTauReco/interface/SecondaryVertexTagInfo.h"
#include "DataFormats/BTauReco/interface/TrackIPTagInfo.h"

#include "Math/GenVector/VectorUtil.h"

class PATSSVJetEmbedder : public edm::EDProducer {
   public:

  explicit PATSSVJetEmbedder(const edm::ParameterSet& iConfig):
    src_(iConfig.getParameter<edm::InputTag>("src"))
  {
    produces<pat::JetCollection>();
  }

  ~PATSSVJetEmbedder() {}
   private:



  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
  {
    using namespace edm;
    using namespace reco;

    std::auto_ptr<pat::JetCollection > out(new pat::JetCollection);
    Handle<pat::JetCollection > cands;

    if(iEvent.getByLabel(src_,cands))
      for(unsigned int  i=0;i!=cands->size();++i){
        pat::Jet jet = cands->at(i);

   double btagSSVHEPOS[5]={-777,-777,-777,-777,-777};
   double btagSSVHPPOS[5]={-777,-777,-777,-777,-777};
   double btagSSVHENEG[5]={-777,-777,-777,-777,-777};
   double btagSSVHPNEG[5]={-777,-777,-777,-777,-777};
   double massSSV=-777;
   unsigned int nSSVPOS=0;
   unsigned int nSSVNEG=0;
   unsigned int nTracks_SSVPOS[5]={0,0,0,0,0}; // Up to 5 just to be safe
   double flightDistancePOS[5]={-777,-777,-777,-777,-777};
   double errorFlightDistancePOS[5]={-777,-777,-777,-777,-777};
   unsigned int nTracks_SSVNEG[5]={0,0,0,0,0};
   double flightDistanceNEG[5]={-777,-777,-777,-777,-777};
   double errorFlightDistanceNEG[5]={-777,-777,-777,-777,-777};


            const reco::SecondaryVertexTagInfo* secInfo = jet.tagInfoSecondaryVertex("secondaryVertex");
            if (secInfo && secInfo->vertexTracks().size()>0) {
                  // Loop on all tracks of all secondary vertices to determine the mass
                  double enall = 0.;
                  double pxall = 0.;
                  double pyall = 0.;
                  double pzall = 0.;
                  for (unsigned int it=0; it<secInfo->vertexTracks().size(); ++it) {
                        double px = secInfo->vertexTracks()[it]->px();
                        double py = secInfo->vertexTracks()[it]->py();
                        double pz = secInfo->vertexTracks()[it]->pz();
                        enall += sqrt(px*px+py*py+pz*pz+0.1396*0.1396);
                        pxall += px;
                        pyall += py;
                        pzall += pz;
                  }
                  double mass2 = enall*enall-pxall*pxall-pyall*pyall-pzall*pzall;
                  if (mass2>0.) massSSV = sqrt(mass2);
		  nSSVPOS=secInfo->nVertices();
                  for (unsigned int isv=0; isv<secInfo->nVertices(); ++isv) {
                        nTracks_SSVPOS[isv]=(secInfo->nVertexTracks(isv));
                        flightDistancePOS[isv]=(secInfo->flightDistance(isv).value());
                        errorFlightDistancePOS[isv]=(secInfo->flightDistance(isv).error());
                  }
            }

            const reco::SecondaryVertexTagInfo* secNegInfo = jet.tagInfoSecondaryVertex("secondaryVertexNegative");

            if (secNegInfo && secNegInfo->vertexTracks().size()>0) {
		  nSSVNEG=secNegInfo->nVertices();
                  for (unsigned int isv=0; isv<secNegInfo->nVertices(); ++isv) {
                        nTracks_SSVNEG[isv]=(secNegInfo->nVertexTracks(isv));
                        flightDistanceNEG[isv]=(secNegInfo->flightDistance(isv).value());
                        errorFlightDistanceNEG[isv]=(secNegInfo->flightDistance(isv).error());
                  }
            }


            for (unsigned int isv=0; isv<nSSVPOS; ++isv) {
                  if (nTracks_SSVPOS[isv]<2) continue;
                  if (errorFlightDistancePOS[isv]<=0.) continue;
                  if (flightDistancePOS[isv]<0.) continue;
                  btagSSVHEPOS[isv]=log(1.+flightDistancePOS[isv]/errorFlightDistancePOS[isv]);
	    }

	     for (unsigned int isv=0; isv<nSSVNEG; ++isv) {
                  if (nTracks_SSVNEG[isv]<2) continue;
                  if (errorFlightDistanceNEG[isv]<=0.) continue;
                  if (flightDistanceNEG[isv]>0.) continue;
                  btagSSVHENEG[isv]=-log(1.-flightDistanceNEG[isv]/errorFlightDistanceNEG[isv]);
            }



            for (unsigned int isv=0; isv<nSSVPOS; ++isv) {
                  if (nTracks_SSVPOS[isv]<3) continue;
                  if (errorFlightDistancePOS[isv]<=0.) continue;
                  if (flightDistancePOS[isv]<0.) continue;
                  btagSSVHPPOS[isv]=log(1.+flightDistancePOS[isv]/errorFlightDistancePOS[isv]);
            }

             for (unsigned int isv=0; isv<nSSVNEG; ++isv) {
                  if (nTracks_SSVNEG[isv]<3) continue;
                  if (errorFlightDistanceNEG[isv]<=0.) continue;
                  if (flightDistanceNEG[isv]>0.) continue;
                  btagSSVHPNEG[isv]=-log(1.-flightDistanceNEG[isv]/errorFlightDistanceNEG[isv]);
            }
        jet.addUserFloat("nSSV",nSSVNEG);
        jet.addUserFloat("nNegativeSSV",nSSVPOS);
        jet.addUserFloat("massSSV",massSSV);
        jet.addUserFloat("btagSSVHE",btagSSVHEPOS[0]);
        jet.addUserFloat("btagSSVHP",btagSSVHPPOS[0]);
        jet.addUserFloat("nTracksSSV",nTracks_SSVPOS[0]);
        jet.addUserFloat("errorFlightDistance",errorFlightDistancePOS[0]);
        jet.addUserFloat("flightDistance",flightDistancePOS[0]);
        jet.addUserFloat("btagSSVHE2",btagSSVHEPOS[1]);
       	jet.addUserFloat("btagSSVHP2",btagSSVHPPOS[1]);
        jet.addUserFloat("nTracksSSV2",nTracks_SSVPOS[1]);
        jet.addUserFloat("errorFlightDistance2",errorFlightDistancePOS[1]);
        jet.addUserFloat("flightDistance2",flightDistancePOS[1]);

        jet.addUserFloat("btagNEGSSVHE",btagSSVHENEG[0]);
        jet.addUserFloat("btagNEGSSVHP",btagSSVHPNEG[0]);
        jet.addUserFloat("nTracksNEGSSV",nTracks_SSVNEG[0]);
        jet.addUserFloat("errorFlightDistanceNEG",errorFlightDistanceNEG[0]);
        jet.addUserFloat("flightDistanceNEG",flightDistanceNEG[0]);

        out->push_back(jet);

	}



    iEvent.put(out);

  }

      // ----------member data ---------------------------
      edm::InputTag src_;
};

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/PluginManager/interface/ModuleDef.h"

DEFINE_FWK_MODULE(PATSSVJetEmbedder);
