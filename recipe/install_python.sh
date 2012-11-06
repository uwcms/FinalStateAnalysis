#!/bin/bash
# 
# This script sets up a python "virtualenv" [1], allowing us to install some 
# useful python modules.
# 
# Author: Evan K. Friis, UW Madison
# 
# Installed modules:
#   > yolk - tools for managing installed packages
#   > ipython - better interactive python
#   > termcolor - utility for coloring the consol
#   > uncertainties - awesome error propagation
#   > progressbar - cool progress bars
#   > cython - used for mixing C and python
#   > argparse - improved argument parsing
#   > rootpy - pythonic bindings for PyROOT 

export recipe=$CMSSW_BASE/src/FinalStateAnalysis/recipe
export vpython=$CMSSW_BASE/src/FinalStateAnalysis/recipe/external/vpython

cd $recipe/external/src/virtualenv

echo "Creating virtual python environment in $vpython"
if [ ! -d "$vpython" ]; then
  python virtualenv.py --distribute $vpython
else
  echo "...virtual environment already setup."
fi

echo "Activating virtual python environment"
cd $vpython
source bin/activate

echo "Installing yolk"
pip install -U yolk
echo "Installing ipython"
pip install -U ipython
echo "Installing termcolor"
pip install -U termcolor
echo "Installing uncertainties <-- awesome error propagation"
pip install -U uncertainties
echo "Install progressbar"
pip install -U progressbar
echo "Install cython"
pip install -U cython
echo "Installing argparse"
pip install -U argparse
echo "Installing pudb <-- interactive debugging"
pip install -U pudb

echo "Installing rootpy"
pip install -e $recipe/external/src/rootpy

