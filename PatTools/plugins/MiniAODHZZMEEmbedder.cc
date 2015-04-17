#ifdef HZZMELA // This should only be compiled if we actually want ME stuff

//////////////////////////////////////////////////////////////////////////////
//                                                                          //
//   MiniAODHZZMEEmbedder.cc                                                //
//                                                                          //
//   Calculates H->ZZ MELA/MEKD etc. for a final state and puts it in the   //
//       final state as a userFloat. A probability is stored for each       //
//       string passed in via the vector "processes," calculated using      //
//       the MEM process and calculator defined in included file            //
//       HZZMELAProcesses.h.                                                //
//   Automatically embeds m4l probabilities as in datacards for SM Higgs    //
//       (as "p0plus_m4l") and background (as "bkg_m4l") as in datacards    //
//                                                                          //
//   Author: Nate Woods, U. Wisconsin                                       //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////


// system includes
#include <memory>
#include <vector>
#include <unordered_map>
#include <utility> // contains std::pair

// CMS includes
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
#include "DataFormats/Math/interface/deltaR.h"

// FSA includes
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"
#include "FinalStateAnalysis/PatTools/data/HZZMEProcesses.h"

// ZZMatrixElement includes
#include "ZZMatrixElement/MEMCalculators/interface/MEMCalculators.h"


class MiniAODHZZMEEmbedder : public edm::EDProducer {
 public:
  MiniAODHZZMEEmbedder(const edm::ParameterSet& pset);
  virtual ~MiniAODHZZMEEmbedder(){}
 private:
  // Methods
  virtual void beginJob();
  virtual void produce(edm::Event& iEvent, const edm::EventSetup& iSetup);
  virtual void endJob();

  // Calculate the matrix element for fs under process hypothesis proc using calculator calc
  const float getZZME(const PATFinalState& fs, MEMNames::Processes proc, 
		      MEMNames::MEMCalcs calc, const std::string& fsrLabel);
  // Calculate the 4l SM Higgs and background probability for fs under systematics assumption syst
  // Outputs by setting sigProb and bkgProb rather than returning
  void getPm4l(const PATFinalState& fs, MEMNames::SuperKDsyst syst, float& sigProb, 
	       float& bkgProb, const std::string& fsrLabel);
  // Tag of final states to calculate MEs for
  edm::InputTag src_;
  // MEM calculator object
  MEMs MEM_; 
  // List of probabilities to calculate
  const std::vector<std::string> processes_;
  // Label of FSR candidate photons
  const std::string fsrLabel_;
  // The process and calculator for each probability we might to calculate are stored in 
  // a pair, keyed to the same string they would be keyed to in the 
  const std::unordered_map<std::string, std::pair<MEMNames::Processes, MEMNames::MEMCalcs> > processInfo_;
  // ME calculation parameters
  const unsigned int energy_; // collision energy
  const double mH_; // Higgs mass hypothesis
  const std::string pdf_; // PDF to use
};


MiniAODHZZMEEmbedder::MiniAODHZZMEEmbedder(const edm::ParameterSet& iConfig) :
  src_(iConfig.exists("src") ?
       iConfig.getParameter<edm::InputTag>("src") :
       edm::InputTag("finalStateeeee")),
  processes_(iConfig.exists("processes") ?
	     iConfig.getParameter<std::vector<std::string> >("processes") :
	     std::vector<std::string>()),
  fsrLabel_(iConfig.exists("fsrLabel") ?
	    iConfig.getParameter<std::string>("fsrLabel") :
	    std::string("FSRCand")),
  processInfo_(getHZZMEProcessInfo()),
  energy_(iConfig.exists("energy") ? 
	  iConfig.getParameter<unsigned int>("energy") :
	  13),
  mH_(iConfig.exists("mH") ? 
      iConfig.getParameter<double>("mH") :
      125.6),
  pdf_(iConfig.exists("pdf") ? 
       iConfig.getParameter<std::string>("pdf") :
       std::string("CTEQ6L"))
{
  MEM_ = MEMs(energy_, mH_, pdf_);

  // Check to make sure all desired processes are valid
  for(std::vector<std::string>::const_iterator iProc = processes_.begin(); 
      iProc < processes_.end(); ++iProc)
    {
      if(processInfo_.find(*iProc) == processInfo_.end())
	throw cms::Exception("MiniAODHZZMEEmbedder") << "Process " << *iProc
						     << " is not defined in "
						     << "PatTools/data/HZZMEProcesses.h.\n" 
						     << "Please define it there or fix your typo.\n";
    }

  produces<PATFinalStateCollection>();
}


void MiniAODHZZMEEmbedder::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) 
{
  std::auto_ptr<PATFinalStateCollection> output(new PATFinalStateCollection);

  edm::Handle<edm::View<PATFinalState> > finalStatesIn;
  iEvent.getByLabel(src_, finalStatesIn);

  for (size_t iFS = 0; iFS < finalStatesIn->size(); ++iFS) 
    {
      PATFinalState* embedInto = finalStatesIn->ptrAt(iFS)->clone();
      for(std::vector<std::string>::const_iterator iProc = processes_.begin(); 
	  iProc < processes_.end(); ++iProc)
	{
	  float ME = getZZME(*embedInto, processInfo_.at(*iProc).first, processInfo_.at(*iProc).second, fsrLabel_);
	  embedInto->addUserFloat(*iProc, ME);
	}

      // Embed SM Higgs and background m4l probabilities, as in datacards
      float p0plus_m4l, bkg_m4l;
      getPm4l(*embedInto, MEMNames::kNone, p0plus_m4l, bkg_m4l, fsrLabel_);
      embedInto->addUserFloat("p0plus_m4l", p0plus_m4l);
      embedInto->addUserFloat("bkg_m4l", bkg_m4l);

      output->push_back(embedInto); // takes ownership
    }

  iEvent.put(output);
}


const float MiniAODHZZMEEmbedder::getZZME(const PATFinalState& fs, MEMNames::Processes proc, 
					  MEMNames::MEMCalcs calc, const std::string& fsrLabel)
{
  std::vector<TLorentzVector> partP4 = std::vector<TLorentzVector>();
  std::vector<int> partID = std::vector<int>();
  for(unsigned int iLep = 0; iLep < fs.numberOfDaughters(); iLep++)
    {
      partID.push_back(fs.daughter(iLep)->pdgId());
      PATFinalState::LorentzVector thisP4 = fs.daughter(iLep)->p4();
      reco::CandidatePtr fsrPtr = fs.bestFSROfZ(iLep, fs.get4LPartner(iLep), fsrLabel);
      if(fsrPtr.isAvailable() && fsrPtr.isNonnull())
	if(reco::deltaR(thisP4, fsrPtr->p4()) < reco::deltaR(fs.daughter(fs.get4LPartner(iLep))->p4(), fsrPtr->p4()))
	  thisP4 += fsrPtr->p4();
      partP4.push_back(TLorentzVector());
      partP4.back().SetPtEtaPhiM(thisP4.pt(), thisP4.eta(), thisP4.phi(), thisP4.mass());
    }

  double ME;
  MEM_.computeME(proc, calc, partP4, partID, ME);

  return ME;
}

// Assigns the answers to sigProb and bkgProb rather than returning them
void MiniAODHZZMEEmbedder::getPm4l(const PATFinalState& fs, MEMNames::SuperKDsyst syst, float& sigProb, 
				   float& bkgProb, const std::string& fsrLabel)
{
  std::vector<TLorentzVector> partP4 = std::vector<TLorentzVector>();
  std::vector<int> partID = std::vector<int>();
  for(unsigned int iLep = 0; iLep < fs.numberOfDaughters(); iLep++)
    {
      partID.push_back(fs.daughter(iLep)->pdgId());
      PATFinalState::LorentzVector thisP4 = fs.daughter(iLep)->p4();
      reco::CandidatePtr fsrPtr = fs.bestFSROfZ(iLep, fs.get4LPartner(iLep), fsrLabel);
      if(fsrPtr.isAvailable() && fsrPtr.isNonnull())
	if(reco::deltaR(thisP4, fsrPtr->p4()) < reco::deltaR(fs.daughter(fs.get4LPartner(iLep))->p4(), fsrPtr->p4()))
	  thisP4 += fsrPtr->p4();
      partP4.push_back(TLorentzVector());
      partP4.back().SetPtEtaPhiM(thisP4.pt(), thisP4.eta(), thisP4.phi(), thisP4.mass());
//      std::cout << "bare lepton id:pt,eta,phi,m" << partID.back() << ":" << fs.daughter(iLep)->pt() << "," 
//		<< fs.daughter(iLep)->eta() << "," << fs.daughter(iLep)->phi() << std::endl;
//      std::cout << "id:pt,eta,phi,m = " << partID.back() << ":" << thisP4.Pt() << "," 
//		<< thisP4.Eta() << "," << thisP4.Phi() << "," << partP4.back().M() << std::endl;
    }

  double pSig, pBkg;
  MEM_.computePm4l(partP4, partID, syst, pSig, pBkg);

  sigProb = float(pSig);
  bkgProb = float(pBkg);
}


void MiniAODHZZMEEmbedder::beginJob(){}
void MiniAODHZZMEEmbedder::endJob(){}


#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(MiniAODHZZMEEmbedder);



#endif // #ifdef HZZMELA
