#!/bin/bash
export NOFWLITE=blah
set -e # fail immediately on error

cp wh_shapes_raw.root wh_shapes.root
echo "Adding statistical shape uncertainties"
./addStatShapes.py wh_shapes.root

rm cards/*
echo "Building data cards"
python makeDataCard.py

echo "Hybridizing cards"
bash make_hybrid_cards.sh

tar cvzf wh_cards.tgz wh_shapes.root cards/all_channels_*.card

echo "Doing asymptotic limits for all cards"
#combine $card -M Asymptotic -H ProfileLikelihood | limit2JSON.py > $card.asymp.json

ls cards/*.card | xargs -n 1 -P 4 -I % sh -c  "combine % -n %.root -M Asymptotic -H ProfileLikelihood | limit2JSON.py > %.asymp.json"

python plot_limit.py all_channels_noHWW
python plot_limit.py all_channels_withHWW
python plot_limit.py all_channels_hybrid
#python plot_limit.py emm_channels
python plot_limit.py emt_channels_noHWW
python plot_limit.py emt_channels_withHWW
python plot_limit.py emt_channels_hybrid
python plot_limit.py mmt_channels_noHWW
python plot_limit.py mmt_channels_withHWW
python plot_limit.py mmt_channels_hybrid
