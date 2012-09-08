'''

Estimate the scale uncertainties on the simulated samples due to
the electron and tau energy scale

'''


import FinalStateAnalysis.PatTools.data as data_tool
import analysis_cfg
import logging
import json
from json import encoder
encoder.FLOAT_REPR = lambda o: format(o, '.4f')

# Setup logging
logging.basicConfig(
    filename='estimateScaleSystematics.log',level=logging.DEBUG, filemode='w')
log = logging.getLogger("analysis")
stderr_log = logging.StreamHandler()
log.addHandler(stderr_log)

int_lumi = analysis_cfg.INT_LUMI
jobid = '2012-02-01-v1-WHAnalyze'

skips = ['DoubleEl', 'EM']
samples, plotter = data_tool.build_data(
    'VH', jobid, 'scratch_results',
    int_lumi, skips, count='emt/skimCounter')

results = {}
for channel, channel_cfg in analysis_cfg.cfg.iteritems():
    log.info("Analyzing channel: %s", channel)
    if channel in analysis_cfg.skip:
        log.warning("Skipping channel %s!!", channel)
        continue
    channel_results = {}
    results[channel] = channel_results
    # The baseline selection
    baseline = channel_cfg['baseline']
    # Get samples to exclude
    exclude = channel_cfg['exclude'] + ['data*']
    ntuple = channel_cfg['ntuple']
    # Get primary dataset
    primds = channel_cfg['primds']
    for charge_cat, charge_cat_cfg in channel_cfg['charge_categories'].iteritems():
        if (channel, charge_cat) in analysis_cfg.skip:
            log.warning("Skipping channel+charge_cat %s+%s!!",
                        channel, charge_cat)
            continue
        log.info("-- charge category: %s", charge_cat)

        extra_selections = charge_cat_cfg['cat_baseline']
        # The final analysis cuts
        final_selections = charge_cat_cfg['selections']['final']['cuts']

        # Get the configuration for the fake objects
        object1_cfg = charge_cat_cfg['object1']
        object2_cfg = charge_cat_cfg['object2']
        object3_cfg = charge_cat_cfg['object3']

        ####################################################################
        ### First, select the final events #################################
        ####################################################################
        log.info("---- selecting final events in data...")
        ultimate_selection = baseline + extra_selections + final_selections\
                + object1_cfg['pass'] + object2_cfg['pass'] + \
                object3_cfg['pass']

        plot_base_name = '_'.join(
            [channel, charge_cat, 'final'])

        def make_mapper(substring, replace_with):
            def mapper_fun(x):
                if substring in x:
                    replaced = x.replace(substring, replace_with)
                    print "%s --> %s" % (x, replaced)
                    return replaced
                return x
            return mapper_fun

        value_for_electrons = \
                '((ElecAbsEta < 1.5)*0.01 + (ElecAbsEta >= 1.5)*0.025)'
        value_for_electrons_up = '(1.0 + %s)' % value_for_electrons
        value_for_electrons_down = '(1.0 - %s)' % value_for_electrons

        # Be careful about the order of these!  (prevent double replaces)
        sys_mapper = {
            'nom' : [lambda x: x],
            'tau_up' : [
                make_mapper('TauPt ', '1.03*TauPt'),
                make_mapper('VisFinalState_Ht ', '(VisFinalState_Ht + 0.03*TauPt)'),
            ],
            'tau_down' : [
                make_mapper('TauPt ', '0.97*TauPt'),
                make_mapper('VisFinalState_Ht ', '(VisFinalState_Ht - 0.03*TauPt)'),
            ],

            'e_up' : [
                make_mapper('ElecPt ', '%s*ElecPt' % value_for_electrons_up),
                make_mapper('VisFinalState_Ht ', '(VisFinalState_Ht + %s*ElecPt)' % value_for_electrons),
                make_mapper('ERelIso', 'ERelIso*(1/%s)' % value_for_electrons_up),
            ],
            'e_down' : [
                make_mapper('ElecPt ', '%s*ElecPt' % value_for_electrons_down),
                make_mapper('VisFinalState_Ht ', '(VisFinalState_Ht - %s*ElecPt)' % value_for_electrons),
                make_mapper('ERelIso', 'ERelIso*(1/%s)' % value_for_electrons_down),
            ]
        }

        samples = ['ZZ', 'WZ']

        for mass in [100, 110, 115, 120, 130, 140, 150, 160]:
            samples.append('VH%i' % mass)
            if mass >= 120:
                samples.append('VH%iWW' % mass)

        for sample in samples:
            channel_results[sample] = {}

            for systematic in ['nom', 'tau_up', 'tau_down', 'e_up', 'e_down']:
                if 'mmt' in channel and 'e_' in systematic:
                    continue

                print "SYS", systematic
                new_cuts = []
                for cut in ultimate_selection:
                    replaced = cut
                    for sys_map in sys_mapper[systematic]:
                        replaced = sys_map(replaced)
                    new_cuts.append(replaced)

                plotter.register_tree(
                    'sys_check_' + plot_base_name + '_' + systematic,
                    ntuple,
                    '1',
                    ' && '.join(new_cuts),
                    #w = weight,
                    binning = [1, -10, 10],
                    include = [sample],
                    exclude = exclude,
                )

                histo = plotter.get_histogram(
                    sample,
                    ntuple + ':' + 'sys_check_' + plot_base_name + '_' + systematic,
                    rebun = 5, show_overflows = True
                )
                print sample, histo.Integral()
                channel_results[sample][systematic] = histo.Integral()

            for sys in list(channel_results[sample].keys()):
                value = channel_results[sample][sys]
                if 'up' in sys or 'down' in sys:
                    nom_val = channel_results[sample]['nom']
                    channel_results[sample][sys + '_scale'] = (value/nom_val-1.)

with open('scale_systematics.json', 'w') as scale_json:
    scale_json.write(json.dumps(results, sort_keys=True, indent=2) + '\n')

