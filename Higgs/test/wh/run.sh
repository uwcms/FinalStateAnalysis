#!/bin/bash
# Run all of the analysis

set -o nounset
set -o errexit

source jobid.sh

export jobid=$jobid7
rake fakerates
#rake fits
rake mmt
rake emt
rake mmcontrol
rake emcontrol

export jobid=$jobid8
rake fakerates
#rake fits
rake mmt
rake emt
rake mmcontrol
rake emcontrol
