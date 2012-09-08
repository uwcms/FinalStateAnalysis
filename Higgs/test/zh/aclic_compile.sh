#!/bin/bash

# Compile a library using ACliC
# Usage: 
#   aclic_compile.sh mylib.C

tmpfile=/tmp/aclic_compile_$$.C

echo "Generating stupid macro in $tmpfile"
cat > $tmpfile << EOF
{
  gROOT->ProcessLine(".L $1++");
}
EOF

echo "Compiling macro"
root -l -b -q $tmpfile

rm $tmpfile
