import FinalStateAnalysis.Utilities.WeightedTFile as WeightedTFile
import FinalStateAnalysis.Utilities.TFileCollection as TFileCollection
import FinalStateAnalysis.Utilities.AnalysisPlotter as AnalysisPlotter
import FinalStateAnalysis.PatTools.datadefs as datadefs
import os
import glob
import logging

log = logging.getLogger("data_construction")

def skip_sample(sample, skips):
    return any((x in sample) for x in skips)

def get_result_dir(jobid, source, sample):
    #jobid =
    #result_dir = "-".join([jobid, sample, 'analyzeFinalStates'])
    result_dir = "-".join([jobid, sample, 'analyze*'])
    return os.path.join(os.environ[source], result_dir, '*', '*.root')

def build_data(jobid, source, target_lumi, skips):
    raw_samples = {}
    # Build the basic weighted files
    for name, info in datadefs.datadefs.iteritems():
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
        if 'x_sec' in info:
            weightfile_args = {
                'target_lumi' : target_lumi,
                'xsec' : info['x_sec'],
                'skim_eff' : 1.0,
                'event_count' : 'eee/skimCounter',
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
        #print subsample_names
        subsamples = [raw_samples[x]['sample'] for x in subsample_names
                      if not skip_sample(x, skips)]
        if not subsamples:
            continue
        samples[name] = AnalysisPlotter.AnalysisMultiSample(name, *subsamples)

    plotter = AnalysisPlotter.AnalysisPlotter(*samples.values())

    return samples, plotter
