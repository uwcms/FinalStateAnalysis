import string

'''
Automate generation of classes_def.xml
'''

final_states = [
    #"PATFinalState", # special case

    # Already generated
    #"PATElecElecFinalState",
    #"PATElecMuFinalState",
    #"PATElecTauFinalState",
    #"PATMuTauFinalState",
    #"PATMuMuFinalState",
    #"PATTauTauFinalState",
    #"PATElecElecElecFinalState",
    #"PATElecElecMuFinalState",
    #"PATElecElecTauFinalState",
    #"PATElecMuMuFinalState",
    #"PATElecMuTauFinalState",
    #"PATMuMuMuFinalState",
    #"PATMuMuTauFinalState",
    #"PATMuTauTauFinalState",
    #"PATTauTauTauFinalState",

    #"PATElecElecElecElecFinalState",
    #"PATElecElecElecMuFinalState",
    #"PATElecElecElecTauFinalState",
    #"PATElecElecMuMuFinalState",
    #"PATElecElecMuTauFinalState",
    #"PATElecElecTauTauFinalState",
    #"PATElecMuMuMuFinalState",
    #"PATElecMuMuTauFinalState",
    #"PATElecMuTauTauFinalState",
    #"PATElecTauTauTauFinalState",
    #"PATMuMuMuMuFinalState",
    #"PATMuMuMuTauFinalState",
    #"PATMuMuTauTauFinalState",
    #"PATMuTauTauTauFinalState",
    #"PATTauTauTauTauFinalState",

    "PATElecPhoFinalState",
    "PATMuPhoFinalState",
    "PATTauPhoFinalState",
    "PATPhoPhoFinalState",
    "PATElecElecPhoFinalState",
    "PATElecMuPhoFinalState",
    "PATElecTauPhoFinalState",
    "PATElecPhoPhoFinalState",
    "PATMuMuPhoFinalState",
    "PATMuTauPhoFinalState",
    "PATMuPhoPhoFinalState",
    "PATTauTauPhoFinalState",
    "PATTauPhoPhoFinalState",
    "PATPhoPhoPhoFinalState",
    "PATElecElecElecPhoFinalState",
    "PATElecElecMuPhoFinalState",
    "PATElecElecTauPhoFinalState",
    "PATElecElecPhoPhoFinalState",
    "PATElecMuMuPhoFinalState",
    "PATElecMuTauPhoFinalState",
    "PATElecMuPhoPhoFinalState",
    "PATElecTauTauPhoFinalState",
    "PATElecTauPhoPhoFinalState",
    "PATElecPhoPhoPhoFinalState",
    "PATMuMuMuPhoFinalState",
    "PATMuMuTauPhoFinalState",
    "PATMuMuPhoPhoFinalState",
    "PATMuTauTauPhoFinalState",
    "PATMuTauPhoPhoFinalState",
    "PATMuPhoPhoPhoFinalState",
    "PATTauTauTauPhoFinalState",
    "PATTauTauPhoPhoFinalState",
    "PATTauPhoPhoPhoFinalState",
    "PATPhoPhoPhoPhoFinalState"
    
]

template = string.Template('''
  <class name="${TheClass}"/>
  <class name="${TheClass}Collection"/>
  <class name="edm::Wrapper<${TheClass}>"/>
  <class name="edm::Wrapper<${TheClass}Collection>"/>
  <class name="edm::Ref<${TheClass}Collection,${TheClass},edm::refhelper::FindUsingAdvance<${TheClass}Collection,${TheClass}> >"/>
  <class name="edm::RefVector<${TheClass}Collection,${TheClass},edm::refhelper::FindUsingAdvance<${TheClass}Collection,${TheClass}> >"/>
  <class name="edm::RefProd<${TheClass}Collection>"/>
  <class name="edm::Ptr<${TheClass}>"/>
''')

for final_state in final_states:
    print template.substitute(TheClass=final_state)
