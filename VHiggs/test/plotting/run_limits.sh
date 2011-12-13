#!/bin/bash
export NOFWLITE=blah

echo "Adding statistical shape uncertainties"
./addStatShapes.py wh_shapes.root

echo "Building data cards"
python makeDataCard.py

tar cvzf wh_cards.tgz wh_shapes.root cards/all_channels_*.card

echo "Doing asymptotic limits for all cards"
#combine $card -M Asymptotic -H ProfileLikelihood | limit2JSON.py > $card.asymp.json

ls cards/*.card | xargs -n 1 -P 4 -I % sh -c \
  "combine % -n %.root -M Asymptotic -H ProfileLikelihood | limit2JSON.py > %.asymp.json"

python plot_limit.py all_channels
python plot_limit.py emm_channels
python plot_limit.py emt_channels
python plot_limit.py mmt_channels

#ntoys=50

#for card in cards/*.card
#do
  #echo "Doing expected limits for $card"
  #combine $card -t $ntoys | limit2JSON.py > $card.exp.json
  #echo "Doing observed limits for $card"
  #combine $card | limit2JSON.py > $card.obs.json
  #echo "Doing asymptotic limits for $card"
#done
