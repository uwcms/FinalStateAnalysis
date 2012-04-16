#!/bin/bash

# Stupid script to dump ZH event counts

for channel in mmtt eett mmmt eemt mmet eeet mmme eeem
do
  echo "================="
  echo "$channel "
  echo -n " final: "
  ls results/analysis/$channel/*events | grep -v anti | xargs combine_event_lists.py --count
  echo ""
  echo  -n "l1 anti: " 
  combine_event_lists.py results/analysis/$channel/*l1*events --count
  echo -n "/" 
  python zh_xcheck/abdollahs_counts.py $channel 1
  echo  -n "l2 anti: " 
  combine_event_lists.py results/analysis/$channel/*l2*events --count
  echo -n "/" 
  python zh_xcheck/abdollahs_counts.py $channel 2
  echo  -n "both anti: " 
  combine_event_lists.py results/analysis/$channel/*both*events --count
  echo -n "/" 
  python zh_xcheck/abdollahs_counts.py $channel 0
done
