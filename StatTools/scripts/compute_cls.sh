#!/bin/bash

# Compute the CLs limits (expected and observed) given the model.
# Outputs a json file giving the expected band and the observed.
# Usage: compute_cls.sh [card_file] [grid_file] [mass]

UNIQ="CLSCOMPUTER${RANDOM}UNIQ"

echo "{"

echo -n '  "mass": '
echo "$3,"
echo '  "method": "cls",'
echo -n '  "+2": '
combine $1 -M HybridNew --freq  --testStat LHC \
  -n $UNIQ \
  --grid=$2 -m $3  --expectedFromGrid=0.975 | \
  grep -e "^Limit: r < " | tail -n 1 | cut -d " " -f4 | sed "s|$|,|"

echo -n '  "+1": '
combine $1 -M HybridNew --freq  --testStat LHC \
  -n $UNIQ \
  --grid=$2 -m $3  --expectedFromGrid=0.84 | \
  grep -e "^Limit: r < " | tail -n 1 | cut -d " " -f4 | sed "s|$|,|"

echo -n '  "exp": '
combine $1 -M HybridNew --freq  --testStat LHC \
  -n $UNIQ \
  --grid=$2 -m $3 --expectedFromGrid=0.5 | \
  grep -e "^Limit: r < " | tail -n 1 | cut -d " " -f4 | sed "s|$|,|"

echo -n '  "obs": '
combine $1 -M HybridNew --freq  --testStat LHC \
  -n $UNIQ \
  --grid=$2 -m $3 | \
  grep -e "^Limit: r < " | tail -n 1 | cut -d " " -f4 | sed "s|$|,|"

echo -n '  "-1": '
combine $1 -M HybridNew --freq  --testStat LHC \
  -n $UNIQ \
  --grid=$2 -m $3  --expectedFromGrid=0.16 | \
  grep -e "^Limit: r < " | tail -n 1 | cut -d " " -f4 | sed "s|$|,|"

echo -n '  "-2": '
combine $1 -M HybridNew --freq  --testStat LHC \
  -n $UNIQ \
  --grid=$2 -m $3  --expectedFromGrid=0.0275 | \
  grep -e "^Limit: r < " | tail -n 1 | cut -d " " -f4 | sed "s|$||"
echo "}"

rm higgsCombine${UNIQ}*root
