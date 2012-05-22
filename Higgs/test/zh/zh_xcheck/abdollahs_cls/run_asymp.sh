#!/bin/bash

for i in `seq 110 10 160`
do
  echo $i
  combine -M Asymptotic -H ProfileLikelihood hzz2l2t_$i.root | limit2JSON.py --mass $i > $i.json
done
