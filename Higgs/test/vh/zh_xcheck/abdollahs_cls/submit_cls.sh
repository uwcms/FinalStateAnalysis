#!/bin/bash

for i in `seq 110 10 160`
do
  echo $i
  make_grid_submission.py -i hzz2l2t_$i.root -submit $s/abdollah_cls/$i -min 0.5 -max 50  -mass $i
done
