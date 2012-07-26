#!/bin/bash
# Run all of the analysis

set -o nounset
set -o errexit

export jobid='2012-07-24-7TeV-Higgs'
rake fakerates
#rake fits
rake mmt
rake emt
rake mmcontrol
rake emcontrol

export jobid='2012-07-24-8TeV-Higgs'
rake fakerates
#rake fits
rake mmt
rake emt
rake mmcontrol
rake emcontrol
