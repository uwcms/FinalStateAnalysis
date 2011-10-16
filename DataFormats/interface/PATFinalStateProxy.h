#ifndef PATFINALSTATEPROXY_7FWRI39L
#define PATFINALSTATEPROXY_7FWRI39L

/*
 *  A Proxy class which wraps a PATFinalState object.  Essentially wraps a
 *  boost::shared_ptr and allows
 *
 *  Takes ownership of a FinalState passed via the constructor.
 */

#include <boost/shared_ptr.hpp>
class PATFinalState;

class PATFinalStateProxy {
  public:
    PATFinalStateProxy(PATFinalState* finalState);
    PATFinalStateProxy();
    const PATFinalState* get() const;
    const PATFinalState* operator->() const;
  private:
    boost::shared_ptr<PATFinalState> finalState_;
};

#endif /* end of include guard: PATFINALSTATEPROXY_7FWRI39L */
