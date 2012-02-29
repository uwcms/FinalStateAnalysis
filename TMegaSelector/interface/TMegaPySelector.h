// Author: Wim Lavrijsen   March 2008

#ifndef ROOT_TMegaPySelector
#define ROOT_TMegaPySelector

//////////////////////////////////////////////////////////////////////////////
//                                                                          //
// TMegaPySelector                                                              //
//                                                                          //
// Python base class equivalent of PROOF TSelector.                         //
//                                                                          //
//////////////////////////////////////////////////////////////////////////////


#include "FinalStateAnalysis/TMegaSelector/interface/TMegaSelector.h"

// Python
struct _object;
typedef _object PyObject;


class TMegaPySelector : public TMegaSelector {
public:
   using TSelector::fStatus;
// using TSelector::fAbort;
   using TSelector::fOption;
   using TSelector::fObject;
   using TSelector::fInput;
   using TSelector::fOutput;

public:
// ctor/dtor ... cctor and assignment are private in base class
   TMegaPySelector( TTree* /* tree */ = 0, PyObject* self = 0 );
   virtual ~TMegaPySelector();

// TSelector set of forwarded (overridden) methods
   virtual Int_t  GetEntry( Long64_t entry, Int_t getall = 0 );
   virtual Bool_t MegaNotify();

   virtual void   MegaInit( TTree* tree );
   virtual void   MegaBegin();
   virtual void   MegaSlaveBegin();
   virtual Bool_t MegaProcess( Long64_t entry );
   virtual void   MegaSlaveTerminate();
   virtual void   MegaTerminate();
   virtual Int_t  Version() const;

   // Add an object to the fOutput list
   virtual void AddToOutput(TObject* object);

   virtual void Abort( const char* why, EAbort what = kAbortProcess );

   ClassDef( TMegaPySelector, 1 );   //Python equivalent base class for PROOF

private:
// private helpers for forwarding to python
   void SetupPySelf();
   PyObject* CallSelf( const char* method, PyObject* pyobject = 0 );

private:
   PyObject* fPySelf;              //! actual python object
};

#endif
