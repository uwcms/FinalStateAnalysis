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
        'legendstyle' : 'lf',
        'format' : 'hist',
        'fillcolor' :colors['red'],
        'name' : "Z + jets",
    },
    'WplusJets*' : {
        'legendstyle' : 'lf',
        'format' : 'hist',
        'fillcolor' : colors['green'],
        'name' : "W + jets",
    },
    'QCDMu' : {
        'legendstyle' : 'lf',
        'format' : 'hist',
        'fillcolor' : colors['magenta'],
        'name' : "QCD",
    },
    'TT*' : {
        'legendstyle' : 'lf',
        'format' : 'hist',
        'fillcolor' : colors['orange'],
        'name' : "ttbar",
    },
    'VH*' : {
        'legendstyle' : 'lf',
        'format' : 'hist',
        'fillcolor' : 0,
        'fillstyle' : 0,
        'linestyle' : 2,
        'linewidth' : 4,
        'linecolor' : colors['green'],
        'name' : "VH",
    },
    'WZ*' : {
        'legendstyle' : 'lf',
        'format' : 'hist',
        'fillcolor' : colors['blue'],
        'name' : "WZ",
    },
    'ZZ*' : {
        'legendstyle' : 'lf',
        'format' : 'hist',
        'fillcolor' : colors['cyan'],
        'name' : "ZZ",
    },
    'data*' : {
        'legendstyle' : 'pe',
        'format' : 'pe',
        'name' : "data",
    },
}

