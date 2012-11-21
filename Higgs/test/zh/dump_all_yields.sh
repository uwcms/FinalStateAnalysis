#!/bin/bash

echo "MMMT"

./dump_zh_yields.py data_DoubleMu mu tau results/analysis/mmmt/data*root

echo "MMET"

./dump_zh_yields.py data_DoubleMu e tau results/analysis/mmet/data*root

echo "MMME"

./dump_zh_yields.py data_DoubleMu mu e results/analysis/mmme/data*root

echo "MMTT"

./dump_zh_yields.py data_DoubleMu t1 t2 results/analysis/mmtt/data*root

echo "EEMT"

./dump_zh_yields.py data_DoubleElectron mu tau results/analysis/eemt/data*root

echo "EEET"

./dump_zh_yields.py data_DoubleElectron e tau results/analysis/eeet/data*root

echo "EEEM"

./dump_zh_yields.py data_DoubleElectron mu e results/analysis/eeem/data*root

echo "EETT"

./dump_zh_yields.py data_DoubleElectron t1 t2 results/analysis/eett/data*root
