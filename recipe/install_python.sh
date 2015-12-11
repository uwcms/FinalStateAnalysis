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
#   > pytables - provides hdf5 support
#   > jupyter - contains ipython notebook modules

export recipe=$CMSSW_BASE/src/FinalStateAnalysis/recipe
export vpython=$CMSSW_BASE/src/FinalStateAnalysis/recipe/external/vpython
export hdf5=$CMSSW_BASE/src/FinalStateAnalysis/recipe/external/hdf5

cd $recipe/external/src/virtualenv

echo "Creating virtual python environment in $vpython"
if [ ! -d "$vpython" ]; then
  python virtualenv.py $vpython
else
  echo "...virtual environment already setup."
fi

echo "Activating virtual python environment"
cd $vpython
source bin/activate

echo "Updating pip to latest version"
pip install -U pip

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
if ! python -c 'import argparse' 2>/dev/null; then
    echo "Installing argparse"
    pip install -U argparse
fi
echo "Installing pudb <-- interactive debugging"
pip install -U pudb
echo "Installing yellowhiggs <-- higgs yellow report x-sections lookup table"
pip install -U yellowhiggs
echo "Installing jupyter (for ipython notebooks)"
pip install -U jupyter

echo "Installing rootpy and necessary peripherals"
# have to mess with things a little to install rootpy
# pyzmq is required to use rootpy in ipython
pip install pyzmq --install-option="--zmq=bundled"

pip install -e $recipe/external/src/rootpy

if [ "$PYTABLES" = "1" ]
then
    echo "Installing PyTables"
    cd $CMSSW_BASE/src/FinalStateAnalysis/recipe/external
    if [ ! -d "hdf5-1.8.11" ]
    then
        echo "Downloading HDF5"
        wget http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8.11/src/hdf5-1.8.11.tar.gz
        tar xvzf hdf5-1.8.11.tar.gz
        cd hdf5-1.8.11
        ./configure --prefix=$hdf5
        cd ..
    fi
    cd hdf5-1.8.11
    echo "Installing HDF5"
    make -j 2
    make install
    cd ..
    export HDF5_DIR=$hdf5
    pip install -U numexpr
    pip install -U tables

    echo "Run: source environment.sh"
fi
