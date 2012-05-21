export ZZFILE=evan_zz_ntuple.root
megaevents.py AnalyzeMMET.py $ZZFILE /emmt/final/Ntuple zz.evts.mmet final
megaevents.py AnalyzeMMMT.py $ZZFILE /mmmt/final/Ntuple zz.evts.mmmt final
megaevents.py AnalyzeMMTT.py $ZZFILE /mmtt/final/Ntuple zz.evts.mmtt final
megaevents.py AnalyzeMMME.py $ZZFILE /emmm/final/Ntuple zz.evts.mmme final

megaevents.py AnalyzeEEET.py $ZZFILE /eeet/final/Ntuple zz.evts.eeet final
megaevents.py AnalyzeEEMT.py $ZZFILE /eemt/final/Ntuple zz.evts.eemt final
megaevents.py AnalyzeEETT.py $ZZFILE /eett/final/Ntuple zz.evts.eett final
megaevents.py AnalyzeEEEM.py $ZZFILE /eeem/final/Ntuple zz.evts.eeem final

for file in `ls zz.evts.*`
do
  echo $file `cat $file | grep evt | wc -l`
done
