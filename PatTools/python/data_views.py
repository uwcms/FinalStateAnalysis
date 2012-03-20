'''

Tool for creating "views" of file containing histograms.

Applies MC normalization factors, styles, etc.

'''

from datadefs import datadefs, data_name_map
import logging
from rootpy.io import open
from rootpy.plotting import views

log = logging.getLogger("get_views")

def get_views(files, sample_extractor, evt_counter, target_lumi):
    ''' Builds views of files

    <sample_extractor>: a function which returns the sample name
                        from the file name.

    <evt_counter>:      a dictionary which maps sample name to number of
                        processed events.
                        Should have the following form:
                            evt_counter[sample]['n_evts']

    <target_lumi>:      desired expected integrated luminosity for MC samples.

    the sample name from the filenames
    '''

    log.info("Making views for %i files", len(files))

    # A "raw" sample corresponds to a key in datadefs.  These may have nicer,
    # "proper" names, provided by the data_name_map.  A "proper" sample can
    # contain several raw sample.
    # For example, WWW includes ['WWWTo2Lplus', 'WWWTo2Lminus']
    raw_sample_infos = {}

    for file in files:
        sample = sample_extractor(file)
        if sample in raw_sample_infos:
            raise KeyError("Sample %s appears more than once!" % sample)

        log.debug("Extracted samples %s from file %s", sample, file)
        n_events = evt_counter[sample]['n_evts']
        log.debug("NumEvents = %i", n_events)
        weight = 1.0
        eff_lumi = -1
        if 'data' not in sample:
            xsec = datadefs[sample]['x_sec']
            log.debug("xsec = %f", xsec)
            log.debug("target_lumi = %f", target_lumi)
            eff_lumi = n_events/xsec
            log.debug("eff. int. lumi. = %f", eff_lumi)
            weight = target_lumi/eff_lumi
        log.debug("weight = %f", weight)

        # Build weighted view
        raw_file = open(file, 'read')
        view = raw_file
        # Check if we need to apply a weight
        if weight != 1.:
            view = views.ScaleView(raw_file, weight)

        raw_sample_infos[sample] = {
            'filename' : file,
            'file' : raw_file,
            'nevts' : n_events,
            'weight' : weight,
            'eff_lumi' : eff_lumi,
            'view' : view,
        }

    proper_sample_infos = {}

    # Now build the composite samples
    for name, subsamples in data_name_map.iteritems():
        # Check sure we have all the dependent samples
        if not all(subsample in raw_sample_infos for subsample in subsamples):
            log.debug("Skipping proper sample %s, we don't have all it's"
                      " dependencies" % name)
            continue
        # Make a sum view of all the sub samples
        log.info("Constructing sum view from %i subsamples" % len(subsamples))
        sumview = views.SumView(
            *[raw_sample_infos[subsample]['view'] for subsample in subsamples])
        unweighted_view = views.SumView(
            *[raw_sample_infos[subsample]['file'] for subsample in subsamples])
        # TODO try and find a style
        log.warning("need to apply style")
        proper_sample_infos[name] = {
            'view' : sumview,
            'unweighted_view' : unweighted_view,
            'subsamples' : dict(
                (subsample, raw_sample_infos[subsample])
                for subsample in subsamples
            )
        }

    return proper_sample_infos
