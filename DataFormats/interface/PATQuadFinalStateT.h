#ifndef FinalStateAnalysis_DataFormats_PATQuadFinalStateT_h
#define FinalStateAnalysis_DataFormats_PATQuadFinalStateT_h

class PATFinalStateProxy;
//class PATMultiCandFinalState;

#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateProxy.h"
#include "FinalStateAnalysis/DataFormats/interface/PATMultiCandFinalStateFwd.h"
#include "FinalStateAnalysis/DataFormats/interface/PATMultiCandFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEventFwd.h"

#include "DataFormats/Math/interface/deltaR.h"

template<class T1, class T2, class T3, class T4>
class PATQuadFinalStateT : public PATFinalState {
  public:
    typedef T1 daughter1_type;
    typedef T2 daughter2_type;
    typedef T3 daughter3_type;
    typedef T4 daughter4_type;

    PATQuadFinalStateT():PATFinalState(){}

    PATQuadFinalStateT(const edm::Ptr<T1>& p1, const edm::Ptr<T2>& p2,
        const edm::Ptr<T3>& p3,
        const edm::Ptr<T4>& p4,
        const edm::Ptr<PATFinalStateEvent>& evt)
      :PATFinalState(
          p1->charge() + p2->charge() + p3->charge() + p4->charge(),
          p1->p4() + p2->p4() + p3->p4() + p4->p4(), evt) {
        p1_ = p1;
        p2_ = p2;
        p3_ = p3;
        p4_ = p4;
      }

    virtual PATQuadFinalStateT<T1, T2, T3, T4>* clone() const {
      return new PATQuadFinalStateT<T1, T2, T3, T4>(*this);
    }

    virtual const reco::Candidate* daughterUnsafe(size_t i) const {
      const reco::Candidate* output = NULL;
      if (i == 0)
        output = p1_.get();
      else if (i == 1)
        output = p2_.get();
      else if (i == 2)
        output = p3_.get();
      else if (i == 3)
        output = p4_.get();
      return output;
    }

    virtual const reco::CandidatePtr daughterPtrUnsafe(size_t i) const {
      if (i == 0)
        return p1_;
      else if (i == 1)
        return p2_;
      else if (i == 2)
        return p3_;
      else if (i == 3)
        return p4_;
      else
        return reco::CandidatePtr();
    }

    size_t numberOfDaughters() const { return 4; }

    virtual reco::CandidatePtr daughterUserCandUnsafe(size_t i,
        const std::string& tag) const {
      if (i == 0)
        return p1_->userCand(tag);
      else if (i == 1)
        return p2_->userCand(tag);
      else if (i == 2)
        return p3_->userCand(tag);
      else if (i == 3)
        return p4_->userCand(tag);
      else
        return reco::CandidatePtr();
    }

    virtual const reco::CandidatePtrVector& daughterOverlaps(
        size_t i, const std::string& label) const {
      if (i == 0)
        return p1_->overlaps(label);
      else if (i == 1)
        return p2_->overlaps(label);
      else if (i == 2)
        return p3_->overlaps(label);
      else if (i == 3)
        return p4_->overlaps(label);
      throw cms::Exception("NullOverlaps") <<
        "PATQuadFinalState::daughterOverlaps(" << i << "," << label
        << ") is null!" << std::endl;
    }

    /// Build a subcandidate w/ fsr
    PATFinalStateProxy subcandfsr( int i, int j, const std::string& fsrLabel="" ) const
    {
      std::vector<reco::CandidatePtr> output;
      output.push_back( daughterPtr(i) );
      output.push_back( daughterPtr(j) );
      
      const reco::CandidatePtr fsrPho = bestFSROfZ(i, j, fsrLabel);
      if(fsrPho.isNonnull() && fsrPho.isAvailable())
	output.push_back(fsrPho);
      return PATFinalStateProxy(new PATMultiCandFinalState(output, evt()));
    }

    /// quad candidate p4 w/ fsr
    LorentzVector p4fsr(const std::string& fsrLabel="") const
    {
      // start with the 4-momentum of the first Z and add to it
      PATFinalState::LorentzVector p = subcandfsr(0, 1, fsrLabel)->p4();

      for(unsigned int i = 2; i+1 < numberOfDaughters(); i += 2)
	{
	  p += subcandfsr(i, i+1, fsrLabel)->p4();
	}

      return p;
    }

    /// Returns the index of this lepton's Z partner in 4l ordering
    const inline size_t get4LPartner(size_t i) const
    {
      return i + (i%2 ? -1 : 1);
    }

    // Get the FSR candidate that moves the invariant mass of the lepton pair closest to nominal Z mass
    const reco::CandidatePtr bestFSROfZ(int i, int j, const std::string& fsrLabel) const
    {
      bool iIsElectron = false;
      bool jIsElectron = false;

      edm::Ptr<pat::Electron> ei = daughterAsElectron(i);
      edm::Ptr<pat::Muon> mi = daughterAsMuon(i);
      if(daughter(i)->isElectron() && ei.isNonnull() && ei.isAvailable())
	{
	  iIsElectron = true;
	}
      else 
	{
	  if(!(daughter(i)->isMuon() && mi.isNonnull() && mi.isAvailable()))
	    return reco::CandidatePtr();
	}

      edm::Ptr<pat::Electron> ej = daughterAsElectron(j);
      edm::Ptr<pat::Muon> mj = daughterAsMuon(j);
      if(daughter(j)->isElectron() && ej.isNonnull() && ej.isAvailable())
	{
	  jIsElectron = true;
	}
      else 
	{
	  if(!(daughter(j)->isMuon() && mj.isNonnull() && mj.isAvailable()))
	    return reco::CandidatePtr();//edm::Ptr<reco::Candidate>(new const reco::Candidate());
	}

      int leptonOfBest; // index of daughter that has best FSR cand 
      int bestFSR = -1; // index of best photon as userCand
      double bestFSRPt = -1; // Pt of best photon
      double bestFSRDeltaR = 1000; // delta R between best FSR and nearest lepton
      float noFSRDist = zCompatibility(i,j); // must be better Z candidate than no FSR
      if(noFSRDist == -1000) // Same sign leptons
	return reco::CandidatePtr();
      PATFinalState::LorentzVector p4NoFSR = daughter(i)->p4() + daughter(j)->p4();

      if((iIsElectron?ei->hasUserInt("n"+fsrLabel):mi->hasUserInt("n"+fsrLabel)))
	{
	  for(int ind = 0; ind < (iIsElectron?ei->userInt("n"+fsrLabel):mi->userInt("n"+fsrLabel)); ++ind)
	    {
	      PATFinalState::LorentzVector fsrCandP4 = daughterUserCandP4(i, fsrLabel+std::to_string(ind));
	      PATFinalState::LorentzVector zCandP4 = p4NoFSR + fsrCandP4;
	      if(zCandP4.mass() < 4. || zCandP4.mass() > 100.) // overall mass cut
		continue;
	      if(zCompatibility(zCandP4) > noFSRDist) // Must bring us closer to on-shell Z
		continue;
	      // If any FSR candidate has pt > 4, pick the highest pt candidate. 
	      // Otherwise, pick the one with the smallest deltaR to its lepton.
	      if(bestFSRPt > 4. || fsrCandP4.pt() > 4.)
		{
		  if(fsrCandP4.pt() < bestFSRPt)
		    continue;
		}
	      else if(reco::deltaR(daughter(i)->p4(), fsrCandP4) > bestFSRDeltaR)
		continue;

	      // This one looks like the best for now
	      leptonOfBest = i;
	      bestFSR = ind;
	      bestFSRPt = fsrCandP4.pt();
	      bestFSRDeltaR = reco::deltaR(daughter(i)->p4(), fsrCandP4);
	    }
	}
      if((jIsElectron?ej->hasUserInt("n"+fsrLabel):mj->hasUserInt("n"+fsrLabel)))
	{
	  //      std::cout << "Found an embedded candidate in event " << evt()->evtId().event() << std::endl;
	  for(int ind = 0; ind < (jIsElectron?ej->userInt("n"+fsrLabel):mj->userInt("n"+fsrLabel)); ++ind)
	    {
	      PATFinalState::LorentzVector fsrCandP4 = daughterUserCandP4(j, fsrLabel+std::to_string(ind));
	      PATFinalState::LorentzVector zCandP4 = p4NoFSR + fsrCandP4;
	      if(zCandP4.mass() < 4. || zCandP4.mass() > 100.) // overall mass cut
		continue;
	      if(zCompatibility(zCandP4) > noFSRDist) // Must bring us closer to on-shell Z
		continue;
	      // If any FSR candidate has pt > 4, pick the highest pt candidate. 
	      // Otherwise, pick the one with the smallest deltaR to its lepton.
	      if(bestFSRPt > 4. || fsrCandP4.pt() > 4.)
		{
		  if(fsrCandP4.pt() < bestFSRPt)
		    continue;
		}
	      else if(reco::deltaR(daughter(j)->p4(), fsrCandP4) > bestFSRDeltaR)
		continue;

	      // This one looks like the best for now
	      leptonOfBest = j;
	      bestFSR = ind;
	      bestFSRPt = fsrCandP4.pt();
	      bestFSRDeltaR = reco::deltaR(daughter(j)->p4(), fsrCandP4);
	    }
	}
      if(bestFSR != -1)
	{
	  //  std::cout << "Accepted FSR cand, event " << evt()->evtId().event() << std::endl;
	  return daughterUserCand(leptonOfBest, fsrLabel+std::to_string(bestFSR));
	}
      //  std::cout << "Rejected FSR cand, event " << evt()->evtId().event() << std::endl;
      return reco::CandidatePtr();//edm::Ptr<reco::Candidate>(new const reco::Candidate());
    }

    double zCompatibilityFSR(int i, int j, const std::string fsrLabel) const
    {
      PATFinalStateProxy z = subcandfsr(i, j, fsrLabel);
      return zCompatibility(z);
    }


    float allFSRIsoContribution(const size_t i, const std::string& label,
				const float dRMin=0.01, const float dRMax=0.4) const
    {
      float isoContrib = 0;

      for(size_t l1 = 0; l1 < numberOfDaughters(); l1 += 2)
	{
	  reco::CandidatePtr fsr = bestFSROfZ(l1, l1+1, label);
	  if(!(fsr.isNonnull() && fsr.isAvailable()))
	    continue;

	  float dR = reco::deltaR(daughter(i)->p4(), fsr->p4());
	  
	  if(dR > dRMin && dR < dRMax)
	    isoContrib += fsr->pt();
	}

      return isoContrib;
    }

    
    /// Build a subcandidate w/ fsr of the main Zs FSR photons
    PATFinalStateProxy subcandPrimaryFSR( size_t i, size_t j, const std::string& fsrLabel="" ) const
    {
      if(j == get4LPartner(i))
	return subcandfsr(i,j,fsrLabel);

      std::vector<reco::CandidatePtr> output;
      output.push_back( daughterPtr(i) );
      output.push_back( daughterPtr(j) );
      
      size_t i2 = get4LPartner(i);
      size_t j2 = get4LPartner(j);

      const reco::CandidatePtr fsr1 = bestFSROfZ(i, i2, fsrLabel);
      const reco::CandidatePtr fsr2 = bestFSROfZ(j, j2, fsrLabel);
      if(fsr1.isNonnull() && fsr1.isAvailable())
	{
	  // photon is always matched with closer lepton
	  if(reco::deltaR(daughter(i)->p4(), fsr1->p4()) < reco::deltaR(daughter(i2)->p4(), fsr1->p4()))
	    output.push_back(fsr1);
	}
      if(fsr2.isNonnull() && fsr2.isAvailable())
	{
	  if(reco::deltaR(daughter(j)->p4(), fsr2->p4()) < reco::deltaR(daughter(j2)->p4(), fsr2->p4()))
	    output.push_back(fsr2);
	}
      return PATFinalStateProxy(new PATMultiCandFinalState(output, evt()));
    }


    // Methods ending with DM are as the equivalent methods inherited from 
    // PATFinalState, but with the user cand ignored if it does not bring the 
    // Z candidate closer to on-shell

    LorentzVector daughterP4WithUserCandDM(const size_t i, const std::string& label) const
    {
      if(fsrImprovesZ(i, label))
        return daughterP4WithUserCand(i, label);
      return daughter(i)->p4();
    }

    const bool fsrImprovesZ(const size_t i, const std::string& label) const
    {
      size_t j = get4LPartner(i);
      LorentzVector without = daughter(i)->p4() + daughter(j)->p4();
      LorentzVector with = daughterP4WithUserCand(i, label) + daughter(j)->p4();

      return (fabs(with.mass() - 91.1876) < fabs(without.mass() - 91.1876));
    }

    LorentzVector diObjectP4WithUserCandsDM(const size_t i, 
                                            const size_t j, 
                                            const std::string& label) const
    {
      return (daughterP4WithUserCandDM(i, label) + 
              daughterP4WithUserCandDM(j, label));
    }

    LorentzVector p4WithUserCandsDM(const std::string& label) const
    {
      LorentzVector out = LorentzVector();
      for(size_t i = 0; i < numberOfDaughters(); ++i)
        out += daughterP4WithUserCandDM(i, label);
      
      return out;      
    }

    const float ptOfDaughterUserCandDM(const size_t i, const std::string& label) const
    {  
      if(fsrImprovesZ(i, label))
        {
          reco::CandidatePtr uCand = daughterUserCand(i, label);
          return uCand->pt();
        }
      
      return 0.;
    }

    const float daughterUserCandIsoContributionDM(const size_t i, const std::string& label) const
    {
      if(fsrImprovesZ(i, label))
        return daughterUserCandIsoContribution(i, label);
      return 0.;
    }

    

  private:
    edm::Ptr<T1> p1_;
    edm::Ptr<T2> p2_;
    edm::Ptr<T3> p3_;
    edm::Ptr<T4> p4_;
};


#endif /* end of include guard: FinalStateAnalysis_DataFormats_PATQuadFinalStateT_h */
