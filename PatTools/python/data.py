'''

Tool for building TFileCollections corresponding to processed data samples.

The TFileCollection is a caching, transparent interface to a collection of
ROOT files which hold histograms and TTrees.

The main function in this module is build_data(...)

The required arguments are:
    * analysis (to determine which samples are applicable)
    * jobid (i.e. 2011-10-25-WHReskim)
    * source (an environment variable which stores where ROOT files are)
    * target_lumi
    * skips - a list of substrings to filter out input files.
       If a one of the skip strings is a substring of a subsample, it will be
       skipped.
    * count - path to a histogram which counts the number of originally
              processed events.

'''
import os
import glob
import logging

import FinalStateAnalysis.PatTools.datadefs as datadefs

import FinalStateAnalysis.Utilities.WeightedTFile as WeightedTFile
import FinalStateAnalysis.Utilities.TFileCollection as TFileCollection
import FinalStateAnalysis.Utilities.AnalysisPlotter as AnalysisPlotter

log = logging.getLogger("data_construction")

def skip_sample(sample, skips):
    return any((x in sample) for x in skips)

def get_result_dir(jobid, source, sample):
    result_dir = "-".join([jobid, sample, 'analyze*'])
    return os.path.join(os.environ[source], result_dir, '*', '*.root')

def build_data(analysis, jobid, source, target_lumi,
               skips, count='emt/skimCounter', unweighted=False):
    raw_samples = {}
    # Build the basic weighted files
    for name, info in datadefs.datadefs.iteritems():
        if analysis not in info['analyses']:
            continue
        log.info("Building sample %s", name)

        if skip_sample(name, skips):
            continue
        if not glob.glob(get_result_dir(jobid, source, name)):
            log.warning("No files - skipping sample %s!", name)
            continue

        collection = TFileCollection.TFileCollection(
            get_result_dir(jobid, source, name))

        weightfile_args = { 'weight' : 1.0,}
        # For MC, we apply weight.
        if not unweighted and 'x_sec' in info:
            weightfile_args = {
                'target_lumi' : target_lumi,
                'xsec' : info['x_sec'],
                'skim_eff' : 1.0,
                'event_count' : count,
                'verbose' : True
            }

        wfile = WeightedTFile.WeightedTFile(collection, **weightfile_args)
        sample = AnalysisPlotter.AnalysisSample(wfile, name)
        # Now apply the weight
        raw_samples[name] = {
            'file' : wfile,
            'sample' : sample
        }

    samples = {}

    # Build the composite files
    for name, subsample_names in datadefs.data_name_map.iteritems():
        valid_subsamples = [
            x for x in subsample_names if not skip_sample(x, skips)]
        if not valid_subsamples:
            continue
        #print subsample_names
        if analysis not in datadefs.datadefs[valid_subsamples[0]]['analyses']:
            continue
        subsamples = [raw_samples[x]['sample'] for x in valid_subsamples]

        samples[name] = AnalysisPlotter.AnalysisMultiSample(name, *subsamples)

    plotter = AnalysisPlotter.AnalysisPlotter(*samples.values())

    return samples, plotter
