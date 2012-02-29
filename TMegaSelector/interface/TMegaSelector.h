#ifndef TMEGASELECTOR_F965XW8K
#define TMEGASELECTOR_F965XW8K

/*
 * TMegaSelector
 *
 * An enhanced version of TSelector.
 *
 */

#include <map>
#include <memory>
#include <string>
#include <utility>

#include <TBranchProxyDirector.h>
#include "TBranchProxy.h"
#include "TSelector.h"

#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelection.h"
#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelectionFactory.h"
#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelectionSet.h"

class TMegaSelector : public TSelector {
  public:
    TMegaSelector(TTree *tree=0);
    virtual ~TMegaSelector();

    TTree *chain;

    // Abstract interface for derived classes
    virtual void MegaInit(TTree* /*tree*/) {}
    virtual Bool_t MegaNotify() { return true; }
    virtual void MegaBegin() {}
    virtual void MegaSlaveBegin() {}
    virtual Bool_t MegaProcess(Long64_t entry)=0;
    virtual void MegaSlaveTerminate() {}
    virtual void MegaTerminate() {}

    // Add a TMegaSelection to the named selection set.  Does not take
    // ownership.
    void AddToSelection(const std::string& name, const TMegaSelection& select);

    // Add a TMegaSelection to the named selection set.  Takes ownershipt.
    void AddToSelection(const std::string& name,
        std::auto_ptr<TMegaSelection> select);

    // Get the TMegaSelectionSet with the given name.  If it doesn't exists,
    // this will return null.
    TMegaSelectionSet* GetSelectionSet(const std::string& name) const;

    // Set which selection set to use for filtering.  Any entries (rows) which
    // do not pass this selection will not be passed to MegaProcess.
    void SetFilterSelection(const std::string&);

    /// Get the total number of processed entries
    unsigned int GetProcessedEntries() const;

    /// Get the number of entries that were filtered
    unsigned int GetFilteredEntries() const;

    /// Get the factory to build TMegaSelections
    const TMegaSelectionFactory* factory() const;

    /// Do not read branch on calls to chain->GetEntry()
    void DisableBranch(const std::string& branch);

    /// Do read branch on calls to chain->GetEntry()
    void EnableBranch(const std::string& branch);

    // Needed for ROOT to call the virtual functions correctly
    virtual Int_t Version() const { return 2; }

    ClassDef( TMegaSelector, 1 );   // Enhanced TSelector

  private:
    void Init(TTree* tree);
    Bool_t Notify();
    void Begin(TTree*);
    void SlaveBegin(TTree*);
    void SlaveTerminate();
    void Terminate();
    Bool_t Process(Long64_t entry);

    // Keep track of entries processed
    unsigned int filteredEntries_;
    unsigned int allEntries_;

    ROOT::TBranchProxyDirector director_; //!Manages the proxies

    // Factory class to build selections
    std::auto_ptr<TMegaSelectionFactory> factory_;

    // The entry and tree currently being processed
    Long64_t currentEntry_;

    typedef std::map<std::string, TMegaSelectionSet*> SelectionSetMap;
    SelectionSetMap selections_;
    // The selection to use for filtering calls to MegaProcess();
    TMegaSelectionSet* filterSelection_;

    // These get applied on each call to Init()
    std::vector<std::pair<std::string, int> > branchCommands_;
};

#endif /* end of include guard: TMEGASELECTOR_F965XW8K */
