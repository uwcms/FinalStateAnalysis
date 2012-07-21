#!/bin/bash

# Run me to analyze VH signal.

set -o errexit
set -o nounset
export jobid=2012-07-19-7TeV-Higgs

rake results/$jobid/AnalyzeTTHSignal/VH_120.root
