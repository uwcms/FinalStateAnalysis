#!/bin/env python
import sys
import subprocess
import json
from FinalStateAnalysis.MetaData.datadefs import datadefs

def getUserHDFSlisting ( username ) :
  cmd = ['hdfs dfs']
  cmd.append('-ls -R')
  cmd.append('/store/user/'+username)
  listing = subprocess.Popen(" ".join(cmd), shell=True, stdout=subprocess.PIPE).stdout.read()
  files = [l.split() for l in listing.split('\n')]
  dirs = [file[-1] for file in files if len(file) > 0 and file[0][0] == 'd']
  # keep only deepest level directories
  dir_subset = []
  for i in range(0, len(dirs)-1) :
    if not dirs[i] in dirs[i+1] :
      dir_subset.append(dirs[i])
  return dir_subset

def findUserPatConfigJsonFiles ( username ) :
  user_pat_configs = []
  with subprocess.Popen("./scrape_pat_config.sh "+username, shell=True, stdout=subprocess.PIPE).stdout as user_pat_configs_filelist :
    for file in user_pat_configs_filelist :
      fn = file.strip()
      # dict is wrapped by hash but hash is in dict...
      wrapped_dict = json.load(open(fn, 'r'))
      if len(wrapped_dict.keys()) > 0 :
        dict = wrapped_dict[wrapped_dict.keys()[0]]
        dict['source'] = fn
        user_pat_configs.append(dict)
  return user_pat_configs

if __name__ == "__main__" :
  username = sys.argv[1]
  store_user = getUserHDFSlisting(username)
  user_pat_configs = findUserPatConfigJsonFiles(username)

  pat_locations = {}
  for name, datadef in datadefs.iteritems() :
    pat_locations[name] = []
    if 'datasetpath' in datadef :
      for dir in store_user :
        if datadef['datasetpath'] in dir :
          loc = {}
          loc['dir'] = '/hdfs'+dir
          for config in user_pat_configs :
            if config['PAT Location'] == loc['dir'] :
              loc['possible PAT config'] = config
          pat_locations[name].append(loc)
    if len(pat_locations[name]) == 0 :
      pat_locations.pop(name)

  print json.dumps(pat_locations, indent=4, separators=(',',': '))
