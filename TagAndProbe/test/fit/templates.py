import os
import ROOT
import pprint
import FinalStateAnalysis.Utilities.RooFitTools as rft
from FinalStateAnalysis.Utilities.Histo import Histo
import FinalStateAnalysis.Utilities.HistoEqualizer as he
from data_sources import data_sources, data_name_map

regions = ['os_pass', 'os_fail', 'ss_pass', 'ss_fail']

ROOT.gROOT.SetStyle("Plain")

def build_fit_vars(ws):
    ws.factory('abstaueta[1, 0, 2.1]')
    ws.factory('pzeta[1.0, -20, 30]')
    ws.factory('mvis[1.0, 10, 200]')
    ws.factory('dca[1.0, 0, 3.0]')
    ws.factory('pt[1.0, 0, 80]')
    ws.factory('dm[1.0, 0, 80]')
    ws.factory('iso[1.0, 0, 0.3]')
    ws.factory('mt[1.0, 0, 100]')
    #ws.defineSet('fit_vars', 'abstaueta,pzeta')
    #ws.defineSet('fit_vars', 'pt')
    #ws.defineSet('fit_vars', 'pt,pzeta')
    #ws.defineSet('fit_vars', 'dca')
    #ws.defineSet('fit_vars', 'dca,pzeta')
    #ws.defineSet('fit_vars', 'mvis,dm,pzeta')
    ws.defineSet('fit_vars', 'mvis')
    #ws.defineSet('all_vars', 'pzeta,mvis,abstaueta,pt,dca')
    ws.defineSet('all_vars', 'pzeta,mvis,pt,dca,abstaueta,dm,iso,mt')
    #ws.defineSet('fit_vars', 'abstaueta')
    ws.var("abstaueta").SetTitle("|#eta_{#tau}|")
    ws.var("pzeta").SetTitle("P_{#zeta}")
    ws.var("mvis").SetTitle("m_{vis}")
    ws.var("pt").SetTitle("p_{T}^{#tau}")
    ws.var("dm").SetTitle("Tau Decay Mode")
    ws.var("iso").SetTitle("Muon Rel. Iso")
    ws.var("mt").SetTitle("MT1MEt")

def get_th1(sample, region, histo, rebin=None):
    th1 = data_sources[data_name_map[sample]]['file'].get_weighted(os.path.join(
        "ohyeah", region, histo))
    assert(th1)
    if rebin and rebin > 1:
        return Histo(th1, rebin = rebin)
    else:
        return Histo(th1)

def ws_importer(ws):
    # Work around the limitation reserved word limitation affecting
    # RooWorkspace::import
    method = getattr(ws, 'import')
    return method

def build_templates(ws):

    rooVars = {
        'abstaueta' : ws.var('abstaueta'),
        'pzeta' : ws.var('pzeta'),
        'dca' : ws.var('dca'),
        'mvis' : ws.var('mvis'),
        'pt' : ws.var('pt'),
        'dm' : ws.var('dm'),
        'iso' : ws.var('iso'),
        'mt' : ws.var('mt'),
    }

    rebinning = {
        'abstaueta' : 10,
        'pzeta' : 5,
        'dca' : 4,
        'mvis' : 4,
        'pt' : 1,
        'dm' : 1,
        'iso' : 1,
        'mt' : 4,
    }

    rebinning_region = {
        'os_pass': 1,
        'ss_pass': 1,
        #'ss_pass': 1,
        'os_fail': 1,
        'ss_fail': 1,
    }


    # Map the names in the root files to the style we use in the fit
    folder_map = {
        'os_pass': 'PassOS',
        'ss_pass': 'PassSS',
        'os_fail': 'FailOS',
        'ss_fail': 'FailSS',
    }

    folder_map_noid = {
        'os_pass': 'OS',
        'ss_pass': 'SS',
        'os_fail': 'OS',
        'ss_fail': 'SS',
    }

    var_map = {
        'abstaueta' : 'AbsTauEta',
        'pzeta' : 'PZeta',
        'dca' : 'LogDCASig2D',
        'mvis' : 'Mvis',
        'pt' : 'TauPt',
        'dm' : 'TauDecayMode',
        'iso' : 'MuonIso',
        'mt' : 'MT1',
    }

    importer = ws_importer(ws)

    # #########################################################################
    # Make QCD templates
    # #########################################################################
    #  We take everything right now from the anti-iso region, except Mvis?
    for var in ['abstaueta', 'pzeta', 'dca', 'pt', 'mt']:
        for region in regions:
            print var, region
            # Get the anti-iso region
            histo = get_th1('data', 'qcd' + folder_map[region], var_map[var],
                            rebin=rebinning[var]*rebinning_region[region])
            # Get as roodatahist.  We need to keep this, because other wise
            # the GC will kill it and the PDF references it.
            datahist, datapdf = histo.makeRooHistPdf(rooVars[var])
            pdf_name = 'pdf_qcd_%s_%s' % (region, rooVars[var].GetName())
            datahist_name = pdf_name + '_hist'
            datapdf.SetName(pdf_name)
            datahist.SetName(datahist_name)
            importer(datapdf)
            #importer(datahist)

    # From MC
    for var in ['dm', 'iso']:
        for region in regions:
            print var, region
            histo = get_th1('qcd', 'sig' + folder_map[region], var_map[var],
                            rebin=rebinning[var]*rebinning_region[region])
            # Get as roodatahist.  We need to keep this, because other wise
            # the GC will kill it and the PDF references it.
            datahist, datapdf = histo.makeRooHistPdf(rooVars[var])
            pdf_name = 'pdf_qcd_%s_%s' % (region, rooVars[var].GetName())
            datahist_name = pdf_name + '_hist'
            datapdf.SetName(pdf_name)
            datahist.SetName(datahist_name)
            importer(datapdf)

    #for var in ['mvis']:
        #for region in regions:
            #print var, region
            ## Get the anti-iso region
            #histo = get_th1('qcd', 'qcd' + folder_map[region], var_map[var],
                            #rebin=rebinning[var]*rebinning_region[region])
            ## Get as roodatahist.  We need to keep this, because other wise
            ## the GC will kill it and the PDF references it.
            #datahist, datapdf = histo.makeRooHistPdf(rooVars[var])
            #pdf_name = 'pdf_qcd_%s_%s' % (region, rooVars[var].GetName())
            #datahist_name = pdf_name + '_hist'
            #datapdf.SetName(pdf_name)
            #datahist.SetName(datahist_name)
            #importer(datapdf)

    # First correct W+jets contribution to sigFailSS
    wjets_factor = get_th1('wjets', 'sigFailSS', 'AbsTauEta').Integral()/ \
            get_th1('wjets', 'wjetsFailSS', 'AbsTauEta').Integral()

    wjets_yield = wjets_factor*get_th1(
        'data', 'wjetsFailSS', 'AbsTauEta').Integral()

    wjets_shape = get_th1('wjets', 'sigFailSS', 'Mvis',
        rebin=rebinning['mvis']*rebinning_region['os_pass'])

    wjets_shape = wjets_shape*(wjets_yield/wjets_shape.Integral())

    # Subtract the W from tomorrow
    data_sigfailss = get_th1(
        'data', 'sigFailSS', 'Mvis',
        rebin=rebinning['mvis']*rebinning_region['os_pass'])

    data_sigfailss = data_sigfailss - wjets_shape

    # Figure out the pass shape from the fail shape
    data_qcd_fail = get_th1('data', 'qcdFailSS', 'Mvis') + \
            get_th1('data', 'qcdFailOS', 'Mvis')
    data_qcd_pass = get_th1('data', 'qcdPassSS', 'Mvis') + \
            get_th1('data', 'qcdPassOS', 'Mvis')

    fail_pass_tr = he.HistoEqualizer(data_qcd_fail, data_qcd_pass)
    #data_sigfailss_transformed = data_sigfailss.transform(fail_pass_tr)

    # Take template from PassSS data
    wjets_factor = get_th1('wjets', 'sigPassSS', 'AbsTauEta').Integral()/ \
            get_th1('wjets', 'wjetsPassSS', 'AbsTauEta').Integral()

    wjets_yield = wjets_factor*get_th1(
        'data', 'wjetsPassSS', 'AbsTauEta').Integral()

    wjets_shape = get_th1('wjets', 'sigPassSS', 'Mvis',
        rebin=rebinning['mvis']*rebinning_region['os_pass'])
    wjets_shape = wjets_shape*(wjets_yield/wjets_shape.Integral())

    data_sigpassss = get_th1(
        'data', 'sigPassSS', 'Mvis',
        rebin=rebinning['mvis']*rebinning_region['os_pass'])

    data_sigpassss_corrected = data_sigpassss - wjets_shape

    for var in ['mvis']:
        for region in regions:
            histo = None
            if 'fail' in region:
                histo = data_sigfailss
            else:
                #histo = data_sigfailss_transformed
                histo = data_sigpassss_corrected
            # Get as roodatahist.  We need to keep this, because other wise
            # the GC will kill it and the PDF references it.
            datahist, datapdf = histo.makeRooHistPdf(rooVars[var])
            pdf_name = 'pdf_qcd_%s_%s' % (region, rooVars[var].GetName())
            datahist_name = pdf_name + '_hist'
            datapdf.SetName(pdf_name)
            datahist.SetName(datahist_name)
            importer(datapdf)

    # #########################################################################
    # Make Wjets templates
    # #########################################################################
    #  Pzeta and Mvis comes from MC
    for var in ['pzeta', 'mvis', 'mt']:
        for region in regions:
            histo = get_th1('wjets', 'sig' + folder_map[region], var_map[var],
                            rebin=rebinning[var]*rebinning_region[region])
            datahist, datapdf = histo.makeRooHistPdf(rooVars[var])
            pdf_name = 'pdf_wjets_%s_%s' % (region, rooVars[var].GetName())
            datahist_name = pdf_name + '_hist'
            datapdf.SetName(pdf_name)
            datahist.SetName(datahist_name)
            importer(datapdf)

    # Eta comes from data
    for var in ['abstaueta', 'dca', 'pt', 'dm', 'iso']:
        for region in regions:
            histo = get_th1('data', 'wjets' + folder_map[region], var_map[var],
                            rebin=rebinning[var]*rebinning_region[region])
            datahist, datapdf = histo.makeRooHistPdf(rooVars[var])
            pdf_name = 'pdf_wjets_%s_%s' % (region, rooVars[var].GetName())
            datahist_name = pdf_name + '_hist'
            datapdf.SetName(pdf_name)
            datahist.SetName(datahist_name)
            importer(datapdf)

    # #########################################################################
    # Make ZTT templates
    # #########################################################################
    #  Everything comes from MC, taking only real taus
    for var in ['abstaueta', 'pzeta', 'mvis', 'dca', 'pt', 'dm', 'iso', 'mt']:
        for region in regions:
            # Get the anti-iso region
            histo = get_th1(
                'zjets', 'sig' + folder_map[region] + '/realTau', var_map[var],
                rebin=rebinning[var]*rebinning_region[region])
            # Get as roodatahist.  We need to keep this, because other wise
            # the GC will kill it and the PDF references it.
            datahist, datapdf = histo.makeRooHistPdf(rooVars[var])
            pdf_name = 'pdf_ztt_%s_%s' % (region, rooVars[var].GetName())
            datahist_name = pdf_name + '_hist'
            datapdf.SetName(pdf_name)
            datahist.SetName(datahist_name)
            importer(datapdf)

    # #########################################################################
    # Make ZTT (fake) templates
    # #########################################################################
    for var in ['abstaueta', 'pzeta', 'mvis', 'dca', 'pt', 'dm', 'iso', 'mt']:
        for region in regions:
            # We can't get the templates from the PassSS region, since the
            # statistics is really poor.  So we don't apply any TauID when
            # building the templates.
            folder = 'sigOS' if 'os_' in region else 'sigSS'
            histo = get_th1(
                'zjets', folder + '/fakeTau', var_map[var],
                rebin=rebinning[var]*rebinning_region[region])
            # Get as roodatahist.  We need to keep this, because other wise
            # the GC will kill it and the PDF references it.
            datahist, datapdf = histo.makeRooHistPdf(rooVars[var])
            pdf_name = 'pdf_zjetsfakes_%s_%s' % (region, rooVars[var].GetName())
            datahist_name = pdf_name + '_hist'
            datapdf.SetName(pdf_name)
            datahist.SetName(datahist_name)
            importer(datapdf)

    ## #########################################################################
    ## Make ZLL templates
    ## #########################################################################
    ##  Everything comes from MC, not splitting pass/fail
    #for var in ['abstaueta', 'pzeta', 'mvis', 'dca', 'pt', 'dm', 'iso', 'mt']:
        #for region in regions:
            ## Get the anti-iso region
            #histo = get_th1(
                #'zll', 'sig' + folder_map_noid[region], var_map[var],
                #rebin=rebinning[var]*rebinning_region[region])
            ## Get as roodatahist.  We need to keep this, because other wise
            ## the GC will kill it and the PDF references it.
            #datahist, datapdf = histo.makeRooHistPdf(rooVars[var])
            #pdf_name = 'pdf_zll_%s_%s' % (region, rooVars[var].GetName())
            #datahist_name = pdf_name + '_hist'
            #datapdf.SetName(pdf_name)
            #datahist.SetName(datahist_name)
            #importer(datapdf)

    # #########################################################################
    # Make ttbar templates
    # #########################################################################
    #  Everything comes from MC
    for var in ['abstaueta', 'pzeta', 'mvis', 'dca', 'pt', 'dm', 'iso', 'mt']:
        for region in regions:
            # Get the anti-iso region
            histo = get_th1(
                'ttbar', 'sig' + folder_map[region], var_map[var],
                rebin=rebinning[var]*rebinning_region[region])
            # Get as roodatahist.  We need to keep this, because other wise
            # the GC will kill it and the PDF references it.
            datahist, datapdf = histo.makeRooHistPdf(rooVars[var])
            pdf_name = 'pdf_ttbar_%s_%s' % (region, rooVars[var].GetName())
            datahist_name = pdf_name + '_hist'
            datapdf.SetName(pdf_name)
            datahist.SetName(datahist_name)
            importer(datapdf)

    # ##############################################################################
    # Build categorization
    # ##############################################################################

    fit_vars = ws.set('fit_vars')
    all_vars = ws.set('all_vars')
    for var in rft.iter_collection(all_vars):
        category_list = []
        for region in regions:
            category_list.append('%s_%s' % (region, var.GetName()))
        ws.factory(
            'categories_%s[%s]' % (var.GetName(),",".join(category_list)))

    # ##############################################################################
    # Build data
    # ##############################################################################
    #
    debug = open('debug.txt', 'w')
    debug.write("wtf")
    debug.flush()


    for var in rft.iter_collection(all_vars):
        keep = []
        combo_data_args = [
        ]
        for region in regions:
            histo = get_th1(
                'data', 'sig' + folder_map[region], var_map[var.GetName()],
                rebin=rebinning[var.GetName()]*rebinning_region[region]
                #rebin=rebinning[var.GetName()]
            )
            print histo
            keep.append(histo)
            datahist = histo.makeRooDataHist(var)
            datahist.SetName('data_%s_%s' % (region, var.GetName()))
            importer(datahist)
            combo_data_args.append(
                ROOT.RooFit.Import('%s_%s' % (region, var.GetName()),
                 histo.th1)
            )

        combo_data = ROOT.RooDataHist(
            "data_combo_%s" % var.GetName(), "Combined data",
            ROOT.RooArgList(var),
            ROOT.RooFit.Index(ws.cat("categories_%s" % var.GetName())),
            *combo_data_args
        )
        importer(combo_data)


def get_initial_sizes(fit_fail_ss = False, fit_pass_ss = True):
    output = {}
    for sample in ['wjets', 'qcd', 'ttbar', 'data']:
        pass_os = get_th1(sample, 'sigPassOS', 'AbsTauEta').Integral()
        pass_ss = get_th1(sample, 'sigPassSS', 'AbsTauEta').Integral()
        fail_os = get_th1(sample, 'sigFailOS', 'AbsTauEta').Integral()
        fail_ss = get_th1(sample, 'sigFailSS', 'AbsTauEta').Integral()
        output['n_%s_os_pass' % sample]  = pass_os
        output['n_%s_os_fail' % sample]  = fail_os
        output['n_%s_ss_pass' % sample]  = pass_ss
        output['n_%s_ss_fail' % sample]  = fail_ss
        output['n_%s_all_pass' % sample] = pass_os
        if True or fit_pass_ss:
            output['n_%s_all_pass' % sample] += pass_ss
        output['n_%s_all_fail' % sample] = fail_os
        if True or fit_fail_ss: # always do this because of layout of fit model
            output['n_%s_all_fail' % sample] += fail_ss

    # Real ZTT taus
    pass_os = get_th1('zjets', 'sigPassOS/realTau', 'AbsTauEta').Integral()
    pass_ss = get_th1('zjets', 'sigPassSS/realTau', 'AbsTauEta').Integral()
    fail_os = get_th1('zjets', 'sigFailOS/realTau', 'AbsTauEta').Integral()
    fail_ss = get_th1('zjets', 'sigFailSS/realTau', 'AbsTauEta').Integral()
    sample = 'ztt'
    output['n_%s_all_pass' % sample] = pass_os
    if fit_pass_ss:
        output['n_%s_all_pass' % sample] += pass_ss
    output['n_%s_all_fail' % sample] = fail_os
    if fit_fail_ss:
        output['n_%s_all_fail' % sample] += fail_ss

    # ZTT fake contribution
    pass_os = get_th1('zjets', 'sigPassOS/fakeTau', 'AbsTauEta').Integral()
    pass_ss = get_th1('zjets', 'sigPassSS/fakeTau', 'AbsTauEta').Integral()
    fail_os = get_th1('zjets', 'sigFailOS/fakeTau', 'AbsTauEta').Integral()
    fail_ss = get_th1('zjets', 'sigFailSS/fakeTau', 'AbsTauEta').Integral()
    sample = 'zjetsfakes'
    output['n_%s_all_pass' % sample] = pass_os
    if True or fit_pass_ss:
        output['n_%s_all_pass' % sample] += pass_ss
    output['n_%s_all_fail' % sample] = fail_os
    if True or fit_fail_ss:
        output['n_%s_all_fail' % sample] += fail_ss

    return output

if __name__ == "__main__":
    ws = ROOT.RooWorkspace("workspace")
    build_fit_vars(ws)
    build_templates(ws)
    #ws.Print("v")
    pprint.pprint(get_initial_sizes())
