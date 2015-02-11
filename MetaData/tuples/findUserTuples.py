from FinalStateAnalysis.MetaData.datadefs import datadefs
import subprocess

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

store_user = getUserHDFSlisting('nsmith')
json_lines = []
for name, datadef in datadefs.iteritems() :
  if 'datasetpath' in datadef :
    for dir in store_user :
      if datadef['datasetpath'] in dir :
        json_lines.append('    "%s" : "%s"' % (name, '/hdfs'+dir) )

print ",\n".join(json_lines)
