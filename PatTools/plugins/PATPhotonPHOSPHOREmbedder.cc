/*
 * Embed the rochester corrections and associated errors in pat::Muons
 *
 * Author: Lindsey A. Gray, UW Madison
 *
 */

#include "FinalStateAnalysis/PatTools/interface/PhosphorCorrectorFunctor.hh"
#include <algorithm>

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

#include <stdio.h>

//extract necessary pieces of namespaces
using edm::EDProducer;
using edm::ParameterSet;
using edm::EventSetup;
using edm::Event;
using edm::InputTag;
using edm::FileInPath;

using pat::Photon;
using pat::PhotonRef;
using pat::PhotonCollection;

using zgamma::PhosphorCorrectionFunctor;
typedef PhosphorCorrectionFunctor correction;

class CorrectorBase {
protected:
  correction* thisCorr;
public:
  CorrectorBase(const std::string& file,bool doCat) { 
    thisCorr = new correction(file.c_str(),doCat);
  }
  virtual ~CorrectorBase() { delete thisCorr; }
  virtual double correct(const Photon&) const = 0;
};

template<unsigned year, bool isMC>
class Corrector: public CorrectorBase{
public:
  Corrector(const std::string& file,bool doCat):CorrectorBase(file,doCat) {}
  // E dE
  double correct(const Photon& ph) const {
    // since this is a compile time constant it should be
    // optimized away
    double Ecorr = 0;
    if( isMC ) {
      reco::GenParticleRef gref = ph.genParticleRef();
      double gen_energy = 0;
      if( gref.isAvailable() && gref.isNonnull() )
	gen_energy = gref->energy();
      
      Ecorr = thisCorr->GetCorrEnergyMC(ph.r9(),year,
					ph.pt(),ph.eta(),
					gen_energy);
    } else {
      Ecorr = thisCorr->GetCorrEnergyData(ph.r9(),year,ph.pt(),ph.eta());
    }
    return Ecorr;
  }  
};

typedef Corrector<2012,false> phosphor2012Data;
typedef Corrector<2012,true> phosphor2012MC;
typedef Corrector<2011,false> phosphor2011Data;
typedef Corrector<2011,true> phosphor2011MC;

class PATPhotonPHOSPHOREmbedder : public EDProducer {
public:
  PATPhotonPHOSPHOREmbedder(const ParameterSet& pset);
  virtual ~PATPhotonPHOSPHOREmbedder(){ delete corrector_; }
  void produce(Event& evt, const EventSetup& es);
private:
  InputTag _src,_pvSrc;
  CorrectorBase* corrector_;
  unsigned _year;
};

PATPhotonPHOSPHOREmbedder::
PATPhotonPHOSPHOREmbedder(const ParameterSet& pset) {

  _src = pset.getParameter<InputTag>("src");    
  _year = pset.getParameter<unsigned>("year");
  bool isMC = pset.getParameter<bool>("isMC"); 
  bool r9cats = pset.getParameter<bool>("r9Categories");
  FileInPath card = pset.getParameter<FileInPath>("dataCard");
  
  switch(_year) {
  case 2011:
    if( isMC ) corrector_ = new phosphor2011MC(card.fullPath(),r9cats);
    else       corrector_ = new phosphor2011Data(card.fullPath(),r9cats);
    break;
  case 2012:
    if( isMC ) corrector_ = new phosphor2012MC(card.fullPath(),r9cats);
    else       corrector_ = new phosphor2012Data(card.fullPath(),r9cats);
    break;
  default:
    throw cms::Exception("InvalidRunYear") 
      << "You are requesting a PHOSPHOR run year that does not exist!" 
      << std::endl;
  }

  produces<PhotonCollection>();
}

void PATPhotonPHOSPHOREmbedder::produce(Event& evt, 
						 const EventSetup& es) {

  std::unique_ptr<PhotonCollection> out(new PhotonCollection);

  edm::Handle<PhotonCollection> phos;
  evt.getByLabel(_src,phos);

  PhotonCollection::const_iterator b = phos->begin();
  PhotonCollection::const_iterator i = b;
  PhotonCollection::const_iterator e = phos->end();
  
  for( ; i != e; ++i ) {
    Photon cPho = *i;
    double corrE = corrector_->correct(cPho);
    
    math::XYZVector newMom = cPho.momentum().unit()*corrE;
    math::XYZTLorentzVector corrp4(newMom.x(),newMom.y(),newMom.z(),corrE);

    cPho.addUserData<math::XYZTLorentzVector>(Form("p4_PHOSPHOR_%i",_year),
					      corrp4);

    out->push_back(cPho);
  }
  
  evt.put(std::move(out));
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(PATPhotonPHOSPHOREmbedder);
