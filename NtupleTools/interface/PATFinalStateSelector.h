#ifndef PATFINALSTATESELECTOR_3LY6MT3N
#define PATFINALSTATESELECTOR_3LY6MT3N

#include "PhysicsTools/SelectorUtils/interface/Selector.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

class PATFinalState;
typedef std::vector<const PATFinalState*> PATFinalStatePtrs;
namespace edm {
  class ParameterSet;
}

class PATFinalStateSelection : public Selector<PATFinalStatePtrs> {
  public:
    PATFinalStateSelection(const edm::ParameterSet& pset);
  private:
}



#endif /* end of include guard: PATFINALSTATESELECTOR_3LY6MT3N */
