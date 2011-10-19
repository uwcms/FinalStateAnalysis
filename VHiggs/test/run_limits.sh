#!/bin/bash

# Merge all of our channel shapes
hadd -f all_shapes.root emt_shapes.root mmt_shapes.root
# Generate the cards
python makeDataCard.py

ntoys=50

for card in cards/*.card
do
  combine $card -t $ntoys -M Asymptotic | limit2JSON.py > $card.exp.json
  combine $card | limit2JSON.py > $card.obs.json
done

