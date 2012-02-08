#!/usr/bin/env python

# Check rate of mu+ mu- tau_h- --> mu+ mu+ tau_h-

import logging
logging.basicConfig(
    filename='analysis.log',level=logging.DEBUG, filemode='w')
log = logging.getLogger("checkMuonCharge")
import analysis_cfg
import ROOT
import os
import FinalStateAnalysis.PatTools.data as data_tool

if __name__ == "__main__":
    log.info("Beginning analysis")
    ############################################################################
    ### Load the data ##########################################################
    ############################################################################
    int_lumi = analysis_cfg.INT_LUMI
    skips = ['DoubleEl', 'EM', 'MuEG']
    samples, plotter = data_tool.build_data(
        'VH', analysis_cfg.JOBID, 'scratch_results',
        int_lumi, skips, count='emt/skimCounter', unweighted=True)

    mumusamples, mumuplotter = data_tool.build_data(
        'VH', '2012-01-28-v1-MuonTP', 'scratch_results',
        int_lumi, skips + ['WW', 'VH', 'TTW', 'TTZ', 'WWW', 'WZ', 'ZZ'],
        count='emt/skimCounter', unweighted=True)

    canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)

    channel = analysis_cfg.cfg['mmt']
    charge_cat_cfg = channel['charge_categories']['mumu']

    object1_cfg = charge_cat_cfg['object1']
    object2_cfg = charge_cat_cfg['object2']
    object3_cfg = charge_cat_cfg['object3']

    cuts = channel['baseline'] \
            + charge_cat_cfg['selections']['final']['cuts'] \
            + object1_cfg['pass'] + object2_cfg['pass'] + object3_cfg['pass']

    # Always require the muons are the opposite sign
    cuts += ['Muon1Charge*Muon2Charge < 0']

    # Now make two categories - where the lead muon can flip, and where the
    # subleading muon can flip.  This prevents counting cases where the charge
    # would become 3.
    lead_can_flip = cuts + ['Muon1Charge*TauCharge > 0']
    sublead_can_flip = cuts + ['Muon2Charge*TauCharge > 0']

    plotter.register_tree(
        'lead_can_flip',
        '/mmt/final/Ntuple',
        'Muon1Pt',
        ' && '.join(lead_can_flip),
        binning = [100, 0, 1000],
        include = ['*data*'],
    )

    plotter.register_tree(
        'sublead_can_flip',
        '/mmt/final/Ntuple',
        'Muon2Pt',
        ' && '.join(sublead_can_flip),
        binning = [100, 0, 1000],
        include = ['*data*'],
    )

    # NB object1 is muon2
    mc_cut = list(channel['baseline']
            + charge_cat_cfg['selections']['final']['cuts']
            + object1_cfg['pass'] + object3_cfg['fail']
            + ['Muon1_MuRelIso < 0.3']
            + ['Muon1Charge*Muon2Charge > 0']
             )

    plotter.register_tree(
        'ss_muons_one_tight_one_global',
        '/mmt/final/Ntuple',
        'Muon1Pt',
        ' && '.join(mc_cut),
        binning = [100, 0, 1000],
        include = ['*Zj*'],
    )

    plotter.register_tree(
        'ss_muons_both_tight',
        '/mmt/final/Ntuple',
        'Muon1Pt',
        ' && '.join(mc_cut + ['Muon1_MuID_WWID > 0.5', 'Muon1_MuRelIso < 0.3']),
        binning = [100, 0, 1000],
        include = ['*Zj*'],
    )

    mc_loose = plotter.get_histogram(
        'Zjets',
        '/mmt/final/Ntuple:ss_muons_one_tight_one_global',
    )

    mc_tight = plotter.get_histogram(
        'Zjets',
        '/mmt/final/Ntuple:ss_muons_both_tight',
    )
    print "Loose and tight rates using mumu+tau nuple"
    print "loose", mc_loose.Integral(), "tight", mc_tight.Integral()

    # Try using singlemu dataset - need to use muon2, since muon1 has
    # the cut applied in the skim
    mumu_cut = list([x for x in channel['baseline']
                     if 'Tau' not in x and 'Muon2_Mass' not in x]
            + charge_cat_cfg['selections']['final']['cuts']
            + object2_cfg['pass']
            + ['Muon2_MuRelIso < 0.3']
            + ['Muon1Charge*Muon2Charge > 0']
             )

    #print mumu_cut

    mumuplotter.register_tree(
        'ss_muons_one_tight_one_global',
        '/mm/final/Ntuple',
        'Muon2Pt',
        ' && '.join(mumu_cut),
        binning = [100, 0, 1000],
        include = ['*Zj*'],
    )

    mumuplotter.register_tree(
        'ss_muons_both_tight',
        '/mm/final/Ntuple',
        'Muon2Pt',
        ' && '.join(mumu_cut + ['Muon2_MuID_WWID > 0.5', 'Muon2_MuRelIso < 0.3']),
        binning = [100, 0, 1000],
        include = ['*Zj*'],
    )

    mc_loose = mumuplotter.get_histogram(
        'Zjets',
        '/mm/final/Ntuple:ss_muons_one_tight_one_global',
    )

    mc_tight = mumuplotter.get_histogram(
        'Zjets',
        '/mm/final/Ntuple:ss_muons_both_tight',
    )

    print "Loose and tight rates using mumu nuple"
    print "loose", mc_loose.Integral(), "tight", mc_tight.Integral()


    lead_unweighted = plotter.get_histogram(
        'data_DoubleMu',
        '/mmt/final/Ntuple:lead_can_flip',
    )
    sublead_unweighted = plotter.get_histogram(
        'data_DoubleMu',
        '/mmt/final/Ntuple:sublead_can_flip',
    )

    def saveplot(filename):
        # Save the current canvas
        filetype = '.pdf'
        canvas.SetLogy(False)
        canvas.Update()
        filename = os.path.join("plots", 'muChargeMisID',
                                filename + filetype)
        log.info('saving %s', filename)
        canvas.Print(filename)
        canvas.SetLogy(True)
        canvas.Update()
        canvas.Print(filename.replace(filetype, '_log' + filetype))

    print "Lead integral", lead_unweighted.Integral()
    lead_unweighted.Draw()
    saveplot('lead_unweighted')

    print "SubLead integral", sublead_unweighted.Integral()
    sublead_unweighted.Draw()
    saveplot('sublead_unweighted')

    # Rebin
    binning = [0, 10, 20, 30, 50, 100, 300, 1000]
    lead_unweighted = lead_unweighted.cloneAndRebin(binning)
    sublead_unweighted = sublead_unweighted.cloneAndRebin(binning)

    lead_unweighted.Draw()
    saveplot('lead_unweighted_rebinned')

    sublead_unweighted.Draw()
    saveplot('sublead_unweighted_rebinned')

    middles = [
        (15, 0.000019464095124069065),
        (25, 0.000035576400614197516),
        (40, 0.00006731462501893484),
        (75, 0.00022753962114866721),
        (200, 0.0029517888112709826),
        (600, 0.021948624227534932),
    ]

    lead_unweighted_total = 0
    lead_weighted_total = 0
    sublead_unweighted_total = 0
    sublead_weighted_total = 0
    for bin_center, scale_factor in middles:
        print "lead: ", bin_center, lead_unweighted(bin_center), \
                lead_unweighted(bin_center)*scale_factor
        lead_unweighted_total += lead_unweighted(bin_center)
        lead_weighted_total += lead_unweighted(bin_center)*scale_factor
        sublead_unweighted_total += sublead_unweighted(bin_center)
        sublead_weighted_total += sublead_unweighted(bin_center)*scale_factor

    print "Lead unweighted integral", lead_unweighted_total,\
            "lead weighted integral", lead_weighted_total
    print "Sublead unweighted integral", sublead_unweighted_total,\
            "sublead weighted integral", sublead_weighted_total

