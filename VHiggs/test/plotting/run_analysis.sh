#!/bin/bash

python analysis.py
while [ $? -ne 0 ]; do
   python analysis.py
done
