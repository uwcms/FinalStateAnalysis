from RecoLuminosity.LumiDB import argparse

import logging
import uncertainties
import sys

# Steal the args so ROOT doesn't mess them up!
args = sys.argv[:]
sys.argv = [sys.argv[0]]

import rootpy.io as io
from rootpy.plotting import views
from rootpy.plotting import Canvas, Legend

from FinalStateAnalysis.MetaData.data_views import data_views

if __name__ == "__main__":

    log = logging.getLogger("render_zh_plots")
    view_builder = logging.getLogger("data_views")
    view_builder.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument('output', help='Output directory')
    parser.add_argument('pd', help='Primary dataset')
    parser.add_argument('l1name', help='Name of first lepton')
    parser.add_argument('l2name', help='Name of first lepton')
    parser.add_argument('bkgs', help='Background est. file')
    parser.add_argument('files', metavar='file',
                        nargs='+', help = 'Histogram files')
    args = parser.parse_args(args[1:])

    log.info("Building views")
    histogram_views = data_views(args.files,args.pd)

    def region_directory(base_view, is_os, passed1, passed2):
        ''' Get the directory given the configuration '''
        directory = "_".join([
            "os" if is_os else "ss",
            args.l1name,
            "pass" if passed1 else "fail",
            args.l2name,
            "pass" if passed2 else "fail",
        ])
        return views.SubdirectoryView(base_view, directory)

    plots_to_make = [
        'z1Mass'
    ]

    for plot_to_make in plots_to_make:
        signal_region = region_directory(



