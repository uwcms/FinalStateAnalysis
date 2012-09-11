#!/bin/bash
cmsenv

export recipe=$CMSSW_BASE/src/FinalStateAnalysis/recipe
export vpython=$CMSSW_BASE/src/FinalStateAnalysis/recipe/external/vpython

cd $recipe/external/src/virtualenv

echo "Creating virtual python environment in $vpython"
python virtualenv.py --distribute $vpython

echo "Activating virtual python environment"
cd $vpython
source bin/activate

echo "Installing rootpy"
pip install git+https://github.com/uwcms/rootpy.git
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

