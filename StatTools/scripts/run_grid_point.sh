#!/bin/bash
# 
# Condor submittable script to generate a CLs grid
# 
# Author: Evan K. Friis, UW Madison
# 
# Based on code by M. Bachtis

PrintUsage() {
  echo "USAGE: run_grid_point.sh [options] <input_card.root> <point> <output>"
  echo "  <input_card> corresponds to a workspace data card.  <point> is the"
  echo "  exclusion limit to probe."
  echo ""
  echo " NB: The random seed actually used for seed S, iter I, job J is:"
  echo "   seed = S + 1000*J + I"
  echo ""
  echo "OPTIONS:"
  echo " --toys=100             (number of toys to run)"
  echo " --iter=1               (number of times to run combine)"
  echo " --seed=1               (base random seed)"
  echo " --job=1                (jobID - will modify random seed)"
  echo " --mass=120             (mass to consider, for label only)"
  exit 0
}

logerror2() {
  echo 2>&1 "$@"
}

logerror() {
  echo 2>&1 "$@"
}
die() {
  if [ $# -gt 0 ]; then
    logerror
    logerror "$@"
  fi
  exit 1
}

OPTS=`getopt -o "h" -l "help,toys:,iter:,seed:,job:,mass:" -- "$@"`
if [ $? -ne 0 ]; then PrintUsage; fi

eval set -- "$OPTS"

TOYS=100
ITER=1
SEED=1
MASS=1

while [ ! -z "$1" ]
do
  case "$1" in
    -h) PrintUsage;;
    --help) PrintUsage;;
    --toys) shift; TOYS=$1;;
    --iter) shift; ITER=$1;;
    --seed) shift; SEED=$1;;
    --job) shift; JOB=$1;;
    --mass) shift; MASS=$1;;
        --) shift; break;;
    *) die "Unexpected option $1";;
  esac
  shift
done

WORKSPACE=$1
shift
POINT=$1
shift
OUTPUT=$1

# Make sure their are not any existing combine files in this working 
# directory.

EXISTING_FILES=`ls higgsCombineTest*.root 2> /dev/null | wc -l`
if [ "$EXISTING_FILES" != "0" ]; then
  logerror "There are already higgsCombineTest result files in this directory!"
  logerror "...exiting"
  exit 5
fi

if [ "$WORKSPACE" = "" ]; then
  die "You must provide a workspace file."
fi

if [ ! -f $WORKSPACE ]; then
  die "Workspace $WORKSPACE file does not exist!"
fi

if [ "$POINT" = "" ]; then
  die "You must provide an exclusion point to check."
fi

if [ "$OUTPUT" = "" ]; then
  die "You must provide an output file."
fi

OPTIONS="--freq --fork 0 --testStat LHC --clsAcc 0"

let BASESEED=(SEED + 10000*JOB - 10000)
COMBINE=${CMSSW_BASE}/bin/${SCRAM_ARCH}/combine

logerror2 "Running combine $ITER time(s) with seed: $SEED toys: $TOYS point: $POINT"
logerror2 " mass: $MASS"
logerror2 " - using the following options: $OPTIONS"

for iteration in `seq 1 $ITER`
do
  let FINALSEED=(BASESEED + iteration)
  logerror2 ""
  logerror2 "========================================================================"
  logerror2 "Doing iter=$iteration, with seed: $FINALSEED"
  logerror2 "========================================================================"
  $COMBINE $WORKSPACE -M HybridNew -s $FINALSEED --singlePoint $POINT \
    --fullBToys --saveToys --saveHybridResult -T $TOYS -m $MASS $OPTIONS
done

hadd $OUTPUT higgsCombine*.root 
rm higgsCombine*root
