/*
 * TMegaSelectionFactory contains logic on how to build TMegaSelections.
 *
 * Author: Evan K. Friis, UW Madison
 */

class TMegaSelectionFactory {
  public:
    TMegaSelectionFactory(ROOT::TBranchProxyDirector* director);

    std::auto_ptr<TMegaSelection> MakeIntCut(const std::string& branch,
        const std::string& op, Int_t value) const;

    std::auto_ptr<TMegaSelection> MakeFloatCut(const std::string& branch,
        const std::string& op, Float_t value) const;

    std::auto_ptr<TMegaSelection> MakeDoubleCut(const std::string& branch,
        const std::string& op, Double_t value) const;

  private:
    template<typename T>
      std::auto_ptr<TMegaSelection> MakeImpl(const std::string& branch,
        const std::string& op, const T& value) const;

    ROOT::TBranchProxyDirector* director_;
};
