'''

Muon fake rate configuration.

'''

from rootpy.plotting import views

# Prefix all outputs with 'mu_'
prefix = 'mu_'

data_sample = 'data_DoubleMu'

things_to_fit = {}

for pt_type in ['pt10', 'pt20']:
    for iso_type in ['iso15', 'iso30']:
        var = 'muonJetPt'
        fit_func = 'landau_func'
        constraint = -1,
        # Fit jet pt w/ a landau
        things_to_fit[(pt_type, iso_type, var)] = {
            'func' : fit_func,
            'constraint' : constraint
        }
        # Fit mu pt w/ an expo
        var = 'muonPt'
        fit_func = 'linear_func'
        constraint = None,
        things_to_fit[(pt_type, iso_type, var)] = {
            'func' : fit_func,
            'constraint' : constraint
        }
        var = 'tauBtag'
        fit_func = 'linear_func'
        constraint = None,
        things_to_fit[(pt_type, iso_type, var)] = {
            'func' : fit_func,
            'constraint' : constraint
        }


# Function to build the regions to do the measurements in
def make_regions(sample):
    regions = {
        'wjets' :  views.SubdirectoryView(sample, 'wjets'),
        'qcd' :  views.SubdirectoryView(sample, 'qcd'),
        'zmm' :  views.SubdirectoryView(sample, 'zmm'),
        'zmm_tau20' :  views.SubdirectoryView(sample, 'zmm_tau20'),
    }
    # EWK is combo of wjets and ZMM
    #regions['ewk'] = views.SumView(regions['wjets'], regions['zmm']),
    return regions
