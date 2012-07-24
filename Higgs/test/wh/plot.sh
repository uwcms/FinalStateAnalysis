export jobid='2012-07-22-7TeV-Higgs'
#rake fakerates
#rake fits
python WHPlotterEMT.py
#python WHPlotterEET.py
python WHPlotterMMT.py
DumpMCvsData.py --files results/$jobid/FakeRatesMM/*root --lumifiles inputs/$jobid/*sum  --rebin 1  --outputdir results/$jobid/plots/FakeRatesMM_dump
DumpMCvsData.py --files results/$jobid/FakeRatesME/*root --lumifiles inputs/$jobid/*sum  --rebin 1  --outputdir results/$jobid/plots/FakeRatesME_dump
DumpMCvsData.py --files results/$jobid/FakeRatesMMM/*root --lumifiles inputs/$jobid/*sum  --rebin 1  --outputdir results/$jobid/plots/FakeRatesMMM_dump
#rake cards
#rake copycards

export jobid='2012-07-22-8TeV-Higgs'
#rake fakerates
#rake fits
python WHPlotterEMT.py
#python WHPlotterEET.py
python WHPlotterMMT.py
DumpMCvsData.py --files results/$jobid/FakeRatesMM/*root --lumifiles inputs/$jobid/*sum  --rebin 1  --outputdir results/$jobid/plots/FakeRatesMM_dump
DumpMCvsData.py --files results/$jobid/FakeRatesME/*root --lumifiles inputs/$jobid/*sum  --rebin 1  --outputdir results/$jobid/plots/FakeRatesME_dump
DumpMCvsData.py --files results/$jobid/FakeRatesMMM/*root --lumifiles inputs/$jobid/*sum  --rebin 1  --outputdir results/$jobid/plots/FakeRatesMMM_dump

#rake cards
#rake copycards

