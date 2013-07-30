#!/bin/bash

# Compute all the limits for the VH PAS

# How it works:
# ls -d limits/cmb ... produces a list of the limit configures/masses to
# compute.  i.e. limits/cmb/115, limits/cmb/120.
# This is piped to xargs, which takes each directory DIR 1 at a time (-n 1)
# and calls limit.py --no-repeat --asymptotic --noprefit --expectedOnly DIR
# which actually computes the limit.  The -P 10 option says to do 10 in
# parallel.  For a machine with fewer cores this should be reduced.
echo $@
INPUT_DIR=$1
NUMPROCS=$2
BLINDED=$3

#rm -f $INPUT_DIR/.limits_computed

if [[ $BLINDED == "YES" ]];
then
    echo "RUNNING BLIND"
    if ls -d $INPUT_DIR/[0-9]* | xargs -n 1 -P $NUMPROCS limit.py --asymptotic --expectedOnly # --no-prefit
    then touch $INPUT_DIR/.limits_computed
    else exit 1
    fi
else
    if ls -d $INPUT_DIR/[0-9]* | xargs -n 1 -P $NUMPROCS limit.py --asymptotic 
    then touch $INPUT_DIR/.limits_computed
    else exit 1
    fi
fi
exit 0
