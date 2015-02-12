#!/bin/env python
import sys, os, subprocess
import json
from FinalStateAnalysis.MetaData.datadefs import datadefs

def getUserHDFSlisting ( username ) :
  cmd = ['hdfs dfs']
  cmd.append('-ls -R')
  cmd.append('/store/user/'+username)
  cmd.append('2>/dev/null')
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
  usernames = sys.argv[1].split(',')
  store_user = []
  user_pat_configs = []
  for username in usernames :
    print "Loading HDFS listing for %s" % username
    store_user.extend(getUserHDFSlisting(username))
    print "Finding FSA PAT-tuplizer configs for %s" % username
    user_pat_configs.extend(findUserPatConfigJsonFiles(username))

  pat_datadefs = {}
  for name, datadef in datadefs.iteritems() :
    if 'datasetpath' in datadef :
      locations = []
      for dir in store_user :
        if datadef['datasetpath'] in dir :
          loc = {}
          loc['dir'] = '/hdfs'+dir
          for config in user_pat_configs :
            if config['PAT Location'] == loc['dir'] :
              loc['possible PAT config'] = config
          locations.append(loc)
      if len(locations) != 0 :
        pat_datadefs[name] = {}
        pat_datadefs[name]['locations'] = locations
        pat_datadefs[name]['datadef'] = datadef

  print json.dumps(pat_datadefs, indent=4, separators=(',',': '))
  # with open(os.path.expanduser('~/public_html/pat_datadefs.min.json'), 'w') as output :
  #   json.dump(pat_datadefs, output)
