export jobid=2012-07-23-7TeV-Higgs
export afile=`find $s/data/$jobid | grep root | head -n 1`

rake "make_wrapper[$afile, eet/final/Ntuple, EETauTree]"
rake "make_wrapper[$afile, emt/final/Ntuple, EMuTauTree]"
rake "make_wrapper[$afile, mmt/final/Ntuple, MuMuTauTree]"
rake "make_wrapper[$afile, mmm/final/Ntuple, MuMuMuTree]"
rake "make_wrapper[$afile, mm/final/Ntuple, MuMuTree]"
rake "make_wrapper[$afile, em/final/Ntuple, EMuTree]"
rake "make_wrapper[$afile, ee/final/Ntuple, EETree]"

ls *pyx | sed "s|pyx|so|" | xargs rake 


rake "meta:getinputs[$jobid, $s/data]"
rake "meta:getmeta[inputs/$jobid, mm/metaInfo, 7]"

export jobid=2012-07-23-8TeV-Higgs
rake "meta:getinputs[$jobid, $s/data]"
rake "meta:getmeta[inputs/$jobid, mm/metaInfo, 8]"
