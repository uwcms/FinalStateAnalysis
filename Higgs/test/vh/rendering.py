'''

Common stuff used in render scripts.

Builds the "views" of the different samples.

'''

from RecoLuminosity.LumiDB import argparse
import json
import logging
import rootpy.io as io
from rootpy.plotting import views
from rootpy.plotting import Canvas

from FinalStateAnalysis.MetaData.data_views import get_views

log = logging.getLogger("rendering")

def build_views(meta_filename, primds, files):
    meta_info = None
    log.info("Opening meta file: %s", meta_filename)
    with open(meta_filename) as meta_file:
        meta_info = json.load(meta_file)

    log.info("Building views")
    data_views = get_views(
        args.files,
        # How to get the sample from the file name
        lambda x: os.path.basename(x).replace('.root', ''),
        meta_info,
        4767,
    )

