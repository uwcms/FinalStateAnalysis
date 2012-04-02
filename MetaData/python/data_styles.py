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
    'Zjets' : {
        'legendstyle' : 'lf',
        'format' : 'hist',
        'fillcolor' :colors['yellow'],
    },
    'Wjets' : {
        'legendstyle' : 'lf',
        'format' : 'hist',
        'fillcolor' : colors['green'],
    },
    'QCDMu' : {
        'legendstyle' : 'lf',
        'format' : 'hist',
        'fillcolor' : colors['magenta'],
    },
    'ttjets' : {
        'legendstyle' : 'lf',
        'format' : 'hist',
        'fillcolor' : colors['orange'],
    },
    'WZ_pythia' : {
        'legendstyle' : 'lf',
        'format' : 'hist',
        'fillcolor' : colors['blue'],
    },
    'ZZ' : {
        'legendstyle' : 'lf',
        'format' : 'hist',
        'fillcolor' : colors['cyan'],
    },
    'data_DoubleMu' : {
        'legendstyle' : 'pe',
        'format' : 'pe',
    },
}
