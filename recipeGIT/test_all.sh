#!/bin/bash

# Run all of the FinalStateAnalysis package unit tests

TESTDIR=$CMSSW_BASE/test/$SCRAM_ARCH

echo "Testing expression ntuple"
$TESTDIR/TestFinalStateAnalysisExpressionNtuple
echo "Testing utilities package"
$TESTDIR/TestFinalStateAnalysisUtilities
echo "Testing FinalState dataformat"
$TESTDIR/TestPATFinalState
echo "Testing Smart Trigger logic"
$TESTDIR/TestSmartTrigger
