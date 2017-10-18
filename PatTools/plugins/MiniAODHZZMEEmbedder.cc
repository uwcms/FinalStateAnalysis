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
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

// FSA includes
#include "FinalStateAnalysis/DataFormats/interface/PATQuadLeptonFinalStates.h"
#include "FinalStateAnalysis/DataFormats/interface/PATQuadLeptonFinalStatesFwd.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalState.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateFwd.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEvent.h"
#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEventFwd.h"
#include "FinalStateAnalysis/PatTools/data/HZZMEProcesses.h"

// ZZMatrixElement includes
#include "ZZMatrixElement/MEMCalculators/interface/MEMCalculators.h"


template<class... Ls>
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
  const float getZZME(const PATQuadFinalStateT<Ls...>& fs, MEMNames::Processes proc, 
		      MEMNames::MEMCalcs calc, const std::string& fsrLabel,
                      bool useJets);
  // Calculate the 4l SM Higgs and background probability for fs under systematics assumption syst
  // Outputs by setting sigProb and bkgProb rather than returning
  void getPm4l(const PATQuadFinalStateT<Ls...>& fs, MEMNames::SuperKDsyst syst, float& sigProb, 
	       float& bkgProb, const std::string& fsrLabel);
  // Tag of final states to calculate MEs for
  edm::EDGetTokenT<edm::View<PATFinalState> > src_;
  // MEM calculator object
  MEMs MEM_; 
  // List of probabilities to calculate
  const std::vector<std::string> processes_;
  // For each process, a boolean indicating if we should include jets
  std::vector<bool> processUsesJets_;
  // Label of FSR candidate photons
  const std::string fsrLabel_;
  // The process and calculator for each probability we might to calculate are stored in 
  // a pair, keyed to the same string they would be keyed to in the 
  const std::unordered_map<std::string, std::pair<MEMNames::Processes, MEMNames::MEMCalcs> > processInfo_;
  const std::unordered_map<std::string, std::pair<MEMNames::Processes, MEMNames::MEMCalcs> > processInfoJets_;
  // ME calculation parameters
  const unsigned int energy_; // collision energy
  const double mH_; // Higgs mass hypothesis
  const std::string pdf_; // PDF to use
};


template<class... Ls>
MiniAODHZZMEEmbedder<Ls...>::MiniAODHZZMEEmbedder(const edm::ParameterSet& iConfig) :
  src_(consumes<edm::View<PATFinalState> >(iConfig.exists("src") ?
       iConfig.getParameter<edm::InputTag>("src") :
       edm::InputTag("finalStateeeee"))),
  processes_(iConfig.exists("processes") ?
	     iConfig.getParameter<std::vector<std::string> >("processes") :
	     std::vector<std::string>()),
  fsrLabel_(iConfig.exists("fsrLabel") ?
	    iConfig.getParameter<std::string>("fsrLabel") :
	    std::string("FSRCand")),
  processInfo_(getHZZMEProcessInfo()),
  processInfoJets_(getHZZMEProcessInfoJets()),
  energy_(iConfig.exists("energy") ? 
	  iConfig.getParameter<unsigned int>("energy") :
	  13),
  mH_(iConfig.exists("mH") ? 
      iConfig.getParameter<double>("mH") :
      125),
  pdf_(iConfig.exists("pdf") ? 
       iConfig.getParameter<std::string>("pdf") :
       std::string("CTEQ6L"))
{
  MEM_ = MEMs(energy_, mH_, pdf_);

  // Check to make sure all desired processes are valid, see which need jet info
  for(auto iProc = processes_.begin(); 
      iProc != processes_.end(); ++iProc)
    {
      if(processInfo_.find(*iProc) == processInfo_.end())
        {
          if(processInfoJets_.find(*iProc) == processInfoJets_.end())
            throw cms::Exception("MiniAODHZZMEEmbedder") << "Process " << *iProc
                                                         << " is not defined in "
                                                         << "PatTools/data/HZZMEProcesses.h.\n" 
                                                         << "Please define it there or fix your typo.\n";
          processUsesJets_.push_back(true);
        }
      else
        processUsesJets_.push_back(false);
    }

  produces<PATFinalStateCollection>();
}


template<class... Ls>
void MiniAODHZZMEEmbedder<Ls...>::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) 
{
  std::unique_ptr<PATFinalStateCollection> output(new PATFinalStateCollection);

  edm::Handle<edm::View<PATFinalState> > finalStatesIn;
  iEvent.getByToken(src_, finalStatesIn);

  for (size_t iFS = 0; iFS < finalStatesIn->size(); ++iFS) 
    {
      PATQuadFinalStateT<Ls...> * embedInto = 
	dynamic_cast<PATQuadFinalStateT<Ls...>* >(finalStatesIn->ptrAt(iFS)->clone());

      for(size_t iProc = 0; iProc < processes_.size(); ++iProc)
	{
          const std::string processName = processes_.at(iProc);
          MEMNames::Processes proc;
          MEMNames::MEMCalcs calc;
          bool useJets = processUsesJets_.at(iProc);
          if(useJets)
            {
              proc = processInfoJets_.at(processName).first;
              calc = processInfoJets_.at(processName).second;
            }
          else
            {
              proc = processInfo_.at(processName).first;
              calc = processInfo_.at(processName).second;
            }
	  float ME = getZZME(*embedInto, proc, calc, fsrLabel_, useJets);
	  embedInto->addUserFloat(processes_.at(iProc), ME);
	}

      // Embed SM Higgs and background m4l probabilities, as in datacards
      float p0plus_m4l, bkg_m4l;
      getPm4l(*embedInto, MEMNames::kNone, p0plus_m4l, bkg_m4l, fsrLabel_);
      embedInto->addUserFloat("p0plus_m4l", p0plus_m4l);
      embedInto->addUserFloat("bkg_m4l", bkg_m4l);

      output->push_back(embedInto); // takes ownership
    }

  iEvent.put(std::move(output));
}


template<class... Ls>
const float MiniAODHZZMEEmbedder<Ls...>::getZZME(const PATQuadFinalStateT<Ls...> & fs, 
						 MEMNames::Processes proc, 
						 MEMNames::MEMCalcs calc, const std::string& fsrLabel,
						 bool includeJets)
{
  std::vector<TLorentzVector> partP4 = std::vector<TLorentzVector>();
  std::vector<int> partID = std::vector<int>();
  for(size_t iLep = 0; iLep < fs.numberOfDaughters(); iLep++)
    {
      partID.push_back(fs.daughter(iLep)->pdgId());
      PATFinalState::LorentzVector thisP4 = fs.daughterP4WithUserCand(iLep, 
                                                                      fsrLabel);
      partP4.push_back(TLorentzVector());
      partP4.back().SetPtEtaPhiM(thisP4.pt(), thisP4.eta(), thisP4.phi(), thisP4.mass());
    }
  
  // if this process cares about jets, add them too
  if(includeJets)
    {
      for(size_t j = 0; j < 2; ++j)
	{
	  if(j < fs.evt()->jets().size())
	    {
	      partP4.push_back(TLorentzVector());
	      PATFinalState::LorentzVector thisP4 = fs.evt()->jets().at(j).p4();
	      partP4.back().SetPtEtaPhiM(thisP4.pt(), thisP4.eta(), thisP4.phi(), thisP4.mass());
	    }
	  else
	    return -1;
	  partID.push_back(0); // jets are always ID 0 in MEM
	}
    }

  double ME;
  MEM_.computeME(proc, calc, partP4, partID, ME);

  return ME;
}

// Assigns the answers to sigProb and bkgProb rather than returning them
template<class... Ls>
void MiniAODHZZMEEmbedder<Ls...>::getPm4l(const PATQuadFinalStateT<Ls...> & fs, 
					  MEMNames::SuperKDsyst syst, float& sigProb, 
					  float& bkgProb, const std::string& fsrLabel)
{
  std::vector<TLorentzVector> partP4 = std::vector<TLorentzVector>();
  std::vector<int> partID = std::vector<int>();
  for(unsigned int iLep = 0; iLep < fs.numberOfDaughters(); iLep++)
    {
      partID.push_back(fs.daughter(iLep)->pdgId());
      PATFinalState::LorentzVector thisP4 = fs.daughterP4WithUserCand(iLep, fsrLabel);
      partP4.push_back(TLorentzVector());
      partP4.back().SetPtEtaPhiM(thisP4.pt(), thisP4.eta(), thisP4.phi(), thisP4.mass());
    }

  double pSig, pBkg;
  MEM_.computePm4l(partP4, partID, syst, pSig, pBkg);

  sigProb = float(pSig);
  bkgProb = float(pBkg);
}

template<class... Ls>
void MiniAODHZZMEEmbedder<Ls...>::beginJob(){}
template<class... Ls>
void MiniAODHZZMEEmbedder<Ls...>::endJob(){}

#include "FWCore/Framework/interface/MakerMacros.h"
typedef MiniAODHZZMEEmbedder<pat::Electron, pat::Electron, pat::Electron, pat::Electron> MiniAODHZZMEEmbedderElecElecElecElec;
typedef MiniAODHZZMEEmbedder<pat::Electron, pat::Electron, pat::Muon, pat::Muon> MiniAODHZZMEEmbedderElecElecMuMu;
typedef MiniAODHZZMEEmbedder<pat::Muon, pat::Muon, pat::Muon, pat::Muon> MiniAODHZZMEEmbedderMuMuMuMu;
DEFINE_FWK_MODULE(MiniAODHZZMEEmbedderElecElecElecElec);
DEFINE_FWK_MODULE(MiniAODHZZMEEmbedderElecElecMuMu);
DEFINE_FWK_MODULE(MiniAODHZZMEEmbedderMuMuMuMu);



#endif // #ifdef HZZMELA
