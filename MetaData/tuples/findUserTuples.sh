#!/bin/bash

if [[ ! $# == 2 ]];
then
  echo "Usage: ${0} user campaign"
  exit
fi
user=$1
campaign=$2
hdfs dfs -ls -R /store/user/${user} |grep "${campaign}$"|sed "s:.*/store/user/${user}/\(.*\)/\(.*/AODSIM/.*\):    '\1' \: '/store/user/${user}/\1/\2':"
