#!/bin/bash

for mass in `seq 111 119`
do
  interpolate_card.py hzz2l2t_110.txt 110 hzz2l2t_120.txt 120 $mass "zh_tt{mass}" "zh_ww{mass}" > hzz2l2t_$mass.txt
done

for mass in `seq 121 129`
do
  interpolate_card.py hzz2l2t_120.txt 120 hzz2l2t_130.txt 130 $mass "zh_tt{mass}" "zh_ww{mass}" > hzz2l2t_$mass.txt
done

for mass in `seq 131 139`
do
  interpolate_card.py hzz2l2t_130.txt 130 hzz2l2t_140.txt 140 $mass "zh_tt{mass}" "zh_ww{mass}" > hzz2l2t_$mass.txt
done

for mass in `seq 141 149`
do
  interpolate_card.py hzz2l2t_140.txt 140 hzz2l2t_150.txt 150 $mass "zh_tt{mass}" "zh_ww{mass}" > hzz2l2t_$mass.txt
done

for mass in `seq 151 159`
do
  interpolate_card.py hzz2l2t_150.txt 150 hzz2l2t_160.txt 160 $mass "zh_tt{mass}" "zh_ww{mass}" > hzz2l2t_$mass.txt
done
