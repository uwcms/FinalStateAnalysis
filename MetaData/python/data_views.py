'''

Tool for creating "views" of file containing histograms.

Applies MC normalization factors, styles, etc.

'''

from datadefs import datadefs, data_name_map
from data_styles import data_styles
import logging
from rootpy.io import open
from rootpy.plotting import views

def data_views(files, normalize_to_dataset):
    ''' Builds views of files.

    <files> gives an iterator of file names to build.

    Each file must contain (in the base directory) two TTexts:

        TText("dataset", "[name of dataset"]),
        TText("intlumi", "[effective/real int. lumi of dataset"]),

    You must pass the name of a logical sample to normalize the data too.

    Example: "data_DoubleMu"

    '''
    log = logging.getLogger("data_views")
    # Figure out the dataset for each file, and the int lumi.
    # Key = dataset name
    # Value = {intlumi, rootpy file, file path}
    raw_samples = {}
    for file in files:
        log.info("Extracting meta data from file %s", file)
        raw_file = open(file, 'read')
        dataset_ttext = raw_file.Get("dataset")
        if not dataset_ttext:
            raise IOError(
                "Input file %s does not have required TText 'dataset'", file)
        dataset = dataset_ttext.GetTitle()
        log.info("=> dataset name: %s", dataset)
        intlumi_ttext = raw_file.Get("intlumi")
        if not intlumi_ttext:
            raise IOError(
                "Input file %s does not have required TText 'intlumi'", file)
        intlumi = float(intlumi_ttext.GetTitle())
        log.info("=> int lumi: %0.f pb-1", intlumi)
        raw_samples[dataset] = {
            'intlumi': intlumi,
            'file' : raw_file,
            'filename' : file
        }

    log.info("Determining total int lumi for sample %s", normalize_to_dataset)
    if not normalize_to_dataset in data_name_map:
        raise KeyError(
            "Normalization dataset %s is not a proper dataset "
            "defined in datadefs.py!" % normalize_to_dataset)
    subsamples = data_name_map[normalize_to_dataset]
    # Make sure we have all the subsamples
    target_int_lumi = 0
    for subsample in subsamples:
        if subsample not in raw_samples:
            raise KeyError(
                "Normalization dataset %s need subsample %s, "
                "but it isn't provided in the list of input files!" %
                (normalize_to_dataset, subsample))
        sub_int_lumi = raw_samples[subsample]['intlumi']
        log.info("Subsample %s has int lumi: %0.f pb-1",
                 subsample, sub_int_lumi)
        target_int_lumi += sub_int_lumi
    log.info("Target int lumi: %0.f pb-1", target_int_lumi)

    log.info("Scaling samples to integrated luminosity")
    for sample, sample_info in raw_samples.iteritems():
        weight = 1.0
        if 'data' in sample:
            log.info("Setting sample %s [DATA] weight to 1.0", sample)
        else:
            weight = target_int_lumi/sample_info['intlumi']
            log.info("Setting sample %s [MC] weight to %0.1f/%0.1f = %0.3g",
                     sample, target_int_lumi, sample_info['intlumi'], weight)
        sample_info['weight'] = weight
        log.info("Building weighted view")
        sample_info['view'] = views.ScaleView(sample_info['file'], weight)

    logical_samples = {}

    # Logical samples are combinations of several subsamples
    log.info("Building logical samples")
    for name, subsamples in data_name_map.iteritems():
        # Check sure we have all the dependent samples
        if not all(subsample in raw_samples for subsample in subsamples):
            log.debug("Skipping logical sample %s, we don't have all it's"
                      " dependencies" % name)
            continue
        # Make a sum view of all the sub samples
        log.info("Constructing logical sample %s from %i subsamples",
                 name, len(subsamples))
        sumview = views.SumView(
            *[raw_samples[subsample]['view'] for subsample in subsamples])
        unweighted_view = views.SumView(
            *[raw_samples[subsample]['file'] for subsample in subsamples])
        style_dict = data_styles.get(name, None)
        if style_dict:
            log.info("Found style for %s - applying Style View", name)
            sumview = views.StyleView(sumview, **style_dict)
            unweighted_view = views.StyleView(unweighted_view, **style_dict)
        else:
            log.warning("Didn't find a style for logical sample %s", name)

        logical_samples[name] = {
            'view' : sumview,
            'unweighted_view' : unweighted_view,
            'subsamples' : dict(
                (subsample, raw_samples[subsample])
                for subsample in subsamples
            )
        }
    return logical_samples
