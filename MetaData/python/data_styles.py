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
    'Zjets*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : '#FFCC66',
        'linecolor' : '#000000',
        'name' : "Z + jets",
        'fillstyle': 'solid',
        },
    'WplusJets*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : '#990000',
        'name' : "W + jets",
        'fillstyle': 'solid',
    },
    'QCD*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : colors['cyan'],
        'linecolor' :colors['cyan'],
        'name' : "QCD",
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
    'WZ*' : {
        'legendstyle' : 'f',
        'drawstyle' : 'hist',
        'fillcolor' : colors['blue'],
        'linecolor' : colors['blue'],
        'name' : "WZ",
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
        'name' : "ZZ",
        'fillstyle': 'solid',
    },
    'data*' : {
        'legendstyle' : 'pe',
        'drawstyle' : 'pe',
        'name' : "Observed",
    },
}

