'''

Tool to lookup Higgs cross sections and branching ratios
========================================================

Wrapper around HCSaW provided by M. Snowball (UF)

Author: Evan K. Friis, UW Madison

Getting a cross section
-----------------------

>>> wh_cs = cross_section('WH', 120.0, 7)
>>> abs(wh_cs - 0.6561) < 1e-6
True

Getting all info about a cross section
--------------------------------------

The following data are returned in a dictionary::

* xsec
* +             (the total error up)
* -             (the total error down)
* scale+
* scale-
* pdf+
* pdf-

The errors are returned as relative deviations from the mean.

>>> wh_cs_info = cross_section_info('WH', 120.0, 7)
>>> # Check the value from the Yellow Report (it's reported in %)
>>> "%0.1f" % (wh_cs_info['scale-']*100)
'-0.7'

Getting a BR
------------

>>> h_ww_br = branching_ratio('WW', 120.0)
>>> abs(h_ww_br - 1.43E-01) < 1e-6
True

'''

import ROOT

# Load the library with the lookup tables
ROOT.gSystem.Load('libFinalStateAnalysisMetaData')

from ROOT import HiggsCSandWidth

_sm = HiggsCSandWidth()

_xsec_map = {
    'ggH' : 1,
    'VBF' : 2,
    'WH' : 3,
    'ZH' : 4,
    'ttH' : 5,
    'total' : 0
}

_br_map = {
    'total' : 0,
    'bb' : 1,
    'tautau' : 2,
    'mumu' : 3,
    'ss' : 4,
    'cc' : 5,
    'tt' : 6,
    'gg' : 7,
    'gamgam' : 8,
    'gamZ' : 9,
    'WW' : 10,
    'ZZ' : 11,
}


def cross_section_info(process, mass, sqrts, spline=True):
    if isinstance(process, basestring):
        process = _xsec_map[process]
    output = {}
    output['xsec'] = _sm.HiggsCS(process, mass, sqrts, spline)
    output['+'] = _sm.HiggsCSErrPlus(process, mass, sqrts)
    output['-'] = _sm.HiggsCSErrMinus(process, mass, sqrts)
    output['scale+'] = _sm.HiggsCSscaleErrPlus(process, mass, sqrts)
    output['scale-'] = _sm.HiggsCSscaleErrMinus(process, mass, sqrts)
    output['pdf+'] = _sm.HiggsCSpdfErrPlus(process, mass, sqrts)
    output['pdf-'] = _sm.HiggsCSpdfErrMinus(process, mass, sqrts)
    return output

def cross_section(process, mass, sqrts, spline=True):
    return cross_section_info(process, mass, sqrts, spline)['xsec']

def branching_ratio(process, mass, spline=True):
    if isinstance(process, basestring):
        process = _br_map[process]
    return _sm.HiggsBR(process, mass, spline)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
