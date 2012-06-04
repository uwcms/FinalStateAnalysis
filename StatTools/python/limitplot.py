'''

Library for producing "Brazilian flag plots."

The library uses json files for exchanging limit information.

You pass it a bunch of json files.  The json files should all have
a <method> item (asymp/cls/etc), and a <mass> point. Observed and
expected can be in separate files. <label> can also optionally be used.

The library groups together the different information from all the files.

Author: Evan K. Friis, UW Madison

'''

import copy
from FinalStateAnalysis.Utilities.graphsmoother import \
        smooth_graph as smoother
import json
import ROOT

def get_limit_info(json_files):
    ''' Extract all information from a set of json files

    The output format is:
    {
        (<method1>, <label1>) : {
            <mass1> : {
                'exp' : XX.X,
                'obs' : XX.X,
                '-1' : XX.X
                etc
            },
            <mass2> : ...
        },
        <method2> : {
        }
    }
    '''
    result = {}
    for file in json_files:
        with open(file) as json_file:
            try:
                file_result = json.load(json_file)
            except:
                print "Can't parse file:", file
                raise
            key = (file_result['method'], file_result.get('label', ''))
            key_result = result.setdefault(key, {})
            mass = file_result['mass']
            mass_result = key_result.setdefault(mass, {})
            # Check what data we have
            for key in ['-1', '-2', 'exp', 'obs', '+1', '+2']:
                if key in file_result:
                    mass_result[key] = file_result[key]
    return result

def build_expected_band(result, key, smooth=-1):
    ''' Build a set of TGraphs giving the "brazilian flag",

    given a <key> into result (i.e. (<method1>, <label1>) above)
    '''
    try:
        mass_points = sorted(result[key].keys())
    except KeyErrror:
        print "Couldn't find key: %s" % key
        print "Available keys: %s" % result.keys()
        raise
    exp = ROOT.TGraphAsymmErrors(len(mass_points))
    onesig = ROOT.TGraphAsymmErrors(len(mass_points))
    twosig = ROOT.TGraphAsymmErrors(len(mass_points))
    for i, mass in enumerate(mass_points):
        mass_result = result[key][mass]
        median = mass_result.get('exp')
        exp.SetPoint(i, mass, median)
        onesig.SetPoint(i, mass, median)
        twosig.SetPoint(i, mass, median)
        onesig.SetPointEYlow(i,  median - mass_result['-1'])
        onesig.SetPointEYhigh(i, mass_result['+1'] - median )
        twosig.SetPointEYlow(i,  median - mass_result['-2'])
        twosig.SetPointEYhigh(i, mass_result['+2'] - median )
    exp.SetLineStyle(2)
    exp.SetLineWidth(2)
    exp.SetLineColor(ROOT.EColor.kBlack)
    onesig.SetFillColor(ROOT.EColor.kGreen)
    twosig.SetFillColor(ROOT.EColor.kYellow)
    if smooth > 0:
        exp = smoother(exp, smooth)
        onesig = smoother(onesig, smooth)
        twosig = smoother(twosig, smooth)
    return (exp, onesig, twosig)

def build_line(result, key, type, linewidth=3):
    ''' Build the limit TGraph '''
    try:
        mass_points = sorted(result[key].keys())
    except KeyError:
        print "Couldn't find key: %s" % repr(key)
        print "Available keys: %s" % repr(result.keys())
        raise
    obs = ROOT.TGraphAsymmErrors(len(mass_points))
    for i, mass in enumerate(mass_points):
        mass_result = result[key][mass]
        limit = mass_result.get(type)
        obs.SetPoint(i, mass, limit)
    obs.SetLineWidth(linewidth)
    return obs

def build_obs_line(result, key):
    return build_line(result, key, 'obs', 3)

def build_exp_line(result, key):
    return build_line(result, key, 'exp', 2)
