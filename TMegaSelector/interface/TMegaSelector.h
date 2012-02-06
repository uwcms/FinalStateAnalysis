/*
 * TMegaSelector
 *
 * An enhanced version of TSelector.
 *
 */

#include "TSelector.h"
#include <TBranchProxyDirector.h>
#include "TBranchProxy.h"
#include <string>
#include <map>

class TMegaSelectionSet;

class TMegaSelector : public TSelector {
  public:
    TMegaSelector(TTree *tree=0);
    virtual ~TMegaSelector();

    TTree *chain;

    // Abstract interface for derived classes
    virtual void MegaInit(TTree* tree)=0;
    virtual Bool_t MegaNotify()=0;
    virtual void MegaBegin()=0;
    virtual void MegaSlaveBegin()=0;
    virtual Bool_t MegaProcess(Long64_t entry)=0;
    virtual void MegaSlaveTerminate()=0;
    virtual void MegaTerminate()=0;

  private:
    void Init(TTree* tree);
    Bool_t Notify();
    void Begin(TTree*);
    void SlaveBegin(TTree*);
    Bool_t Process(Long64_t entry);
    void SlaveTerminate();
    void Terminate();

    ROOT::TBranchProxyDirector director_; //!Manages the proxys

    // The entry and tree currently being processed
    Long64_t currentEntry_;

    std::map<std::string, TMegaSelectionSet*> selections_;
    // The selection to use for filtering calls to MegaProcess();
    TMegaSelectionSet* filterSelection_;
};
