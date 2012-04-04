#!/bin/bash

# Run megadebug on all of abdollah's events
# If you save this to a file, view it with less -r

megadebug=$fsa/TMegaSelector/scripts/megadebug 

echo "Debugging MMMT"

$megadebug AnalyzeMMMT.py zh_events_ntuple.txt /mmmt/final/Ntuple \
  unique- base_selections+  hadronic_tau_id m3_id \
  --events 172014:58:91568080 177139,143,226464086 172635,159,238215970

echo "Debugging MMET"

$megadebug AnalyzeMMET.py zh_events_ntuple.txt /emmt/final/Ntuple \
  unique- base_selections+   hadronic_tau_id e_id+ \
  --events 171178,12,11119024 161217,396,346679510

echo "Debugging MMME"

$megadebug AnalyzeMMME.py zh_events_ntuple.txt /emmm/final/Ntuple \
  unique+ base_selections+  e_id m3_id  \
  --events 179889,195,291267852 177184,10,12646620

echo "Debugging EETT"

$megadebug AnalyzeEETT.py zh_events_ntuple.txt /eett/final/Ntuple \
  unique- base_selections+  hadronic_t1_id hadronic_t2_id  \
  --events 178100,335,455090581

echo "Debugging EEET"

$megadebug AnalyzeEEET.py zh_events_ntuple.txt /eeet/final/Ntuple \
  unique- base_selections+  e3_id  hadronic_tau_id \
  --events 172252,40,47105541 177718,469,736335702
