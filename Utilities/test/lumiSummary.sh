#!/usr/bin/env bash


for file in $*
do
  RUN=`echo $file | sed "s|runs/||" | sed "s|.csv||"`
  INSTLUMI=`cat $file | averageLuminosity.py`
  echo "$RUN : $INSTLUMI"
done

