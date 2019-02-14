import string

'''
Automate generation of classes_def.xml
'''

final_states = [
    #"PATFinalState", # special case

    # Already generated
    "PATElecFinalState",
    "PATMuFinalState",
    "PATTauFinalState",
    "PATPhoFinalState",
    "PATJetFinalState",

    "PATElecElecFinalState",
    "PATElecMuFinalState",
    "PATElecTauFinalState",
    "PATMuTauFinalState",
    "PATMuMuFinalState",
    "PATTauTauFinalState",
    "PATElecElecElecFinalState",
    "PATElecElecMuFinalState",
    "PATElecElecTauFinalState",
    "PATElecMuMuFinalState",
    "PATElecMuTauFinalState",
    "PATMuMuMuFinalState",
    "PATMuMuTauFinalState",
    "PATElecTauTauFinalState",
    "PATMuTauTauFinalState",
    "PATTauTauTauFinalState",

    "PATElecElecElecElecFinalState",
    "PATElecElecElecMuFinalState",
    "PATElecElecElecTauFinalState",
    "PATElecElecMuMuFinalState",
    "PATElecElecMuTauFinalState",
    "PATElecElecTauTauFinalState",
    "PATElecMuMuMuFinalState",
    "PATElecMuMuTauFinalState",
    "PATElecMuTauTauFinalState",
    "PATElecTauTauTauFinalState",
    "PATMuMuMuMuFinalState",
    "PATMuMuMuTauFinalState",
    "PATMuMuTauTauFinalState",
    "PATMuTauTauTauFinalState",
    "PATTauTauTauTauFinalState",

    "PATElecElecElecElecElecFinalState",
    "PATElecElecElecElecMuFinalState",
    "PATElecElecElecMuMuFinalState",
    "PATElecElecMuMuMuFinalState",
    "PATElecMuMuMuMuFinalState",
    "PATMuMuMuMuMuFinalState",

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

minimal_template = string.Template('''
  <class name="${TheClass}"/>
  <class name="edm::Wrapper<${TheClass}>"/>
  <class name="${TheClass}Collection"/>
  <class name="edm::Wrapper<${TheClass}Collection>"/>
''')


for final_state in final_states:
    if final_state.count('Pho') > 2:
        continue
    if final_state.count('Tau') and final_state.count('Pho'):
        continue
    print minimal_template.substitute(TheClass=final_state)
