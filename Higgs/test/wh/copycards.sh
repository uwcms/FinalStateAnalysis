#!/bin/bash
# Copy data cards to the HiggsAnalysis/HiggsTauTau/setup/vhtt folder

set -o nounset
set -o errexit

source jobid.sh

export jobid=$jobid7
rake copycards

export jobid=$jobid8
rake copycards
