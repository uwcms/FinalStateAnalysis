#!/bin/bash

# Nuke PatTools from orbit.
# 
# This allow a cleaner, slimmer working area without all the PAT dependencies
# checked out.
#
# This script removes the entire PatTools directory, and makes sure that 
# git doesn't complain about the removal.
#
# If you pull changes to PatTools from a remote, you'll need to rerun the
# script.
#
# Author: Evan K. Friis, UW Madison


# Can suppress interactive confirmation by setting FORCENUKE=1
if [ -z "$FORCENUKE" ]; then
   while true; do
       read -p "Do you wish nuke PatTools from orbit? " yn
       case $yn in
           [Yy]* ) echo "sounds good dude"; break;;
           [Nn]* ) exit 2;;
           * ) echo "Please answer yes or no.";;
       esac
   done
fi

echo "Deleting all files in PatTools..."
rm -rf $fsa/PatTools 

echo "Telling git to ignore changes in them..."
git ls-files $fsa/PatTools | xargs -n 1 git update-index --assume-unchanged 

echo "done."
