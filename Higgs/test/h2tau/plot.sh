#!/bin/bash
# Plot for 7TeV and 8TeV

set -o nounset
set -o errexit

export jobid='2012-07-29-8TeV-Higgs'
python PlotEM.py

export jobid='2012-07-29-7TeV-Higgs'
python PlotEM.py
