# Central make file to run VH analysis
#
# Author: Evan K. Friis, UW Madison

# Common definitions of data samples, analyzer locations.
include Makefile.inc

# Building meta information about samples:
# This includes # of events, measured/effective integrated luminosity.

meta_data: 
	make -f Makefile.meta meta_data

# Rules for building ZH subchannels

# Z->mumu + X
zh_mmmt: 
	export channel=mmmt
	export ntuple_path=mmmt
	export analyzer=AnalyzeMMMT.py
	export leading_z_selector=zh_zmm_selection.py
	export primd=DoubleMu
	# Monitoring branches
	export branches=m1_m2_Mass m3_t_Mass
	make -f Makefile.zh histograms plots

zh_mmet: 
	export channel=mmet
	export ntuple_path=emmt
	export analyzer=AnalyzeMMET.py
	export leading_z_selector=zh_zmm_selection.py
	export primd=DoubleMu
	# Monitoring branches
	export branches=m1_m2_Mass e_t_Mass
	make -f Makefile.zh histograms plots events

zh_mmme: 
	export channel=mmme
	export ntuple_path=emmm
	export analyzer=AnalyzeMMME.py
	export leading_z_selector=zh_zmm_selection.py
	export primd=DoubleMu
	# Monitoring branches
	export branches=m1_m2_Mass e_m3_Mass
	make -f Makefile.zh histograms plots events

zh_mmtt: 
	export channel=mmtt
	export ntuple_path=mmtt
	export analyzer=AnalyzeMMTT.py
	export leading_z_selector=zh_zmm_selection.py
	export primd=DoubleMu
	# Monitoring branches
	export branches=m1_m2_Mass t1_t2_Mass
	make -f Makefile.zh histograms plots events

# Z->ee + X
zh_eemt: 
	export channel=eemt
	export ntuple_path=eemt
	export analyzer=AnalyzeEEMT.py
	export leading_z_selector=zh_zee_selection.py
	export primd=DoubleElectron
	# Monitoring branches
	export branches=e1_e2_Mass m_t_Mass
	make -f Makefile.zh histograms plots

zh_eeet: 
	export channel=eeet
	export ntuple_path=emmt
	export analyzer=AnalyzeEEET.py
	export leading_z_selector=zh_zee_selection.py
	export primd=DoubleElectron
	# Monitoring branches
	export branches=e1_e2_Mass e3_t_Mass
	make -f Makefile.zh histograms plots events

zh_eeem: 
	export channel=eeem
	export ntuple_path=eeem
	export analyzer=AnalyzeEEEM.py
	export leading_z_selector=zh_zee_selection.py
	export primd=DoubleElectron
	# Monitoring branches
	export branches=e1_e2_Mass e3_m_Mass
	make -f Makefile.zh histograms plots events

zh_eett: 
	export channel=eett
	export ntuple_path=mmtt
	export analyzer=AnalyzeEETT.py
	export leading_z_selector=zh_zee_selection.py
	export primd=DoubleElectron
	# Monitoring branches
	export branches=e1_e2_Mass t1_t2_Mass
	make -f Makefile.zh histograms plots events

# Do all ZH analysis
zh: zh_mmtt zh_mmet zh_mmme zh_mmmt zh_eett zh_eeet zh_eeem zh_eemt 

.PHONY: meta_data \
  zh \
  zh_mmtt zh_mmet zh_mmme zh_mmmt \
  zh_eett zh_eeet zh_eeem zh_eemt 
