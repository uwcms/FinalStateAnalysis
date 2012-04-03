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

from FinalStateAnalysis.MetaData.data_views import data_views

log = logging.getLogger("rendering")

