/*
 * Embed information about muons inside jets.
 *
 * TODO: use user cands?
 *
 * Author: Maria Cepeda (UW)
 *
 */

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

#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidate.h"
#include "DataFormats/MuonReco/interface/MuonSelectors.h"
#include "Math/GenVector/VectorUtil.h"

// Looks for a Muon in the Jet, and saves the highest ptrel one. Future improvement: save all...
// Electron skeleton added, but useless without ID requirements on it



class PATMuonInJetEmbedder : public edm::EDProducer {
  public:

    explicit PATMuonInJetEmbedder(const edm::ParameterSet& iConfig):
      src_(iConfig.getParameter<edm::InputTag>("src")),
      srcVertices_(iConfig.getParameter<edm::InputTag>("srcVertex"))
  {
    produces<pat::JetCollection>();
  }

    ~PATMuonInJetEmbedder() {}
  private:



    virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
    {
      using namespace edm;
      using namespace reco;

      std::unique_ptr<pat::JetCollection > out(new pat::JetCollection);
      Handle<pat::JetCollection > cands;

      edm::Handle<reco::VertexCollection> vertexHandle;
      iEvent.getByLabel(srcVertices_, vertexHandle);

      if(iEvent.getByLabel(src_,cands))
        for(unsigned int  i=0;i!=cands->size();++i){
          pat::Jet jet = cands->at(i);

          double MuonInJetPt=-10;
          double MuonInJetCharge=0;
          double MuonInJetPhi=-10;
          double MuonInJetEta=-10;
          double MuonInJetPtRel=0;
          double MuonInJetDXY=1000;
          double MuonInJetDZ=1000;
          double MuonInJetIsoABS=-10;
          double MuonInJetDXYERR=1000;
          double MuonInJetDZERR=1000;
          double ElectronInJetPt=-10;
          double ElectronInJetCharge=0;
          double ElectronInJetPhi=-10;
          double ElectronInJetEta=-10;
          double ElectronInJetPtRel=0;

          int nConst=jet.nConstituents();

          for(int i=0; i<nConst; i++){
            reco::PFCandidatePtr leptoncand=jet.getPFConstituent(i);

            if(abs(leptoncand->pdgId())==13)
            {
              reco::MuonRef muref = leptoncand->muonRef();
              if (!muref->isGlobalMuon()) continue;
              if (!muref->isTrackerMuon()) continue;

              double dxy = 100; double dz=100;  double dxyError=100; double dzError=100;
              if(vertexHandle->size()>=1){
                dxy=muref->innerTrack()->dxy(vertexHandle->at(0).position());
                dz = muref->innerTrack()->dz(vertexHandle->at(0).position());
                dxyError= muref->innerTrack()->dxyError();
                dzError = muref->innerTrack()->dzError();

              }
              if (fabs(dxy)>0.2) continue;
              if(fabs(dz)>0.2) continue;
              double normalizedChi2 = muref->globalTrack()->normalizedChi2();
              if (normalizedChi2>10.) continue;
              int trackerHits = muref->globalTrack()->hitPattern().numberOfValidTrackerHits();
              if (trackerHits<11) continue;
              int pixelHits = muref->globalTrack()->hitPattern().numberOfValidPixelHits();
              if (pixelHits<1) continue;
              int muonHits = muref->globalTrack()->hitPattern().numberOfValidMuonHits();
              if (muonHits<1) continue;

              int nMatches = muref->numberOfMatches();
              if (nMatches<2) continue;

              double ptrelcand=sqrt(pow(leptoncand->p(),2) - pow(leptoncand->px()*jet.px()+leptoncand->py()*jet.py()+leptoncand->pz()*jet.pz(),2)/pow(jet.p(),2));
              if(ptrelcand>MuonInJetPtRel){
                MuonInJetPt=leptoncand->pt();
                MuonInJetEta=leptoncand->eta();
                MuonInJetPhi=leptoncand->phi();
                MuonInJetCharge=leptoncand->charge();
                MuonInJetPtRel=ptrelcand*leptoncand->charge();
                MuonInJetDXY=dxy;
                MuonInJetDZ=dz;
                MuonInJetDXYERR= dxyError;
                MuonInJetDZERR= dzError;
                MuonInJetIsoABS=(muref->isolationR03().sumPt + muref->isolationR03().emEt + muref->isolationR03().hadEt);
              }
            }
            if(abs(leptoncand->pdgId())==11)
            {
              double ptrelcand=sqrt(pow(leptoncand->p(),2) - pow(leptoncand->px()*jet.px()+leptoncand->py()*jet.py()+leptoncand->pz()*jet.pz(),2)/pow(jet.p(),2));
              if(ptrelcand>ElectronInJetPtRel){
                ElectronInJetPt=leptoncand->pt();
                ElectronInJetEta=leptoncand->eta();
                ElectronInJetPhi=leptoncand->phi();
                ElectronInJetCharge=leptoncand->charge();
                ElectronInJetPtRel=ptrelcand*leptoncand->charge();
              }
            }
          }

          jet.addUserFloat("MuonInJetPt",MuonInJetPt);
          jet.addUserFloat("ElectronInJetPt",ElectronInJetPt);
          jet.addUserFloat("MuonInJetPhi",MuonInJetPhi);
          jet.addUserFloat("ElectronInJetPhi",ElectronInJetPhi);
          jet.addUserFloat("MuonInJetEta",MuonInJetEta);
          jet.addUserFloat("ElectronInJetEta",ElectronInJetEta);
          jet.addUserFloat("MuonInJetCharge",MuonInJetCharge);
          jet.addUserFloat("ElectronInJetCharge",ElectronInJetCharge);
          jet.addUserFloat("MuonInJetPtRel",MuonInJetPtRel);
          jet.addUserFloat("ElectronInJetPtRel",ElectronInJetPtRel);
          jet.addUserFloat("MuonInJetDXY",MuonInJetDXY);
          jet.addUserFloat("MuonInJetDXYERR",MuonInJetDXYERR);
          jet.addUserFloat("MuonInJetDZ",MuonInJetDZ);
          jet.addUserFloat("MuonInJetDZERR",MuonInJetDZERR);
          jet.addUserFloat("MuonInJetIsoABS",MuonInJetIsoABS);

          out->push_back(jet);
        }

      iEvent.put(std::move(out));

    }

    // ----------member data ---------------------------
    edm::InputTag src_;
    edm::InputTag srcVertices_;
};

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/PluginManager/interface/ModuleDef.h"

DEFINE_FWK_MODULE(PATMuonInJetEmbedder);
