#ifndef PATDICANDIDATESYSTEMATICS_H
#define PATDICANDIDATESYSTEMATICS_H

#include "DataFormats/PatCandidates/interface/PATObject.h"
#include "DataFormats/Candidate/interface/LeafCandidate.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/Math/interface/deltaPhi.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

typedef pat::PATObject<reco::LeafCandidate> PATLeafCandidate;

template<typename T1, typename T2>
class PATDiCandidateSystematics : public PATLeafCandidate {
  public:
    typedef reco::Candidate::LorentzVector LorentzVector;

    PATDiCandidateSystematics():PATLeafCandidate(){};

    PATDiCandidateSystematics(
        const edm::Ptr<T1>& p1, const edm::Ptr<T2>& p2,
        const edm::Ptr<pat::MET>& met,
        const edm::Ptr<reco::Vertex>& vertex):PATLeafCandidate(
          reco::LeafCandidate( p1->charge() + p2->charge(),
            p1->p4() + p2->p4(), vertex->position())) {
      daughter1_ = p1;
      daughter2_ = p2;
      met_ = met;
    }

    const edm::Ptr<T1>& daughter1() const { return daughter1_; }
    const edm::Ptr<T2>& daughter2() const { return daughter2_; }
    const edm::Ptr<pat::MET>& met() const { return met_; }
    const edm::Ptr<reco::Vertex>& vertexObject() const { return vertex_; }

    LorentzVector visP4(const std::string& d1SysTag,
        const std::string& d2SysTag) const {
      const LorentzVector& p4_1 = daughter1_->userCand(d1SysTag)->p4();
      const LorentzVector& p4_2 = daughter2_->userCand(d2SysTag)->p4();
      return p4_1 + p4_2;
    }

    LorentzVector totalP4(const std::string& d1SysTag,
        const std::string& d2SysTag, const std::string& metSysTag) const {
      const LorentzVector& p4_1 = daughter1_->userCand(d1SysTag)->p4();
      const LorentzVector& p4_2 = daughter2_->userCand(d2SysTag)->p4();
      const LorentzVector& met = met_->userCand(metSysTag)->p4();
      return p4_1 + p4_2 + met;
    }

    std::pair<double,double> pZetas(const std::string& d1SysTag,
        const std::string& d2SysTag, const std::string& metSysTag) const {

      const LorentzVector& leg1 = daughter1_->userCand(d1SysTag)->p4();
      const LorentzVector& leg2 = daughter2_->userCand(d2SysTag)->p4();
      const LorentzVector& met = met_->userCand(metSysTag)->p4();

      double leg1x = cos(leg1.phi());
      double leg1y = sin(leg1.phi());
      double leg2x = cos(leg2.phi());
      double leg2y = sin(leg2.phi());
      double zetaX = leg1x + leg2x;
      double zetaY = leg1y + leg2y;
      double zetaR = std::sqrt(zetaX*zetaX + zetaY*zetaY);
      if ( zetaR > 0. ) {
        zetaX /= zetaR;
        zetaY /= zetaR;
      }

      double visPx = leg1.px() + leg2.px();
      double visPy = leg1.py() + leg2.py();
      double pZetaVis = visPx*zetaX + visPy*zetaY;

      double px = visPx + met.px();
      double py = visPy + met.py();
      double pZeta = px*zetaX + py*zetaY;

      return std::make_pair(pZeta, pZetaVis);
    }

    double deltaPhi12(const std::string& d1SysTag,
        const std::string& d2SysTag) const {
      const LorentzVector& p4_1 = daughter1_->userCand(d1SysTag)->p4();
      const LorentzVector& p4_2 = daughter2_->userCand(d2SysTag)->p4();
      return deltaPhi(p4_1.phi(), p4_2.phi());
    }

    double mt1MEt(const std::string& d1SysTag,
        const std::string& metSysTag) const {
      const LorentzVector& p4_1 = daughter1_->userCand(d1SysTag)->p4();
      const LorentzVector& met = met_->userCand(metSysTag)->p4();

      double totalEt = p4_1.pt() + met.Et();
      double totalPt = (p4_1 + met).pt();

      // to do double check this
      return std::sqrt(totalEt*totalEt - totalPt*totalPt);
    }

    double mt2MEt(const std::string& d2SysTag,
        const std::string& metSysTag) const {
      const LorentzVector& p4_2 = daughter2_->userCand(d2SysTag)->p4();
      const LorentzVector& met = met_->userCand(metSysTag)->p4();

      double totalEt = p4_2.pt() + met.Et();
      double totalPt = (p4_2 + met).pt();
      // to do double check this
      return std::sqrt(totalEt*totalEt - totalPt*totalPt);
    }

  private:
    edm::Ptr<T1> daughter1_;
    edm::Ptr<T2> daughter2_;
    edm::Ptr<pat::MET> met_;
    edm::Ptr<reco::Vertex> vertex_;
};

#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Tau.h"

typedef PATDiCandidateSystematics<pat::Muon, pat::Tau> PATMuTauSystematics;

#endif /* end of include guard: PATDICANDIDATESYSTEMATICS_H */
