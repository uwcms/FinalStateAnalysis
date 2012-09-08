#!/bin/bash
# Plot all of the analysis

set -o nounset
set -o errexit

source jobid.sh
export jobid=$jobid7
python WHPlotterEMT.py
python WHPlotterMMT.py
python PlotControlZMM.py
python PlotControlEM.py
rake cards
#DumpMCvsData.py --files results/$jobid/FakeRatesMM/*root --lumifiles inputs/$jobid/*sum  --rebin 1  --outputdir results/$jobid/plots/FakeRatesMM_dump
#DumpMCvsData.py --files results/$jobid/FakeRatesME/*root --lumifiles inputs/$jobid/*sum  --rebin 1  --outputdir results/$jobid/plots/FakeRatesME_dump
#DumpMCvsData.py --files results/$jobid/FakeRatesMMM/*root --lumifiles inputs/$jobid/*sum  --rebin 1  --outputdir results/$jobid/plots/FakeRatesMMM_dump

export jobid=$jobid8
python WHPlotterEMT.py
python WHPlotterMMT.py
python PlotControlZMM.py
python PlotControlEM.py
rake cards
#DumpMCvsData.py --files results/$jobid/FakeRatesMM/*root --lumifiles inputs/$jobid/*sum  --rebin 1  --outputdir results/$jobid/plots/FakeRatesMM_dump
#DumpMCvsData.py --files results/$jobid/FakeRatesME/*root --lumifiles inputs/$jobid/*sum  --rebin 1  --outputdir results/$jobid/plots/FakeRatesME_dump
#DumpMCvsData.py --files results/$jobid/FakeRatesMMM/*root --lumifiles inputs/$jobid/*sum  --rebin 1  --outputdir results/$jobid/plots/FakeRatesMMM_dump
