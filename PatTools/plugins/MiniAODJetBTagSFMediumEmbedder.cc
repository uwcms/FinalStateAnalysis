/*
 * Embed PF Jet IDs (see https://twiki.cern.ch/twiki/bin/view/CMS/JetID)
 * into pat::Jets
 *
 * Author: Evan K. Friis, UW Madison
 */


#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/EDProducer.h"

#include "DataFormats/PatCandidates/interface/Jet.h"

// b tag systematics related
#include <TFile.h>
#include <TH2D.h>
#include "TRandom3.h"
#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
#include "CondFormats/BTauObjects/interface/BTagCalibrationReader.h"
#include "boost/filesystem.hpp"

bool applySFM(double eta, bool& isBTagged, float Btag_SF, float Btag_eff){
    TRandom3 rand_;
    rand_ = TRandom3((int)((eta+5)*100000));
    //rand_ = new TRandom3(12345);

    bool newBTag = isBTagged;

    if (Btag_SF == 1) return newBTag; //no correction needed 

    //throw die
    float coin = rand_.Uniform();    
    //std::cout<<"Uniform coin: "<<coin<<std::endl;

    if(Btag_SF > 1){  // use this if SF>1

        if( !isBTagged ) {

            //fraction of jets that need to be upgraded
            float mistagPercent = (1.0 - Btag_SF) / (1.0 - (Btag_SF/Btag_eff) );

            //upgrade to tagged
            if( coin < mistagPercent ) {newBTag = true;}
        }

    }else{  // use this if SF<1

        //downgrade tagged to untagged
        if( isBTagged && coin > Btag_SF ) {newBTag = false;}

    }

    return newBTag;
}



class MiniAODJetBTagSFMediumEmbedder : public edm::EDProducer {
  public:
    MiniAODJetBTagSFMediumEmbedder(const edm::ParameterSet& pset);

    virtual ~MiniAODJetBTagSFMediumEmbedder(){
        delete calib;
        delete reader_light;
        delete reader_light_up;
        delete reader_light_down;
        delete reader;
        delete reader_up;
        delete reader_down;
    }

    void produce(edm::Event& evt, const edm::EventSetup& es);
  private:
    edm::EDGetTokenT<edm::View<pat::Jet> > srcToken_;
    bool doBTag_;
    bool isEffFile_;
    TFile *f_EffMap;
    TH2D *h2_TTEffMapB;
    TH2D *h2_TTEffMapC;
    TH2D *h2_TTEffMapUDSG;
    TH2D *h2_ZJetsEffMapB;
    TH2D *h2_ZJetsEffMapC;
    TH2D *h2_ZJetsEffMapUDSG;


    BTagCalibration *calib;
    BTagCalibrationReader *reader;
    BTagCalibrationReader *reader_up;
    BTagCalibrationReader *reader_down;
    BTagCalibrationReader *reader_light;
    BTagCalibrationReader *reader_light_up;
    BTagCalibrationReader *reader_light_down;
};

MiniAODJetBTagSFMediumEmbedder::MiniAODJetBTagSFMediumEmbedder(const edm::ParameterSet& pset) {
  srcToken_ = consumes<edm::View<pat::Jet> >(pset.getParameter<edm::InputTag>("src"));
  produces<pat::JetCollection>();

  std::string base = std::getenv("CMSSW_BASE");
  std::string fEff =   "/src/FinalStateAnalysis/PatTools/data/htautau_btagging_efficiencies_76x.root";
  std::string path= base+fEff;
  isEffFile_   = boost::filesystem::exists( path  );
  doBTag_ = true;
  //std::cout<<"btag SF producer! isEffFile_ "<<isEffFile_<<"  doBTag_ "<<doBTag_<<std::endl;



  if (!(isEffFile_ && doBTag_)){
    std::cout<<"WARNING::NBTagFiller No efficiency file found!!!"<<std::endl;}

  else {
    // for b tag promote/demote method 2a)
    // https://twiki.cern.ch/twiki/bin/view/CMS/BTagSFMethods#2a_Jet_by_jet_updating_of_the_b
    calib=new BTagCalibration("CSVv2", std::string(std::getenv("CMSSW_BASE"))+"/src/FinalStateAnalysis/PatTools/data/CSVv2_76x.csv");
    reader_light=new BTagCalibrationReader(calib, BTagEntry::OP_MEDIUM, "incl", "central");
    reader_light_up=new BTagCalibrationReader(calib, BTagEntry::OP_MEDIUM, "incl", "up");
    reader_light_down=new BTagCalibrationReader(calib, BTagEntry::OP_MEDIUM, "incl", "down");
    reader=new BTagCalibrationReader(calib, BTagEntry::OP_MEDIUM, "mujets", "central");
    reader_up=new BTagCalibrationReader(calib, BTagEntry::OP_MEDIUM, "mujets", "up");  // sys up
    reader_down=new BTagCalibrationReader(calib, BTagEntry::OP_MEDIUM, "mujets", "down");  // sys down

    std::cout<<"INFO::NBTagFiller using efficiency map"<<std::endl;
    TFile *f_EffMap = new TFile(path.c_str(),"READONLY");
    h2_TTEffMapB    = (TH2D*)f_EffMap->Get("btag_eff_b");
    h2_TTEffMapC    = (TH2D*)f_EffMap->Get("btag_eff_c");
    h2_TTEffMapUDSG = (TH2D*)f_EffMap->Get("btag_eff_oth");
    h2_ZJetsEffMapB    = (TH2D*)f_EffMap->Get("btag_eff_b");
    h2_ZJetsEffMapC    = (TH2D*)f_EffMap->Get("btag_eff_c");
    h2_ZJetsEffMapUDSG = (TH2D*)f_EffMap->Get("btag_eff_oth");
  }
}

void MiniAODJetBTagSFMediumEmbedder::produce(edm::Event& evt, const edm::EventSetup& es) {
  std::auto_ptr<pat::JetCollection> output(new pat::JetCollection);

  edm::Handle<edm::View<pat::Jet> > input;
  evt.getByToken(srcToken_, input);
  output->reserve(input->size());


  for (size_t i = 0; i < input->size(); ++i) {
      pat::Jet jet = input->at(i);
      bool btagged = false;
      bool btaggedup = false;
      bool btaggeddown = false;
      bool pass = false;
      double pt = jet.pt();
      double eta = std::abs(jet.eta());
      //std::cout<<"=====Jet====="<<std::endl;
      //std::cout<<"Jet Pt: "<<pt<<std::endl;
      //std::cout<<"Jet Eta: "<<eta<<std::endl;
      if (pt<20 || std::abs(eta)>2.4) {continue;}
      else if (pt>1000.) {pt=999.;}
      int jetflavor = jet.partonFlavour();
      double SF =0,SFup=0,SFdown=0,eff=0;
      if (jet.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags")>0.80) pass =true;
      if (fabs(jetflavor) == 5) {                // real b-jet
          //std::cout<<"=====Jet Flavor B====="<<std::endl;
          if (pt<30){ 
              //std::cout<<"=====Jet SF"<<std::endl;
              SF = reader->eval(BTagEntry::FLAV_B, eta, 30. );
              SFup = 2*reader_up->eval(BTagEntry::FLAV_B, eta, 30. );
              SFdown = 2*reader_down->eval(BTagEntry::FLAV_B, eta, 30. );
          }
          else if (pt>670){ 
              //std::cout<<"=====Jet SF"<<std::endl;
              SF = reader->eval(BTagEntry::FLAV_B, eta, 669. );
              SFup = 2*reader_up->eval(BTagEntry::FLAV_B, eta, 669. );
              SFdown = 2*reader_down->eval(BTagEntry::FLAV_B, eta, 669. );
          }
          else{ 
              //std::cout<<"=====Jet SF"<<std::endl;
              SF = reader->eval(BTagEntry::FLAV_B, eta,pt );
              SFup = reader_up->eval(BTagEntry::FLAV_B, eta,pt );
              SFdown = reader_down->eval(BTagEntry::FLAV_B, eta,pt );
          }
          eff = 0.6829; 
          //std::cout<<"=====Jet EFF"<<std::endl;
          if (doBTag_ )eff = h2_TTEffMapB->GetBinContent( h2_TTEffMapB->GetXaxis()->FindBin(pt), h2_TTEffMapB->GetYaxis()->FindBin(eta) );
          else if (doBTag_ )eff = h2_ZJetsEffMapB->GetBinContent( h2_ZJetsEffMapB->GetXaxis()->FindBin(pt), h2_ZJetsEffMapB->GetYaxis()->FindBin(eta) );
      }
      else if (fabs(jetflavor) == 4) { 
          //std::cout<<"=====Jet Flavor C====="<<std::endl;
          if (pt<30){ 
              //std::cout<<"=====Jet SF"<<std::endl;
              SF = reader->eval(BTagEntry::FLAV_C, eta, 30. );
              SFup = 2*reader_up->eval(BTagEntry::FLAV_C, eta, 30. );
              SFdown = 2*reader_down->eval(BTagEntry::FLAV_C, eta, 30. );
          }
          else if (pt>670){ 
              //std::cout<<"=====Jet SF"<<std::endl;
              SF = reader->eval(BTagEntry::FLAV_C, eta, 669. );
              SFup = 2*reader_up->eval(BTagEntry::FLAV_C, eta, 669. );
              SFdown = 2*reader_down->eval(BTagEntry::FLAV_C, eta, 669. );
          }
          else{ 
              SF = reader->eval(BTagEntry::FLAV_C, eta,pt );
              SFup = reader_up->eval(BTagEntry::FLAV_C, eta,pt );
              SFdown = reader_down->eval(BTagEntry::FLAV_C, eta,pt );
          }
          eff =0.18;
          //std::cout<<"=====Jet EFF"<<std::endl;
          if (doBTag_) eff = h2_TTEffMapC->GetBinContent( h2_TTEffMapC->GetXaxis()->FindBin(pt), h2_TTEffMapC->GetYaxis()->FindBin(eta) );
          else if (doBTag_) eff = h2_ZJetsEffMapC->GetBinContent( h2_ZJetsEffMapC->GetXaxis()->FindBin(pt), h2_ZJetsEffMapC->GetYaxis()->FindBin(eta) );
      }  
      else {
          //std::cout<<"=====Jet Flavor UDSG====="<<std::endl;
          //std::cout<<"=====Jet SF"<<std::endl;
          SF = reader_light->eval(BTagEntry::FLAV_UDSG, eta, pt );
          SFup = reader_light_up->eval(BTagEntry::FLAV_UDSG, eta, pt );
          SFdown = reader_light_down->eval(BTagEntry::FLAV_UDSG, eta, pt );
          eff =0.012;
          //std::cout<<"=====Jet EFF"<<std::endl;
          if (doBTag_){ 
              eff = h2_TTEffMapUDSG->GetBinContent( h2_TTEffMapUDSG->GetXaxis()->FindBin(pt), h2_TTEffMapUDSG->GetYaxis()->FindBin(eta) );

          }
          else if (doBTag_){ 
              //std::cout<<"=====Jet Pt Bin"<<std::endl;
              //std::cout<<"pt bin: "<<h2_ZJetsEffMapUDSG->GetXaxis()->FindBin(pt)<<std::endl;
              //std::cout<<"=====Jet Eta bin"<<std::endl;
              //std::cout<<"eta bin: "<<h2_ZJetsEffMapUDSG->GetYaxis()->FindBin(eta)<<std::endl;
              eff = h2_ZJetsEffMapUDSG->GetBinContent( h2_ZJetsEffMapUDSG->GetXaxis()->FindBin(pt), h2_ZJetsEffMapUDSG->GetYaxis()->FindBin(eta) );
          }
          //std::cout<<"=====After Jet EFF"<<std::endl;
          //cout<< "Flavor UDSG: EFF" <<endl;
      }

      //std::cout<<"pt: "<<pt<<std::endl;
      //std::cout<<"flavor: "<<fabs(jetflavor)<<std::endl;
      //std::cout<<"SF: "<<SF<<std::endl;
      //std::cout<<"eff: "<<eff<<std::endl;
      btagged = applySFM(eta, pass, SF, eff);
      btaggedup = applySFM(eta, pass, SFup, eff);
      btaggeddown = applySFM(eta, pass, SFdown, eff);

      // Embed the sf info for calculation later
      jet.addUserFloat("btaggedM", float(btagged));
      jet.addUserFloat("btaggedupM", float(btaggedup));
      jet.addUserFloat("btaggeddownM", float(btaggeddown));
      jet.addUserFloat("passM", float(pass));
      jet.addUserFloat("btagSFM", SF);
      jet.addUserFloat("btagSFupM", SFup);
      jet.addUserFloat("btagSFdownM", SFdown);
      jet.addUserFloat("btagEffM", eff);
      output->push_back(jet);
  } // end jet loop

  evt.put(output);
}




#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODJetBTagSFMediumEmbedder);
