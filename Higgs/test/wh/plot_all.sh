export jobid='2012-07-12-8TeV-Higgs'
#rake fakerates
#rake fits
python WHPlotterEMT.py
python WHPlotterEET.py
python WHPlotterMMT.py
rake cards
rake copycards

export jobid='2012-07-09-7TeV-Higgs'
#rake fakerates
#rake fits
python WHPlotterEMT.py
python WHPlotterEET.py
python WHPlotterMMT.py
rake cards
rake copycards
