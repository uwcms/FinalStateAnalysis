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
          double mass_SSV=-777;
          double mass_SSVNEG=-777;

          double massD_SSV=-777;
          double massD_SSVNEG=-777;

          double massD0_SSV=-777;
          double massD0_SSVNEG=-777;

          unsigned int nSSVNEG=0, nSSVPOS=0;
          unsigned int nTracks_SSVPOS[5]={0,0,0,0,0}; // Up to 5 just to be safe
          double flightDistancePOS[5]={-777,-777,-777,-777,-777};
          double errorFlightDistancePOS[5]={-777,-777,-777,-777,-777};
          unsigned int nTracks_SSVNEG[5]={0,0,0,0,0};
          double flightDistanceNEG[5]={-777,-777,-777,-777,-777};
          double errorFlightDistanceNEG[5]={-777,-777,-777,-777,-777};

          int chargeSSV=0;
          int chargeSSVNEG=0;

          double track1_px=-777, track1_py=-777, track1_pz=-777;    // Seriously, this has to be redone and coded as a vector. Is there a userVector thing?
          double track2_px=-777, track2_py=-777, track2_pz=-777;
          double track3_px=-777, track3_py=-777, track3_pz=-777;

          double trackNeg1_px=-777, trackNeg1_py=-777, trackNeg1_pz=-777;
          double trackNeg2_px=-777, trackNeg2_py=-777, trackNeg2_pz=-777;
          double trackNeg3_px=-777, trackNeg3_py=-777, trackNeg3_pz=-777;

          int track1_charge=-777, track2_charge=-777, track3_charge=-777;
          int trackNeg1_charge=-777, trackNeg2_charge=-777, trackNeg3_charge=-777;


          const reco::SecondaryVertexTagInfo* secInfo = jet.tagInfoSecondaryVertex("secondaryVertex");
          if (secInfo && secInfo->vertexTracks().size()>0) {
            // Loop on all tracks of all secondary vertices to determine the mass
            double enall = 0.;
            double pxall = 0.;
            double pyall = 0.;
            double pzall = 0.;
            double enD = 0.;
            double enD0_1 = 0.;
            double enD0_2 = 0.;

            int chargeSSV=0;   // first find charge of vertex (to see if it is D+ or D-)

            for (unsigned int it=0; it<secInfo->vertexTracks().size(); ++it) {
              chargeSSV+=secInfo->vertexTracks()[it]->charge();
            }

            for (unsigned int it=0; it<secInfo->vertexTracks().size(); ++it) {
              double px = secInfo->vertexTracks()[it]->px();
              double py = secInfo->vertexTracks()[it]->py();
              double pz = secInfo->vertexTracks()[it]->pz();
              enall += sqrt(px*px+py*py+pz*pz+0.1396*0.1396);    // mass v1: everything is a pion
              pxall += px;
              pyall += py;
              pzall += pz;

              if(secInfo->vertexTracks().size()==3 && abs(chargeSSV)==1){  // check if this is a 3 track decay with global charge -1 or +1
                double mass_hadron=0.1396;
                if(secInfo->vertexTracks()[it]->charge()*chargeSSV<0) mass_hadron=0.493677;  // (pi-,pi-,ka+) or (pi+,pi+,k-)
                enD += sqrt(px*px+py*py+pz*pz+mass_hadron*mass_hadron);    // mass v2:  2 pions and a kaon
              }

              if(secInfo->vertexTracks().size()==2) { // Look for D0. This is more complicated (kpi, which is k and which is pi?)
                double mass_pi=0.1396, mass_k=0.493677;
                if(it==0){
                  enD0_1 += sqrt(px*px+py*py+pz*pz+mass_pi*mass_pi);    // mass v3: pi +ka
                  enD0_2 += sqrt(px*px+py*py+pz*pz+mass_k*mass_k);
                } else if(it==1){
                  enD0_1 += sqrt(px*px+py*py+pz*pz+mass_k*mass_k);    // mass v3: pi + ka
                  enD0_2 += sqrt(px*px+py*py+pz*pz+mass_pi*mass_pi);
                }
              }

              if(it==0) {track1_px=px; track1_py=py; track1_pz=pz; track1_charge=secInfo->vertexTracks()[it]->charge();}
              else if (it==1) {track2_px=px; track2_py=py; track2_pz=pz; track2_charge=secInfo->vertexTracks()[it]->charge();}
              else if (it==2) {track3_px=px; track3_py=py; track3_pz=pz; track3_charge=secInfo->vertexTracks()[it]->charge();}
            }
            double mass2 = enall*enall-pxall*pxall-pyall*pyall-pzall*pzall;
            if (mass2>0.) mass_SSV = sqrt(mass2);

            double mass2D = enD*enD-pxall*pxall-pyall*pyall-pzall*pzall;
            if (mass2D>0.) massD_SSV = sqrt(mass2D);

            double mass2D0_1 = enD0_1*enD0_1-pxall*pxall-pyall*pyall-pzall*pzall;
            if (mass2D0_1>0.) mass2D0_1 = sqrt(mass2D0_1);

            double mass2D0_2 = enD0_2*enD0_2-pxall*pxall-pyall*pyall-pzall*pzall;
            if (mass2D0_2>0.) mass2D0_2 = sqrt(mass2D0_2);

            if( fabs(mass2D0_1-1.87)<0.05 && fabs(mass2D0_2-1.87)>0.05)  massD0_SSV=mass2D0_1;
            else if ( fabs(mass2D0_2-1.87)<0.05 && fabs(mass2D0_1-1.87)>0.05)  massD0_SSV=mass2D0_2;

            nSSVPOS=secInfo->nVertices();
            for (unsigned int isv=0; isv<secInfo->nVertices(); ++isv) {
              nTracks_SSVPOS[isv]=(secInfo->nVertexTracks(isv));
              flightDistancePOS[isv]=(secInfo->flightDistance(isv).value());
              errorFlightDistancePOS[isv]=(secInfo->flightDistance(isv).error());
            }
          }

          const reco::SecondaryVertexTagInfo* secNegInfo = jet.tagInfoSecondaryVertex("secondaryVertexNegative");

          if (secNegInfo && secNegInfo->vertexTracks().size()>0) {
            // Loop on all tracks of all secondary vertices to determine the mass
            double enall = 0.;
            double pxall = 0.;
            double pyall = 0.;
            double pzall = 0.;
            double enD = 0.;
            double enD0_1 = 0.;
            double enD0_2 = 0.;

            int chargeSSVNEG=0;   // first find charge of vertex (to see if it is D+ or D-)

            for (unsigned int it=0; it<secNegInfo->vertexTracks().size(); ++it) {
              chargeSSVNEG+=secNegInfo->vertexTracks()[it]->charge();
            }

            for (unsigned int it=0; it<secNegInfo->vertexTracks().size(); ++it) {
              double px = secNegInfo->vertexTracks()[it]->px();
              double py = secNegInfo->vertexTracks()[it]->py();
              double pz = secNegInfo->vertexTracks()[it]->pz();
              enall += sqrt(px*px+py*py+pz*pz+0.1396*0.1396);    // mass v1: everything is a pion
              pxall += px;
              pyall += py;
              pzall += pz;

              if(secNegInfo->vertexTracks().size()==3 && abs(chargeSSVNEG)==1){  // check if this is a 3 track decay with global charge -1 or +1
                double mass_hadron=0.1396;
                if(secNegInfo->vertexTracks()[it]->charge()*chargeSSVNEG<0) mass_hadron=0.493677;  // (pi-,pi-,ka+) or (pi+,pi+,k-)
                enD += sqrt(px*px+py*py+pz*pz+mass_hadron*mass_hadron);    // mass v2:  2 pions and a kaon
              }

              if(secNegInfo->vertexTracks().size()==2) { // Look for D0. This is more complicated (kpi, which is k and which is pi?)
                double mass_pi=0.1396, mass_k=0.493677;
                if(it==0){
                  enD0_1 += sqrt(px*px+py*py+pz*pz+mass_pi*mass_pi);    // mass v3: pi +ka
                  enD0_2 += sqrt(px*px+py*py+pz*pz+mass_k*mass_k);
                } else if(it==1){
                  enD0_1 += sqrt(px*px+py*py+pz*pz+mass_k*mass_k);    // mass v3: pi + ka
                  enD0_2 += sqrt(px*px+py*py+pz*pz+mass_pi*mass_pi);
                }
              }

              if(it==0) {track1_px=px; track1_py=py; track1_pz=pz; track1_charge=secNegInfo->vertexTracks()[it]->charge();}
              else if (it==1) {track2_px=px; track2_py=py; track2_pz=pz; track2_charge=secNegInfo->vertexTracks()[it]->charge();}
              else if (it==2) {track3_px=px; track3_py=py; track3_pz=pz; track3_charge=secNegInfo->vertexTracks()[it]->charge();}
            }
            double mass2 = enall*enall-pxall*pxall-pyall*pyall-pzall*pzall;
            if (mass2>0.) mass_SSVNEG = sqrt(mass2);

            double mass2D = enD*enD-pxall*pxall-pyall*pyall-pzall*pzall;
            if (mass2D>0.) massD_SSVNEG = sqrt(mass2D);

            double mass2D0_1 = enD0_1*enD0_1-pxall*pxall-pyall*pyall-pzall*pzall;
            if (mass2D0_1>0.) mass2D0_1 = sqrt(mass2D0_1);

            double mass2D0_2 = enD0_2*enD0_2-pxall*pxall-pyall*pyall-pzall*pzall;
            if (mass2D0_2>0.) mass2D0_2 = sqrt(mass2D0_2);

            if( fabs(mass2D0_1-1.87)<0.05 && fabs(mass2D0_2-1.87)>0.05)  massD0_SSVNEG=mass2D0_1;
            else if ( fabs(mass2D0_2-1.87)<0.05 && fabs(mass2D0_1-1.87)>0.05)  massD0_SSVNEG=mass2D0_2;

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
          jet.addUserFloat("nSSV",nSSVPOS);
          jet.addUserFloat("nNegativeSSV",nSSVNEG);
          jet.addUserFloat("mass_SSV",mass_SSV);
          jet.addUserFloat("mass_SSVNEG",mass_SSVNEG);
          jet.addUserFloat("massD_SSV",massD_SSV);
          jet.addUserFloat("massD_SSVNEG",massD_SSVNEG);

          jet.addUserFloat("chargeSSV",chargeSSV);
          jet.addUserFloat("chargeSSVNEG",chargeSSVNEG);

          jet.addUserFloat("massD0_SSV",massD0_SSV);
          jet.addUserFloat("massD0_SSVNEG",massD0_SSVNEG);

          jet.addUserFloat("SSVNeg_track1_px",trackNeg1_px);
          jet.addUserFloat("SSVNeg_track1_py",trackNeg1_py);
          jet.addUserFloat("SSVNeg_track1_pz",trackNeg1_pz);
          jet.addUserFloat("SSVNeg_track1_charge",trackNeg1_charge);

          jet.addUserFloat("SSV_track1_px",track1_px);
          jet.addUserFloat("SSV_track1_py",track1_py);
          jet.addUserFloat("SSV_track1_pz",track1_pz);
          jet.addUserFloat("SSV_track1_charge",track1_charge);

          jet.addUserFloat("SSVNeg_track2_px",trackNeg2_px);
          jet.addUserFloat("SSVNeg_track2_py",trackNeg2_py);
          jet.addUserFloat("SSVNeg_track2_pz",trackNeg2_pz);
          jet.addUserFloat("SSVNeg_track2_charge",trackNeg2_charge);

          jet.addUserFloat("SSV_track2_px",track2_px);
          jet.addUserFloat("SSV_track2_py",track2_py);
          jet.addUserFloat("SSV_track2_pz",track2_pz);
          jet.addUserFloat("SSV_track2_charge",track2_charge);

          jet.addUserFloat("SSVNeg_track3_px",trackNeg3_px);
          jet.addUserFloat("SSVNeg_track3_py",trackNeg3_py);
          jet.addUserFloat("SSVNeg_track3_pz",trackNeg3_pz);
          jet.addUserFloat("SSVNeg_track3_charge",trackNeg3_charge);

          jet.addUserFloat("SSV_track3_px",track3_px);
          jet.addUserFloat("SSV_track3_py",track3_py);
          jet.addUserFloat("SSV_track3_pz",track3_pz);
          jet.addUserFloat("SSV_track3_charge",track3_charge);

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
