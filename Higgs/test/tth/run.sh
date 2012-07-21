#!/bin/bash

# Run me to analyze VH signal.

set -o errexit
set -o nounset
export jobid=2012-07-19-7TeV-Higgs

export isVH=True
rake results/$jobid/AnalyzeTTHSignal/VH_120.root
export isVH=False
rake results/$jobid/AnalyzeTTHSignal/TTplusJets_madgraph.root
