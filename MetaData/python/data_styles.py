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
        'format' : 'hist',
        'fillcolor' : '#FFCC66',
        'linecolor' : '#000000',
        'name' : "Z + jets",
    },
    'WplusJets*' : {
        'legendstyle' : 'f',
        'format' : 'hist',
        'fillcolor' : '#990000',
        'name' : "W + jets",
    },
    'QCD*' : {
        'legendstyle' : 'f',
        'format' : 'hist',
        'fillcolor' : colors['magenta'],
        'linecolor' :colors['magenta'],
        'name' : "QCD",
    },
    'TT*' : {
        'legendstyle' : 'f',
        'format' : 'hist',
        'fillcolor' : '#9999CC',
        'linecolor' : '#9999CC',
        'name' : "ttbar",
    },
    'VH*' : {
        'legendstyle' : 'l',
        'format' : 'hist',
        'fillcolor' : 0,
        'fillstyle' : 0,
        'linestyle' : 2,
        'linewidth' : 4,
        'linecolor' : '#1C1C76',
        'name' : "VH",
    },
    'WZ*' : {
        'legendstyle' : 'f',
        'format' : 'hist',
        'fillcolor' : colors['blue'],
        'linecolor' : colors['blue'],
        'name' : "WZ",
    },
    'WW*' : {
        'legendstyle' : 'f',
        'format' : 'hist',
        'fillcolor' : colors['red'],
        'linecolor' : colors['red'],
        'name' : "WW",
    },
    'ZZ*' : {
        'legendstyle' : 'f',
        'format' : 'hist',
        'linecolor' : '#50A634',
        'fillcolor' : '#50A634',
        'name' : "ZZ",
    },
    'data*' : {
        'legendstyle' : 'pe',
        'format' : 'pe',
        'name' : "Observed",
    },
}

