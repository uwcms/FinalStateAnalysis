#!/bin/bash

# Analyze the e-mu channel

set -o nounset
set -o errexit

export jobid='2012-07-29-7TeV-Higgs'
rake em

export jobid='2012-07-29-8TeV-Higgs'
rake em
