echo "Checking out rootpy library"

cd $CMSSW_BASE/src/FinalStateAnalysis/recipe/external/src/
git clone git@github.com:ekfriis/rootpy.git
cd rootpy
git remote add upstream https://github.com/ndawe/rootpy.git
