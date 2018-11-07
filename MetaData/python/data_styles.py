'''

Define styles for the different data samples.

The keys correspond to "logical" samples, defined in data_name_map of
datadefs.py

The values are dictionaries, which can be passed as kwargs to objects which
inherit from rootpy Plottable


http://ndawe.github.com/rootpy/reference/rootpy.plotting.html#rootpy.plotting.core.Plottable

'''

from FinalStateAnalysis.Utilities.solarized import colors

data_styles = {
    'GluGlu_LFV*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : 0,
        'fillstyle' : 0,
        'linestyle' : 1,
        'linewidth' : 4,
        'linecolor' : colors['blue'],
        'name' : "LFV ggH",
    },
    'VBF_LFV*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : 0,
        'fillstyle' : 0,
        'linestyle' : 1,
        'linewidth' : 4,
        'linecolor' : colors['orange'],
        'name' : "LFV qqH",
    },
    '*HToTauTau*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : '#1c761c',
        'fillstyle' : 'solid',
        'linecolor' : '#1c761c',
        'name' : "HTT",
    },
    'ZH*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : '#761c76',
        'fillstyle' : 'solid',
        'linestyle' : 1,
        'linewidth' : 4,
        'linecolor' : '#761c76',
        'name' : "ZH",
    },
    'WH*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : '#1c7676',
        'fillstyle' : 'solid',
        'linestyle' : 1,
        'linewidth' : 4,
        'linecolor' : '#1c7676',
        'name' : "WH",
    },
    'VBFH*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : '#43757d',
        'fillstyle' : 'solid',
        'linestyle' : 1,
        'linewidth' : 4,
        'linecolor' : '#43757d',
        'name' : "qqH",
    },
    'DY*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : '#FFCC66',
        'linecolor' : '#FFCC66',
        'name' : "Z + jets",
        'fillstyle': 'solid',
        },
    'W*Jets*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : '#990000',
        'linecolor' : '#990000',
        'name' : "W + jets",
        'fillstyle': 'solid',
    },
    'QCD*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : colors['cyan'],
        'linecolor' : colors['cyan'],
        'name' : "Fakes",
        'fillstyle': 'solid',
    },
    'TT*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : '#9999CC',
        'linecolor' : '#9999CC',
        'name' : "ttbar",
        'fillstyle': 'solid',
    },
    'ST*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : '#999900',
        'linecolor' : '#999900',
        'name' : "singlet",
        'fillstyle': 'solid',
    },
    'VH*HWW' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : colors['orange'],
        'linecolor' : colors['orange'],
        'name' : "VH H#rightarrowWW",
        'fillstyle': 'solid',
    },
    'VH*' : {
        'legendstyle' : 'l',
        'drawstyle' : 'hist',
        'fillcolor' : 0,
        'fillstyle' : 0,
        'linestyle' : 2,
        'linewidth' : 4,
        'linecolor' : '#1C1C76',
        'name' : "VH",
    },
    'WZ*ZToTauTau*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : colors['blue'],
        'linecolor' : colors['blue'],
        'name' : "WZ#rightarrowl#tau#tau",
        'fillstyle': 'solid',
    },
    'WZ*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : colors['red'],
        'linecolor' : colors['red'],
        'name' : "Diboson",
        'fillstyle': 'solid',
    },
    'WW*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : colors['red'],
        'linecolor' : colors['red'],
        'name' : "WW",
        'fillstyle': 'solid',
    },
    'ZZ*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'linecolor' : '#50A634',
        'fillcolor' : '#50A634',
        'name' : "Diboson",
        'fillstyle': 'solid',
    },
    'data*' : {
        'legendstyle' : 'pe',
        'drawstyle' : 'pe',
        'markerstyle' : 20,
#        'markersize'  : 2,
        'name' : "Observed",
    },
}

#makes life easier when converting shape files
data_styles['fakes'] = data_styles['DY*']
data_styles['zz'] = data_styles['ZZ*']
data_styles['wz'] = data_styles['WZ*']
data_styles['charge_fakes'] = data_styles['TT*']
