#!/bin/bash 

pick=$fsa/MetaData/scripts/pick.py 

pickscript=event_lists/my_event_picker.sh

rm -f $pickscript
touch $pickscript

$pick DoubleMu results/analysis/mmmt/*events --output {dataset}-uw-mmmt >> $pickscript

$pick DoubleMu results/analysis/mmet/*events --output {dataset}-uw-mmet >> $pickscript

$pick DoubleMu results/analysis/mmtt/*events --output {dataset}-uw-mmtt >> $pickscript

$pick DoubleMu results/analysis/mmme/*events --output {dataset}-uw-mmme >> $pickscript

$pick DoubleElectron results/analysis/eemt/*events --output {dataset}-uw-eemt >> $pickscript

$pick DoubleElectron results/analysis/eeet/*events --output {dataset}-uw-eeet >> $pickscript

$pick DoubleElectron results/analysis/eett/*events --output {dataset}-uw-eett >> $pickscript

$pick DoubleElectron results/analysis/eeem/*events --output {dataset}-uw-eeem >> $pickscript
