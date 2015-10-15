#include "FinalStateAnalysis/DataAlgos/interface/helpers.h"

#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "FWCore/Utilities/interface/Exception.h"
#include "PhysicsTools/HepMCCandAlgos/interface/GenParticlesHelper.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"

#include "CommonTools/UtilAlgos/interface/MCMatchSelector.h"
#include "CommonTools/UtilAlgos/interface/MatchByDRDPt.h"
#include "CommonTools/UtilAlgos/interface/MatchLessByDPt.h"
#include "DataFormats/Math/interface/deltaR.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "TMatrixD.h"
#include "TMath.h"
#include <vector>
//#include <iostream>

namespace fshelpers {

  double xySignficance(const reco::Candidate::Vector& vector,
                       const TMatrixD& covariance) {
    // Instead of playing around w/ vector types to get ROOT
    // to do this for us, just do it manually.
    double vx = vector.x();
    double vy = vector.y();
    double mag2 = vx*vx + vy*vy;
    double mag = TMath::Sqrt(mag2);

    if (mag < 1.0e-9)
      return -1;

    // vT dot cov dot v
    double c00 = covariance(0,0);
    double c01 = covariance(0,1);
    double c10 = covariance(1,0);
    double c11 = covariance(1,1);

    double covDotVx = (c00*vx + c01*vy);
    double covDotVy = (c10*vx + c11*vy);

    double vTdotCovDotV = vx*covDotVx + vy*covDotVy;

    if (vTdotCovDotV < 0)
      return -2;

    // compute error pointing along the vector
    double error = TMath::Sqrt(vTdotCovDotV)/mag;

    return mag/error;
  }

  // By C. Veelken
  std::pair<double, double> pZeta( const reco::Candidate::LorentzVector& leg1,
                                   const reco::Candidate::LorentzVector& leg2, double metPx, double metPy) {
    //std::cout << "<CompositePtrCandidateT1T2MEtAlgorithm::compZeta>:" << std::endl;

    double leg1x = cos(leg1.phi());
    double leg1y = sin(leg1.phi());
    double leg2x = cos(leg2.phi());
    double leg2y = sin(leg2.phi());
    double zetaX = leg1x + leg2x;
    double zetaY = leg1y + leg2y;
    double zetaR = TMath::Sqrt(zetaX*zetaX + zetaY*zetaY);
    if ( zetaR > 0. ) {
      zetaX /= zetaR;
      zetaY /= zetaR;
    }

    //std::cout << " leg1Phi = " << leg1.phi()*180./TMath::Pi() << std::endl;
    //std::cout << " leg2Phi = " << leg2.phi()*180./TMath::Pi() << std::endl;

    //std::cout << " zetaX = " << zetaX << std::endl;
    //std::cout << " zetaY = " << zetaY << std::endl;

    //std::cout << " zetaPhi = " << normalizedPhi(atan2(zetaY, zetaX))*180./TMath::Pi() << std::endl;

    double visPx = leg1.px() + leg2.px();
    double visPy = leg1.py() + leg2.py();
    double pZetaVis = visPx*zetaX + visPy*zetaY;

    //std::cout << " visPx = " << visPx << std::endl;
    //std::cout << " visPy = " << visPy << std::endl;

    double px = visPx + metPx;
    double py = visPy + metPy;
    double pZeta = px*zetaX + py*zetaY;

    //std::cout << " metPhi = " << normalizedPhi(atan2(metPy, metPx))*180./TMath::Pi() << std::endl;

    //assert(pZetaVis >= 0.);

    return std::make_pair(pZeta, pZetaVis);
  }

  double collinearMass(const reco::Candidate::LorentzVector& p1, const reco::Candidate::LorentzVector& p2, const reco::Candidate::LorentzVector& met){
        double METproj= fabs(met.px()*p2.px()+met.py()*p2.py())/p2.pt();
        double xth=p2.pt()/(p2.pt()+METproj);
        double mass=(p1+p2).mass()/sqrt(xth);
        return mass;
  }

  double transverseMass(const reco::Candidate::LorentzVector& p1,
                        const reco::Candidate::LorentzVector& p2){
    double totalEt = p1.Et() + p2.Et();
    double totalPt = (p1 + p2).pt();
    double mt2 = totalEt*totalEt - totalPt*totalPt;
    if (mt2 < 0) {
      std::cout << "P1 = " << p1 << " P2 = " << p2 << " " << mt2 << std::endl;
    }
    return std::sqrt(std::abs(mt2));
  }

  // Taken from CommonTools/CandUtils/AddFourMomenta.h
  void addFourMomenta( reco::Candidate & c ) {
    reco::Candidate::LorentzVector p4( 0, 0, 0, 0 );
    reco::Candidate::Charge charge = 0;
    size_t n = c.numberOfDaughters();
    for(size_t i = 0; i < n; ++i) {
      const reco::Candidate * d = (const_cast<const reco::Candidate &>(c)).daughter(i);
      p4 += d->p4();
      charge += d->charge();
    }
    c.setP4( p4 );
    c.setCharge( charge );
  }

  /// Helper function to get the matched status 1 gen particle .
  /// If preFSR is true, the last unbranched particle in the matched 
  /// particle's chain is returned instead.
  /// The preFSR option is not guaranteed to work for any generators
  /// except Pythia 6 and Pythia 8.
  const reco::GenParticleRef getGenParticle(const reco::Candidate*   daughter, 
                                            const reco::GenParticleRefProd genCollectionRef, 
                                            int pdgIdToMatch, bool checkCharge, 
                                            bool preFSR)
  {
    //if no genPaticle no matching
    if(!genCollectionRef){
      return reco::GenParticleRef();
    }
    reco::GenParticleCollection genParticles = *genCollectionRef;
 
    //builds pset used by various subclasses
    edm::ParameterSet pset;
    pset.addParameter<double>("maxDPtRel", 0.5);
    pset.addParameter<double>("maxDeltaR", 0.5);
    std::vector<int> pdgIdsToMatch;
    pdgIdsToMatch.push_back(pdgIdToMatch);
    pset.addParameter<std::vector<int> >("mcPdgId", pdgIdsToMatch);
    std::vector<int> status;
    status.push_back(1);

/*    if(pdgIdToMatch==15){
     for (int istatus = 21; istatus< 30 ; istatus++){
      status.push_back(istatus); //pythia8 particles from an hard process have status code 21-29 
     } // this is specifically for allowing to get gen taus, matching them to the hardprocess. It should be checked further. 
    }
    // removing this 
*/

    pset.addParameter<std::vector<int> >("mcStatus", status);
    pset.addParameter<bool>("resolveByMatchQuality", false);
    pset.addParameter<bool>("checkCharge", checkCharge);
    pset.addParameter<bool>("resolveAmbiguities", true); //does not make any difference since we have no access to multiple candidates to match

    reco::MCMatchSelector<reco::Candidate, reco::GenParticle> slector(pset);
    reco::MatchByDRDPt<reco::Candidate, reco::GenParticle> matcher(pset);

    //copied from CommonTools/ UtilAlgos/ interface/ PhysObjectMatcher.h
    typedef std::pair<size_t, size_t> IndexPair;
    typedef std::vector<IndexPair> MatchContainer;

    // loop over (one in my case) candidates
    int index = -1;
    double minDr = 9999;
    // loop over target collection
    for(size_t m = 0; m != genParticles.size(); ++m) {
      const reco::GenParticle& match = genParticles[m];
      // check lock and preselection
      if ( slector(*daughter, match) ) {
       // matching requirement fulfilled -> store pair of indices
        if ( matcher(*daughter,match) )  {
	  double curDr = reco::deltaR(*daughter,match);
          if(curDr < minDr){
            minDr = curDr;
            index = m;
          }
        }
      }
    }

    reco::GenParticleRef out = reco::GenParticleRef();
    if(index != -1){
      out = reco::GenParticleRef(genCollectionRef,index);
    }
    //No Match found
    else{
      return reco::GenParticleRef();
    }

    // if we want the equivalent particle from the hard scatter, loop back
    // through particle's ancestry until we find it
    // This is not a good way to do this, but the good way (commented below) doesn't exist in 7_2_X
    //
    if(preFSR)
    {
      while(out->motherRef(0).isNonnull() && !(out->isLastCopyBeforeFSR()))
        out = out->motherRef(0);
    }

    return out;
    
  }

  /// Helper function to get the first interesting mother particle 
  const reco::GenParticleRef getMotherSmart(const reco::GenParticleRef genPart, int idNOTtoMatch)
  {
    if( genPart->numberOfMothers() == 0 ) return genPart; // if we've recursed all the way back we need to stop

    const reco::GenParticleRef mother = genPart->motherRef();
    if( !(mother.isAvailable() && mother.isNonnull())  ) return mother;
    if( mother.isAvailable() && mother.isNonnull() && (mother->status() == 3 || mother->status()==22) && mother->pdgId() != idNOTtoMatch )
       return mother;
    else
      return getMotherSmart(mother, idNOTtoMatch);
  }

  const bool comesFromHiggs(const reco::GenParticleRef genPart)
  {
    if( genPart->numberOfMothers() >= 1 ){
      const reco::GenParticleRef mother = /*dynamic_cast<reco::GenParticleRef>*/ (genPart->motherRef());
      if( !(mother.isAvailable() && mother.isNonnull()) ){
        return false;
      }
      if( mother.isAvailable() && mother.isNonnull() && (mother->pdgId() == 25 || mother->pdgId() == 35 ) ){ // h^0 or H^0
        return true;
      }
      else{
        return comesFromHiggs(mother);
      }
    }
    else{
      return false;
    }
  }

  const reco::Candidate::LorentzVector metPhiCorrection(const reco::Candidate::LorentzVector& vector, int nvertices, bool isMC)
  {
    //ReReco data / Summer'12 MC + Summer'13 JEC Type1 PFMET
    const double cx0 = (isMC) ? +1.62861e-01 : +4.83642e-02;  // 0.1166 :  0.2661;
    const double cxS = (isMC) ? -2.38517e-02 : +2.48870e-01;  // 0.0200 :  0.3217;
    const double cy0 = (isMC) ? +3.60860e-01 : -1.50135e-01;  // 0.2764 : -0.2251;
    const double cyS = (isMC) ? -1.30335e-01 : -8.27917e-02;  //-0.1280 : -0.1747;

    double offset_x = cx0 + cxS*nvertices;
    double offset_y = cy0 + cyS*nvertices;

    double newx     = vector.x() - offset_x;
    double newy     = vector.y() - offset_y;
    double mag      = TMath::Sqrt(newx*newx + newy*newy);

    //the vector is made in pt eta phi e coordinates!
    return reco::Candidate::LorentzVector(newx, newy, 0., mag);
  }

  const bool findDecay(const reco::GenParticleRefProd genCollectionRef, int pdgIdMother, int pdgIdDaughter)
  {
                              
    //if no genPaticle no matching
       if(!genCollectionRef){
             return false;
       }

       bool found=false;
       reco::GenParticleCollection pGenPart = *genCollectionRef;
                for( size_t i = 0; i < pGenPart.size(); ++ i ) {
                        const reco::GenParticle& genpart = (pGenPart)[i];
                        if(fabs(genpart.pdgId())==pdgIdMother && genpart.isLastCopy()){
                        //std::cout<<"M"<<genpart.pdgId()<<"   -->"<<genpart.isHardProcess()<<std::endl;
                        for(unsigned int j=0; j<genpart.numberOfDaughters(); j++){
                                const reco::Candidate* Wdaughter=genpart.daughter(j);
                                if(fabs(Wdaughter->pdgId())==pdgIdDaughter) found=true;
                                //std::cout<<"....\t"<<Wdaughter->pdgId()<<"..."<<Wdaughter->status()<<std::endl;    
                        }
                        }
      }

      return found;
  }

  float genHTT(const lhef::HEPEUP lheeventinfo){
      float sumpt=0;
      for (int i = 0; i < lheeventinfo.NUP ; ++i) {
            if (lheeventinfo.ISTUP[i] <0||((abs(lheeventinfo.IDUP[i])>5&&lheeventinfo.IDUP[i]!=21) ))  continue;
            double px=lheeventinfo.PUP.at(i)[0];
            double py=lheeventinfo.PUP.at(i)[1];
            double pt=sqrt(px*px+py*py);

            sumpt+=pt;
       }

      return sumpt;
  }

  float jetQGVariables(const reco::CandidatePtr  jetptr, const std::string& myvar, const std::vector<edm::Ptr<reco::Vertex>>& recoVertices)
  {
  //std::map <std::string, float> varMap; 
  const pat::Jet *jet = dynamic_cast<const pat::Jet*> (jetptr.get());
  if (myvar == "eta")
    return jet->eta();
  Bool_t useQC = true;
  // if(fabs(jet->eta()) > 2.5 && type == "MLP") useQC = false;		//In MLP: no QC in forward region

  std::vector<edm::Ptr<reco::Vertex>>::const_iterator vtxLead = recoVertices.begin();

    Float_t sum_weight = 0., sum_deta = 0., sum_dphi = 0., sum_deta2 = 0., sum_dphi2 = 0., sum_detadphi = 0., sum_pt = 0.;
    Int_t nChg_QC = 0, nChg_ptCut = 0, nNeutral_ptCut = 0;

    //Loop over the jet constituents
    std::vector<reco::PFCandidatePtr> constituents = jet->getPFConstituents();
    for(unsigned i = 0; i < constituents.size(); ++i){
      reco::PFCandidatePtr part = jet->getPFConstituent(i);      
      if(!part.isNonnull()) continue;
    
      reco::TrackRef itrk = part->trackRef();
    
      bool trkForAxis = false;
      if(itrk.isNonnull()){						//Track exists --> charged particle
        if(part->pt() > 1.0) nChg_ptCut++;
  	
      //Search for closest vertex to track
      std::vector<edm::Ptr<reco::Vertex>>::const_iterator  vtxClose = recoVertices.begin();
      for( std::vector<edm::Ptr<reco::Vertex>>::const_iterator  vtx = recoVertices.begin(); vtx != recoVertices.end(); ++vtx){
	if(fabs(itrk->dz((*vtx)->position())) < fabs(itrk->dz((*vtxClose)->position()))) vtxClose = vtx;
      }
  	
        if(vtxClose == vtxLead){
          Float_t dz = itrk->dz((*vtxClose)->position());
          Float_t dz_sigma = sqrt(pow(itrk->dzError(),2) + pow((*vtxClose)->zError(),2));
  	
          if(itrk->quality(reco::TrackBase::qualityByName("highPurity")) && fabs(dz/dz_sigma) < 5.){
            trkForAxis = true;
            Float_t d0 = itrk->dxy((*vtxClose)->position());
            Float_t d0_sigma = sqrt(pow(itrk->d0Error(),2) + pow((*vtxClose)->xError(),2) + pow((*vtxClose)->yError(),2));
            if(fabs(d0/d0_sigma) < 5.) nChg_QC++;
          }
        }
      } else {								//No track --> neutral particle
        if(part->pt() > 1.0) nNeutral_ptCut++;
        trkForAxis = true;
      }
    
      Float_t deta = part->eta() - jet->eta();
      Float_t dphi = 2*atan(tan(((part->phi()- jet->phi()))/2));           
      Float_t partPt = part->pt(); 
      Float_t weight = partPt*partPt;

      if(!useQC || trkForAxis){					//If quality cuts, only use when trkForAxis
        sum_weight += weight;
        sum_pt += partPt;
        sum_deta += deta*weight;                  
        sum_dphi += dphi*weight;                                                                                             
        sum_deta2 += deta*deta*weight;                    
        sum_detadphi += deta*dphi*weight;                               
        sum_dphi2 += dphi*dphi*weight;
      }	
    }

    //Calculate axis and ptD
    Float_t a = 0., b = 0., c = 0.;
    Float_t ave_deta = 0., ave_dphi = 0., ave_deta2 = 0., ave_dphi2 = 0.;
    if(sum_weight > 0){
      if (myvar == "ptD")
        return sqrt(sum_weight)/sum_pt;
      ave_deta = sum_deta/sum_weight;
      ave_dphi = sum_dphi/sum_weight;
      ave_deta2 = sum_deta2/sum_weight;
      ave_dphi2 = sum_dphi2/sum_weight;
      a = ave_deta2 - ave_deta*ave_deta;                          
      b = ave_dphi2 - ave_dphi*ave_dphi;                          
      c = -(sum_detadphi/sum_weight - ave_deta*ave_dphi);                
    } 
    else if(myvar == "ptD")
      return 0;
    Float_t delta = sqrt(fabs((a-b)*(a-b)+4*c*c));
  
    if(myvar == "axis1")
      return (a+b+delta > 0) ? sqrt(0.5*(a+b+delta)) : 0.;
    else if(myvar == "axis2")
      return (a+b-delta > 0) ? sqrt(0.5*(a+b-delta)) : 0.;
    else if(myvar == "mult")
      return (nChg_QC + nNeutral_ptCut);
    else if(myvar == "mult_MLP_QC")
      return (nChg_QC );
    else if(myvar == "mult_MLP")
      return (nChg_ptCut + nNeutral_ptCut );
  
    return -1.;
  }

}
