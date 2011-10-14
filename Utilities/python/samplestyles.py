import styling

'''

Define common style parameters for oft-used samples


'''

SAMPLE_STYLES = {
    'ztt' : {
        'color' : styling.colors['ewk_yellow'],
        'nicename' : 'Z #rightarrow #tau #tau',
    },
    'Zjets' : {
        'color' : styling.colors['ewk_yellow'],
        'nicename' : 'Z+jets',
    },
    'zll' : {
        'color' : styling.colors['ewk_purple'],
        'nicename' : 'Z #rightarrow ll',
    },
    'Wjets' : {
        'color' : styling.colors['ewk_red'],
        'line_width' : 2,
        'nicename' : 'W+jets',
    },
    'QCD*' : {
        'color' : styling.colors['ewk_orange'],
        'nicename' : 'QCD',
    },
    'ttjets' : {
        'color' : styling.colors['ewk_light_purple'],
        'nicename' : 'tt+jets',
    },
    'WZ' : {
        'color' : styling.colors['grey'],
        'nicename' : 'WZ',
    },
    'ZZ' : {
        'color' : styling.colors['med_blue'],
        'nicename' : 'ZZ',
    },
    'WW' : {
        'color' : styling.colors['light_blue'],
        'nicename' : 'WW',
    },
    'data*' : {
        'marker_style' : 20,
        'marker_size' : 1,
        'draw_opt' : 'pe',
        'nicename' : 'Data',
    },
    'VH*' : {
        'color' : styling.colors['red'],
        ##'draw_opt' : 'lf',
        #'line_width' : 2,
        #'line_color' : styling.colors['black'],
        #'fill_color' : styling.colors['white'],
        #'fill_style' : 1,
        'nicename' : 'VHiggs',
    },
}
