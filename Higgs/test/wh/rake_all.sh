#!/bin/bash

set -o nounset
set -o errexit

export jobid='2012-07-23-7TeV-Higgs'
rake fakerates
rake fits
rake mmt
rake emt
#rake eet

export jobid='2012-07-23-8TeV-Higgs'
rake fakerates
rake fits
rake mmt
rake emt
#rake eet

