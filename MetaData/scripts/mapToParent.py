#!/usr/bin/python

'''
File: mapToParent.py
Author: Ian Ross (iross@cern.ch), University of Wisconsin Madison
Description: Reads the xml output from jobs and maps patTuples -> parent data files. Results get dumped in a JSON file
'''

import glob
import sys
import os
import json

from jobReportSummary import parse_job_reports,group_by_run,collapse_ranges_in_list

from itertools import chain

try:
    import RecoLuminosity.LumiDB.argparse as argparse
except:
    argparse = None

def json_summary(run_lumi_set, indent=2):
    '''
    Compute a crab -report like json summary for a set of runs and lumis.
    Example:
    >>> run_lumis = [(100, 2), (100, 1), (150, 1), (150, 2), (150, 8)]
    >>> # Disable indentation
    >>> json_summary(run_lumis, None)
    '{"100": [[1, 2]], "150": [[1, 2], [8, 8]]}'
    '''
    run_lumis = sorted(run_lumi_set)
    output = {}
    if not run_lumis:
        return output
    for run, lumis_in_run in group_by_run(run_lumis):
        output[str(run)] = list(collapse_ranges_in_list(lumis_in_run))
    return output

def filterInputs(lIn,substr="root://cmsxrootd.hep.wisc.edu/"):
    """Remove substring from all members of a list of strings"""
    temp=[]
    for i in lIn:
        temp.append(i.replace(substr,""))        
    return temp

def convertToJSON(map,dumpLumis,jsonOut):
    """Takes a library of outputFile={parsed:results}, craps out a JSON with interesting info """
    minimap={} #smaller map for easier reading
    for it in map:
        lumis= json_summary(map[it]['input_run_lumis'],4)
#        minimap[it]={'input_files' : filterInputs(map[it]['input_files'],"root://cmsxrootd.hep.wisc.edu/")} #todo: make sure this is the right cleaning address...
        minimap[it]={'input_files' : map[it]['input_files']} 
        if dumpLumis:
            minimap[it]['output_run_lumis']=json_summary(map[it]['output_run_lumis'])
    with open(jsonOut,'wb') as out:
        json.dump(minimap, out, sort_keys=True, indent=4)
    pass


def main():
    if argparse is None:
        sys.stderr.write("Try harder.\n"
                "Couldn't figure out how to parse args... Try a cmsenv.")

    parser = argparse.ArgumentParser(description='%prog -- scan run output and map pattuples to parent data files')
    parser.add_argument("--dir",dest="dir",type=str,default="")
    parser.add_argument("--output",dest="output",type=str,default="patMap.json",required=True)
    parser.add_argument("--storeLumis",dest="lumis",action="store_true",default=False,required=False)
    args = parser.parse_args()

    xmls = []
    dir=args.dir
    dumpLumis=False
    if args.lumis:
        dumpLumis=True

    map={}
    files = chain(*[glob.glob(dir+'/submit/*/*.xml')]) #what is this magic?
#    files = chain(*[glob.glob(dir+'*.xml')]) #what is this magic?
    for it in files:
        try:
            output = parse_job_reports([it])
            if not output['ok']:
                continue
            map[output['output_files'][0]]=output #why is output_files saved as a list?
        except IndexError:
            continue
    convertToJSON(map,dumpLumis,args.output)

if __name__ == '__main__':
    try:
        ret = main()
    except KeyboardInterrupt:
        ret = None
    sys.exit(ret)
