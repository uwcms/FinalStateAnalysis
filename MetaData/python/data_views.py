'''

Tool for creating "views" of file containing histograms.

Applies MC normalization factors, styles, etc.

'''

import copy
from data_styles import data_styles
import logging
import os
import rootpy.io as io
from rootpy.plotting import views

log = logging.getLogger("data_views")

def extract_sample(filename):
    ''' Get sample name from a path

    >>> extract_sample('path/to/Zjets_M50.root')
    Zjets_M50
    '''
    sample = os.path.basename(filename)
    sample = sample.replace('.root', '').replace('.lumicalc.sum', '')
    return sample

def read_lumi(filename):
    ''' Read lumi stored in a file

    The lumi is stored as a single float value.
    '''
    with open(filename) as lumifile:
        return float(lumifile.readline().strip())

def data_views(files, lumifiles):
    ''' Builds views of files.

    [files] gives an iterator of .root files with histograms to build.

    [lumifiles] gives the correspond list of .lumisum files which contain
    the effective integrated luminosity of the samples.

    The lumi to normalize to is taken as the sum of the data file int. lumis.

    '''

    files = list(files)

    log.info("Creating views from %i files", len(files))

    # Map sample_name => root file
    histo_files = dict((extract_sample(x), io.open(x)) for x in files)

    # Map sample_name => lumi file
    lumi_files = dict((extract_sample(x), read_lumi(x)) for x in lumifiles)

    # Identify data files
    datafiles = set([name for name in histo_files.keys() if 'data' in name])

    log.info("Found the following data samples:")
    log.info(" ".join(datafiles))
    datalumi = sum(lumi_files[x] for x in datafiles)
    log.info("-> total int. lumi = %0.0fpb-1", datalumi)

    # Figure out the dataset for each file, and the int lumi.
    # Key = dataset name
    # Value = {intlumi, rootpy file, weight, weighted view}
    output = {}

    for sample in histo_files.keys():
        raw_file = histo_files[sample]
        intlumi = lumi_files[sample]
        log.debug("Building sample: %s => int lumi: %0.f pb-1", sample, intlumi)
        weight = datalumi/intlumi
        if 'data' in sample:
            weight = 1
        log.debug("Weight: %0.2f", weight)

        view = views.ScaleView(raw_file, weight)
        unweighted_view = raw_file

        # Add the style view
        style_dict = data_styles.get(sample, None)
        if style_dict:
            log.info("Found style for %s - applying Style View", sample)

            # Set style and title
            # title = the name of the sample, rootpy Legend uses this.
            nicename = copy.copy(style_dict['name'])
            view = views.TitleView(
                views.StyleView(view, **style_dict), nicename
            )
            unweighted_view = views.TitleView(
                views.StyleView(unweighted_view, **style_dict), nicename
            )

        output[sample] = {
            'intlumi': intlumi,
            'file' : raw_file,
            'weight' : weight,
            'view' : view,
            'unweighted_view' : unweighted_view
        }

    # Merge the data into just 'data'
    log.info("Merging data together")
    output['data'] = {
        'intlumi' : datalumi,
        'weight' : 1,
        'view' : views.SumView(*[output[x]['view'] for x in datafiles]),
        'unweighted_view' : views.SumView(*[output[x]['unweighted_view']
                                            for x in datafiles]),
    }

    return output
