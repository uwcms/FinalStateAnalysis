# Central make file to run VH analysis
#
# Author: Evan K. Friis, UW Madison

# Common definitions of data samples, analyzer locations.
include Makefile.inc

# Building meta information about samples:
# This includes # of events, measured/effective integrated luminosity.

meta_data: 
	make -f Makefile.meta meta_data

targets = histograms plots events

# Rules for building ZH subchannels

# Z->mumu + X
zh_mmmt: 
	make -f Makefile.zh \
	  channel=mmmt \
	  ntuple_path=mmmt \
	  analyzer=AnalyzeMMMT.py \
	  leading_z_selector=zh_zmm_selection.py \
	  primd=DoubleMu \
	  l1name=mu \
	  l2name=tau \
	  branches="m1_m2_Mass m3_t_Mass" \
	  $(targets)

zh_mmet: 
	make -f Makefile.zh \
	  channel=mmet \
	  ntuple_path=emmt \
	  analyzer=AnalyzeMMET.py \
	  leading_z_selector=zh_zmm_selection.py \
	  primd=DoubleMu \
	  l1name=e \
	  l2name=tau \
	  branches="m1_m2_Mass e_t_Mass" \
	  $(targets)

zh_mmme: 
	make -f Makefile.zh \
	  channel=mmme \
	  ntuple_path=emmm \
	  analyzer=AnalyzeMMME.py \
	  leading_z_selector=zh_zmm_selection.py \
	  primd=DoubleMu \
	  l1name=mu \
	  l2name=e \
	  branches="m1_m2_Mass e_m3_Mass" \
	  $(targets)

zh_mmtt: 
	make -f Makefile.zh \
	  channel=mmtt \
	  ntuple_path=mmtt \
	  analyzer=AnalyzeMMTT.py \
	  leading_z_selector=zh_zmm_selection.py \
	  primd=DoubleMu \
	  l1name=t1 \
	  l2name=t2 \
	  branches="m1_m2_Mass t1_t2_Mass" \
	  $(targets)

# Z->ee + X
zh_eemt: 
	make -f Makefile.zh \
	  channel=eemt \
	  ntuple_path=eemt \
	  analyzer=AnalyzeEEMT.py \
	  leading_z_selector=zh_zee_selection.py \
	  primd=DoubleElectron \
	  l1name=mu \
	  l2name=tau \
	  branches="e1_e2_Mass m_t_Mass" \
	  $(targets)

zh_eeet: 
	make -f Makefile.zh \
	  channel=eeet \
	  ntuple_path=eeet \
	  analyzer=AnalyzeEEET.py \
	  leading_z_selector=zh_zee_selection.py \
	  primd=DoubleElectron \
	  l1name=e \
	  l2name=tau \
	  branches="e1_e2_Mass e3_t_Mass" \
	  $(targets)

zh_eeem: 
	make -f Makefile.zh \
	  channel=eeem \
	  ntuple_path=eeem \
	  analyzer=AnalyzeEEEM.py \
	  leading_z_selector=zh_zee_selection.py \
	  primd=DoubleElectron \
	  l1name=mu \
	  l2name=e \
	  branches="e1_e2_Mass e3_m_Mass" \
	  $(targets)

zh_eett: 
	make -f Makefile.zh \
	  channel=eett \
	  ntuple_path=eett \
	  analyzer=AnalyzeEETT.py \
	  leading_z_selector=zh_zee_selection.py \
	  primd=DoubleElectron \
	  l1name=t1 \
	  l2name=t2 \
	  branches="e1_e2_Mass t1_t2_Mass" \
	  $(targets)

# Do all ZH analysis
zh: zh_mmtt zh_mmet zh_mmme zh_mmmt zh_eett zh_eeet zh_eeem zh_eemt 

results/analysis/zh_yields.txt: zh print_zh.py
	./print_zh.py results/analysis/*/zjet_bkgs.json > $@


.PHONY: meta_data \
  zh \
  zh_mmtt zh_mmet zh_mmme zh_mmmt \
  zh_eett zh_eeet zh_eeem zh_eemt 
