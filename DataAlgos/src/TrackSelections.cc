//#include "FinalStateAnalysis/DataAlgos/interface/TrackSelections.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"

#include "DataFormats/Candidate/interface/Candidate.h"
#include "DataFormats/RecoCandidate/interface/RecoCandidate.h"
//#include "DataFormats/RecoCandidate/interface/TrackCandidate.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

struct mypion{
  double p_pt;
  double p_eta;
  double p_phi;
  double p_iso;
  double p_charge;
  double p_gen;
  double p_dxy;
  double p_dz;
  double p_pv;
  double p_flag;
};

std::vector<double> computeTrackInfo(
    const std::vector<const reco::Candidate*>& tracks, const std::vector<pat::PackedCandidate> pfs, const reco::GenParticleRefProd genCollectionRef, bool has_gen) {
  std::vector<mypion> pion_list;

  std::vector<double> output;

  int numTracks = tracks.size();

  for (const reco::Candidate *mytrack : tracks) {
     if (fabs(mytrack->pdgId())==211){
	mypion mp1;
        double charged = 0, neutral = 0, pileup  = 0;
        for (unsigned int i = 0, n = pfs.size(); i < n; ++i) {
            const pat::PackedCandidate pf = pfs[i];
	    if (sqrt((pf.eta()-mytrack->eta())*(pf.eta()-mytrack->eta())+deltaPhi(pf.phi(),mytrack->phi())*deltaPhi(pf.phi(),mytrack->phi()))<0.3 && sqrt((pf.eta()-mytrack->eta())*(pf.eta()-mytrack->eta())+deltaPhi(pf.phi(),mytrack->phi())*deltaPhi(pf.phi(),mytrack->phi()))>0.001){
                if (pf.charge() == 0) {
                    if (pf.pt() > 0.5) neutral += pf.pt();
                } else if (pf.fromPV() >= 2) {
                    charged += pf.pt();
                } else {
                    if (pf.pt() > 0.5) pileup += pf.pt();
                }
            }
            if (sqrt((pf.eta()-mytrack->eta())*(pf.eta()-mytrack->eta())+deltaPhi(pf.phi(),mytrack->phi())*deltaPhi(pf.phi(),mytrack->phi()))<0.001){
		mp1.p_dxy=pf.dxy();
                mp1.p_dz=pf.dz();
                mp1.p_pv=pf.fromPV();
                mp1.p_flag=pf.trackHighPurity();
	    }
        }
        double iso = charged + std::max(0.0, neutral-0.5*pileup);
	mp1.p_iso=iso;

	double genID=-1;
        if (has_gen){
            reco::GenParticleCollection genParticles = *genCollectionRef;
            if ( genParticles.size() > 0 ) {
                reco::GenParticle& closest = genParticles[0];
                double closestDR = 999;
                for(size_t m = 0; m != genParticles.size(); ++m) {
                    reco::GenParticle& genp = genParticles[m];
	            double tmpDR = sqrt((genp.eta()-mytrack->eta())*(genp.eta()-mytrack->eta())+deltaPhi(genp.phi(),mytrack->phi())*deltaPhi(genp.phi(),mytrack->phi()));
                    if ( fabs(genp.pdgId())==211 && tmpDR < closestDR ) { closest = genp; closestDR = tmpDR; }
                }
                genID = abs(closest.pdgId());
                if (closestDR>0.2) genID = -1;
	    }
        }
	mp1.p_gen=genID;
	mp1.p_pt=mytrack->pt();
        mp1.p_eta=mytrack->eta();
        mp1.p_phi=mytrack->phi();
        mp1.p_charge=mytrack->charge();
        if (mp1.p_pv>1) pion_list.push_back(mp1);
    }
  }

  std::sort(begin(pion_list), end(pion_list), [](mypion a, mypion b){return a.p_pt > b.p_pt;});

  if (pion_list.size()>0){
    output.push_back(pion_list[0].p_pt);
    output.push_back(pion_list[0].p_eta);
    output.push_back(pion_list[0].p_phi);
    output.push_back(pion_list[0].p_charge);
    output.push_back(pion_list[0].p_dxy);
    output.push_back(pion_list[0].p_dz);
    output.push_back(pion_list[0].p_pv);
    output.push_back(pion_list[0].p_flag);
    output.push_back(pion_list[0].p_iso);
    output.push_back(pion_list[0].p_gen);
  }
  if (pion_list.size()>1){
    output.push_back(pion_list[1].p_pt);
    output.push_back(pion_list[1].p_eta);
    output.push_back(pion_list[1].p_phi);
    output.push_back(pion_list[1].p_charge);
    output.push_back(pion_list[1].p_dxy);
    output.push_back(pion_list[1].p_dz);
    output.push_back(pion_list[1].p_pv);
    output.push_back(pion_list[1].p_flag);
    output.push_back(pion_list[1].p_iso);
    output.push_back(pion_list[1].p_gen);
  }
  if (pion_list.size()>2){
    output.push_back(pion_list[2].p_pt);
    output.push_back(pion_list[2].p_eta);
    output.push_back(pion_list[2].p_phi);
    output.push_back(pion_list[2].p_charge);
    output.push_back(pion_list[2].p_dxy);
    output.push_back(pion_list[2].p_dz);
    output.push_back(pion_list[2].p_pv);
    output.push_back(pion_list[2].p_flag);
    output.push_back(pion_list[2].p_iso);
    output.push_back(pion_list[2].p_gen);
  }



  for (int j=output.size(); j<31; ++ j){
    output.push_back( -9999 );
  }

  return output;
}

