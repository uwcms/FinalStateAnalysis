export jobid='2012-07-09-8TeV-Higgs'
#rake fakerates
#rake fits
python WHPlotterEMT.py
python WHPlotterEET.py
python WHPlotterMMT.py
rake cards

export jobid='2012-07-09-7TeV-Higgs'
#rake fakerates
#rake fits
python WHPlotterEMT.py
python WHPlotterEET.py
python WHPlotterMMT.py
rake cards
