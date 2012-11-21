#!/bin/bash

for i in `seq 110 10 160`
do
  echo $i
  compute_cls.sh hzz2l2t_$i.root myGrid$i.root $i > $i.cls.json
done
