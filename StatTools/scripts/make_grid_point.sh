#!/bin/bash
# Run a single limit combination job
# Usage:
# ./make_grid_point.sh [input_card.root] [seed] [point] [toys] [extra_options]

WORKSPACE=$1
shift
SEED=$1
shift
POINT=$1
shift
TOYS=$1
shift
EXTRAS="$@"

COMBINE=${CMSSW_BASE}/bin/${SCRAM_ARCH}/combine

$COMBINE $WORKSPACE -M HybridNew -s $SEED --singlePoint $POINT \
  --saveToys --saveHybridResult -T $TOYS

mv higgsCombine*.root $outputFileName
