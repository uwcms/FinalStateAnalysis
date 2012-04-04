#!/bin/bash

# Run megadebug on all of the UW events
# If you save this to a file, view it with less -r

megadebug=$fsa/TMegaSelector/scripts/megadebug 

echo "Debugging MMMT"

#$megadebug AnalyzeMMMT.py uw_events_ntuple.txt /mmmt/final/Ntuple \
  #unique- base_selections+  hadronic_tau_id m3_id \
  #--events 

echo "Debugging MMET"

$megadebug AnalyzeMMET.py uw_events_ntuple.txt /emmt/final/Ntuple \
  unique base_selections+   hadronic_tau_id e_id+ \
  --events 163334,499,286336207

#echo "Debugging MMME"

#$megadebug AnalyzeMMME.py uw_events_ntuple.txt /emmm/final/Ntuple \
  #unique+ base_selections+  e_id m3_id  \
  #--events 179889,195,291267852 177184,10,12646620

#echo "Debugging EETT"

#$megadebug AnalyzeEETT.py uw_events_ntuple.txt /eett/final/Ntuple \
  #unique- base_selections+  hadronic_t1_id hadronic_t2_id  \
  #--events 178100,335,455090581

#echo "Debugging EEET"

#$megadebug AnalyzeEEET.py uw_events_ntuple.txt /eeet/final/Ntuple \
  #unique- base_selections+  e3_id  hadronic_tau_id \
  #--events 172252,40,47105541 177718,469,736335702

## Don't need to do MMTT
