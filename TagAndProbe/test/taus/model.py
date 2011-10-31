import ROOT
from collections import defaultdict
import FinalStateAnalysis.Utilities.RooFitTools as rft
import templates

def ws_importer(ws):
    # Work around the limitation reserved word limitation affecting
    # RooWorkspace::import
    method = getattr(ws, 'import')
    return method

def build_model(workspace, init_vals, fit_ss_fail=True, fit_ss_pass=True):
    # Build the fit model into the workspace.  Assumes the existence of the
    # following templates:
    # 1) ztt pass/fail, OS/SS
    # 1) zttfake pass/fail, OS/SS
    # 2) wjets pass/fail, OS/SS
    # 3) qcd pass/fail, OS/SS
    # 4) Zll pass/fail, OS/SS
    # 5) ttbar pass/fail, OS/SS
    #
    # Each PDF should have the following name:
    # pdf_[name]_[os/ss]_[pass/fail]_[fitVar]
    #
    # The normalization of each pdf is named
    # n_[name]_[os/ss/all]_[pass/fail]
    #
    # The init_vals dictionary can be used to specify initial values
    # for the normalizations.

    ws = workspace
    importer = ws_importer(ws)

    # ##############################################################################
    # Extrapolating from the OS to SS regions
    # ##############################################################################
    ws.factory("qcd_os_ss_ratio_pass_meas[1.23]")
    ws.factory("wjets_os_ss_ratio_pass_meas[2.07]")
    ws.factory("zjetsfakes_os_ss_ratio_pass_meas[2.98]") # in MC
    #ws.factory("zll_os_ss_ratio_pass_meas[1.5]") # in MC
    ws.factory("ttbar_os_ss_ratio_pass_meas[5.97]") # in MC

    ws.factory("qcd_os_ss_ratio_pass_nuis[1.0, 0.0, 5.0]")
    ws.factory("wjets_os_ss_ratio_pass_nuis[1.0, 0.0, 5.0]")
    ws.factory("zjetsfakes_os_ss_ratio_pass_nuis[1.0, 0.0, 5.0]")
    #ws.factory("zll_os_ss_ratio_pass_nuis[1.0, 0.0, 5.0]")
    ws.factory("ttbar_os_ss_ratio_pass_nuis[1.0, 0.0, 5.0]")

    ws.factory("expr::qcd_os_ss_ratio_pass("
               "'@0*@1', {qcd_os_ss_ratio_pass_meas, qcd_os_ss_ratio_pass_nuis})")

    ws.factory("expr::wjets_os_ss_ratio_pass("
               "'@0*@1', {wjets_os_ss_ratio_pass_meas, wjets_os_ss_ratio_pass_nuis})")

    ws.factory("expr::zjetsfakes_os_ss_ratio_pass("
               "'@0*@1', {zjetsfakes_os_ss_ratio_pass_meas, zjetsfakes_os_ss_ratio_pass_nuis})")

    #ws.factory("expr::zll_os_ss_ratio_pass("
               #"'@0*@1', {zll_os_ss_ratio_pass_meas, zll_os_ss_ratio_pass_nuis})")

    ws.factory("expr::ttbar_os_ss_ratio_pass("
               "'@0*@1', {ttbar_os_ss_ratio_pass_meas, ttbar_os_ss_ratio_pass_nuis})")

    # Constraints
    ws.factory("RooLognormal::qcd_os_ss_ratio_pass_con(qcd_os_ss_ratio_pass_nuis,"
               "1.0, 0.05)")
    ws.factory("RooLognormal::wjets_os_ss_ratio_pass_con(wjets_os_ss_ratio_pass_nuis,"
               "1.0, 0.05)")
    ws.factory("RooLognormal::zjetsfakes_os_ss_ratio_pass_con(zjetsfakes_os_ss_ratio_pass_nuis,"
               "1.0, 0.05)")
    #ws.factory("RooLognormal::zll_os_ss_ratio_pass_con(zll_os_ss_ratio_pass_nuis,"
               #"1.0, 0.05)")
    ws.factory("RooLognormal::ttbar_os_ss_ratio_pass_con(ttbar_os_ss_ratio_pass_nuis,"
               "1.0, 0.05)")

    ws.factory("qcd_os_ss_ratio_fail_meas[1.07]")
    ws.factory("wjets_os_ss_ratio_fail_meas[1.55]")
    ws.factory("zjetsfakes_os_ss_ratio_fail_meas[1.11]")
    #ws.factory("zll_os_ss_ratio_fail_meas[1.05]")
    ws.factory("ttbar_os_ss_ratio_fail_meas[1.46]")

    ws.factory("qcd_os_ss_ratio_fail_nuis[1.0, 0.0, 5.0]")
    ws.factory("wjets_os_ss_ratio_fail_nuis[1.0, 0.0, 5.0]")
    ws.factory("zjetsfakes_os_ss_ratio_fail_nuis[1.0, 0.0, 5.0]")
    #ws.factory("zll_os_ss_ratio_fail_nuis[1.0, 0.0, 5.0]")
    ws.factory("ttbar_os_ss_ratio_fail_nuis[1.0, 0.0, 5.0]")

    ws.factory("expr::qcd_os_ss_ratio_fail("
               "'@0*@1', {qcd_os_ss_ratio_fail_meas, qcd_os_ss_ratio_fail_nuis})")

    ws.factory("expr::wjets_os_ss_ratio_fail("
               "'@0*@1', {wjets_os_ss_ratio_fail_meas, wjets_os_ss_ratio_fail_nuis})")

    ws.factory("expr::zjetsfakes_os_ss_ratio_fail("
               "'@0*@1', {zjetsfakes_os_ss_ratio_fail_meas, zjetsfakes_os_ss_ratio_fail_nuis})")

    #ws.factory("expr::zll_os_ss_ratio_fail("
               #"'@0*@1', {zll_os_ss_ratio_fail_meas, zll_os_ss_ratio_fail_nuis})")

    ws.factory("expr::ttbar_os_ss_ratio_fail("
               "'@0*@1', {ttbar_os_ss_ratio_fail_meas, ttbar_os_ss_ratio_fail_nuis})")

    # Constraints
    ws.factory("RooLognormal::qcd_os_ss_ratio_fail_con(qcd_os_ss_ratio_fail_nuis,"
               "1.0, 0.05)")
    ws.factory("RooLognormal::wjets_os_ss_ratio_fail_con(wjets_os_ss_ratio_fail_nuis,"
               "1.0, 0.05)")
    ws.factory("RooLognormal::zjetsfakes_os_ss_ratio_fail_con(zjetsfakes_os_ss_ratio_fail_nuis,"
               "1.0, 0.15)")
    #ws.factory("RooLognormal::zll_os_ss_ratio_fail_con(zll_os_ss_ratio_fail_nuis,"
               #"1.0, 0.05)")
    ws.factory("RooLognormal::ttbar_os_ss_ratio_fail_con(ttbar_os_ss_ratio_fail_nuis,"
               "1.0, 0.05)")

    # ##############################################################################
    # The quantities of interest
    # ##############################################################################

    ws.factory("tau_id_eff[0.66, 0.0, 1.0]")
    ws.factory("tau_charge_misid[0.02, 0.0, 1.0]")
    ws.factory("tau_fail_charge_misid[0.1, 0.0, 1.0]")

    # Total ZTT events in all samples
    ws.factory("prod::n_ztt_total(n_ztt_total_scale[1.0, 0, 50], n_ztt_total_init[%f])" %
               (init_vals['n_ztt_all_pass'] + init_vals['n_ztt_all_fail']) )

    ws.factory('expr::n_ztt_os_fail("@0*(1-@1)*(1-@2)",'
               '{n_ztt_total, tau_id_eff, tau_fail_charge_misid})')
    ws.factory('expr::n_ztt_ss_fail("@0*(1-@1)*@2",'
               '{n_ztt_total, tau_id_eff, tau_fail_charge_misid})')

    ws.factory('expr::n_ztt_os_pass("@0*@1*(1-@2)",'
               '{n_ztt_total, tau_id_eff, tau_charge_misid})')
    ws.factory('expr::n_ztt_ss_pass("@0*@1*@2",'
               '{n_ztt_total, tau_id_eff, tau_charge_misid})')

    # ##############################################################################
    # QCD yields in all regions
    # ##############################################################################

    ws.factory('prod::n_qcd_all_pass(n_qcd_all_pass_scale[1.0, 0, 50],'
               'n_qcd_all_pass_init[%f])' % init_vals['n_qcd_all_pass'])
    ws.factory('prod::n_qcd_all_fail(n_qcd_all_fail_scale[1.0, 0, 50],'
               'n_qcd_all_fail_init[%f])' % init_vals['n_qcd_all_fail'])

    ws.factory('expr::n_qcd_ss_pass('
              "'@0/(1 + @1)', {n_qcd_all_pass, qcd_os_ss_ratio_pass})")
    ws.factory('expr::n_qcd_os_pass('
              "'@0 - @1', {n_qcd_all_pass, n_qcd_ss_pass})")

    ws.factory('expr::n_qcd_ss_fail('
              "'@0/(1 + @1)', {n_qcd_all_fail, qcd_os_ss_ratio_fail})")
    ws.factory('expr::n_qcd_os_fail('
              "'@0 - @1', {n_qcd_all_fail, n_qcd_ss_fail})")

    # ##############################################################################
    # W yields in all regions
    # ##############################################################################

    ws.factory('prod::n_wjets_all_pass(n_wjets_all_pass_scale[1.0, 0, 50],'
               'n_wjets_all_pass_init[%f])' % init_vals['n_wjets_all_pass'])
    ws.factory('prod::n_wjets_all_fail(n_wjets_all_fail_scale[1.0, 0, 50],'
               'n_wjets_all_fail_init[%f])' % init_vals['n_wjets_all_fail'])

    ws.factory('expr::n_wjets_ss_pass('
              "'@0/(1 + @1)', {n_wjets_all_pass, wjets_os_ss_ratio_pass})")
    ws.factory('expr::n_wjets_os_pass('
              "'@0 - @1', {n_wjets_all_pass, n_wjets_ss_pass})")

    ws.factory('expr::n_wjets_ss_fail('
              "'@0/(1 + @1)', {n_wjets_all_fail, wjets_os_ss_ratio_fail})")
    ws.factory('expr::n_wjets_os_fail('
              "'@0 - @1', {n_wjets_all_fail, n_wjets_ss_fail})")

    ws.factory('n_wjets_sb_all_pass[%f, 0, 10000000]' % init_vals['n_wjets_all_pass'])
    ws.factory('n_wjets_sb_all_fail[%f, 0, 10000000]' % init_vals['n_wjets_all_fail'])

    ## Constrain using Wjets sideband
    #ws.factory('RooGaussian::n_wjets_ss_pass_con('
               #'n_wjets_ss_pass, %f, %f)' %  (
                   #init_vals['data_exp_wjets_ss_pass'] ,
                   #0.1*init_vals['data_exp_wjets_ss_pass'])
              #)

    ## Constrain using Wjets sideband
    #ws.factory('RooGaussian::n_wjets_os_pass_con('
               #'n_wjets_os_pass, %f, %f)' %  (
                   #init_vals['data_exp_wjets_os_pass'] ,
                   #0.1*init_vals['data_exp_wjets_os_pass'])
              #)

    #ws.factory('RooGaussian::n_wjets_os_fail_con('
               #'n_wjets_os_fail, %f, %f)' %  (
                   #init_vals['data_exp_wjets_os_fail'] ,
                   #0.1*init_vals['data_exp_wjets_os_fail'])
              #)

    # ##############################################################################
    # Zll yields in all regions
    # ##############################################################################

    #ws.factory('prod::n_zll_all_pass(n_zll_all_pass_scale[1.0, 0, 50],'
               #'n_zll_all_pass_init[%f])'% init_vals['n_zll_all_pass'])
    #ws.factory('prod::n_zll_all_fail(n_zll_all_fail_scale[1.0, 0, 50],'
               #'n_zll_all_fail_init[%f])'% init_vals['n_zll_all_fail'])

    #ws.factory('expr::n_zll_ss_pass('
              #"'@0/(1 + @1)', {n_zll_all_pass, zll_os_ss_ratio_pass})")
    #ws.factory('expr::n_zll_os_pass('
              #"'@0 - @1', {n_zll_all_pass, n_zll_ss_pass})")

    #ws.factory('expr::n_zll_ss_fail('
              #"'@0/(1 + @1)', {n_zll_all_fail, zll_os_ss_ratio_fail})")
    #ws.factory('expr::n_zll_os_fail('
              #"'@0 - @1', {n_zll_all_fail, n_zll_ss_fail})")

    ## Constraint
    #ws.factory('RooGaussian::n_zll_all_pass_con(n_zll_all_pass_scale, 1.0, 0.1)')
    #ws.factory('RooGaussian::n_zll_all_fail_con(n_zll_all_fail_scale, 1, 0.1)')

    # ##############################################################################
    # Ztt fakes yields in all regions
    # ##############################################################################

    ws.factory('prod::n_zjetsfakes_all_pass(n_zjetsfakes_all_pass_scale[1.0, 0, 50],'
               'n_zjetsfakes_pass_init[%f])' % init_vals['n_zjetsfakes_all_pass'])

    ws.factory('prod::n_zjetsfakes_all_fail(n_zjetsfakes_all_fail_scale[1.0, 0, 50],'
               'n_zjetsfakes_fail_init[%f])' % init_vals['n_zjetsfakes_all_fail'])

    ws.factory('expr::n_zjetsfakes_ss_pass('
              "'@0/(1 + @1)', {n_zjetsfakes_all_pass, zjetsfakes_os_ss_ratio_pass})")
    ws.factory('expr::n_zjetsfakes_os_pass('
              "'@0 - @1', {n_zjetsfakes_all_pass, n_zjetsfakes_ss_pass})")

    ws.factory('expr::n_zjetsfakes_ss_fail('
              "'@0/(1 + @1)', {n_zjetsfakes_all_fail, zjetsfakes_os_ss_ratio_fail})")
    ws.factory('expr::n_zjetsfakes_os_fail('
              "'@0 - @1', {n_zjetsfakes_all_fail, n_zjetsfakes_ss_fail})")

    # Constraint
    ws.factory('RooGaussian::n_zjetsfakes_all_pass_con(n_zjetsfakes_all_pass_scale, 1., 0.1)')
    ws.factory('RooGaussian::n_zjetsfakes_all_fail_con(n_zjetsfakes_all_fail_scale, 1., 0.1)')

    # This changes result dramatically!
    #ws.factory('RooGaussian::n_zjetsfakes_all_pass_con(n_zjetsfakes_all_pass_scale, n_ztt_total_scale, 0.04)')
    #ws.factory('RooGaussian::n_zjetsfakes_all_fail_con(n_zjetsfakes_all_fail_scale, n_ztt_total_scale, 0.04)')

    # ##############################################################################
    # ttbar yields
    # ##############################################################################

    ws.factory('prod::n_ttbar_all_pass(n_ttbar_all_pass_scale[1.0, 0, 50],'
               'n_ttbar_all_pass_init[%f])' % init_vals['n_ttbar_all_pass'])
    ws.factory('prod::n_ttbar_all_fail(n_ttbar_all_fail_scale[1.0, 0, 50],'
               'n_ttbar_all_fail_init[%f])' % init_vals['n_ttbar_all_fail'])

    ws.factory('expr::n_ttbar_ss_pass('
              "'@0/(1 + @1)', {n_ttbar_all_pass, ttbar_os_ss_ratio_pass})")
    ws.factory('expr::n_ttbar_os_pass('
              "'@0 - @1', {n_ttbar_all_pass, n_ttbar_ss_pass})")

    ws.factory('expr::n_ttbar_ss_fail('
              "'@0/(1 + @1)', {n_ttbar_all_fail, ttbar_os_ss_ratio_fail})")
    ws.factory('expr::n_ttbar_os_fail('
              "'@0 - @1', {n_ttbar_all_fail, n_ttbar_ss_fail})")

    # Constraint
    ws.factory('RooGaussian::n_ttbar_all_pass_con(n_ttbar_all_pass_scale, 1, 0.1)')
    ws.factory('RooGaussian::n_ttbar_all_fail_con(n_ttbar_all_fail_scale, 1, 0.1)')

    # ##############################################################################
    # Total yield in each region
    # ##############################################################################

    for region in templates.regions:
        yield_sum_list = []
        for sample in ['ztt', 'qcd', 'wjets', 'ttbar', 'zjetsfakes']:
            yield_num = 'n_%s_%s' % (sample, region)
            yield_sum_list.append(yield_num)
        ws.factory('sum::n_all_%s(%s)' % (region, ','.join(yield_sum_list)))

    # ##############################################################################
    # build composite PDFs
    # ##############################################################################
    all_vars = ws.set('all_vars')

    for var in rft.iter_collection(all_vars):
        for region in templates.regions:
            pdf_product_list = []
            # SUM::name(f1*pdf1,f2*pdf2,f3*pdf3)
            for sample in ['ztt', 'qcd', 'wjets', 'ttbar', 'zjetsfakes']:
                yield_var_name = 'n_%s_%s' % (sample, region)
                pdf_name = 'pdf_%s_%s_%s' % (sample, region, var.GetName())
                pdf_product_list.append("%s*%s" % (yield_var_name, pdf_name))
            # Build the PDF
            pdf_name = 'pdf_all_%s_%s' % (region, var.GetName())
            ws.factory("SUM::%s(%s)" % (pdf_name, ",".join(pdf_product_list)))
            # Build pseudo data
            pdf_to_generate = ws.pdf(pdf_name)
            pseudo_data = pdf_to_generate.generate(
                ROOT.RooArgSet(var), int(init_vals['n_data_%s' % region]))
            pseudo_data.SetName('pseudodata_%s_%s' % (region, var.GetName()))
            importer(pseudo_data)

    # ##############################################################################
    # Create simultaneous PDFs
    # ##############################################################################
    # SIMUL::name(cat,a=pdf1,b=pdf2]
    # -- Create simultaneous p.d.f index category cat.
    # Make pdf1 to state a, pdf2 to state b
    for var in rft.iter_collection(all_vars):
        category_pdf_list = []
        for region in templates.regions:
            if not fit_ss_fail and 'ss_fail' in region:
                print "Skipping SS fail region in SimPDF builder"
                continue
            category = '%s_%s' % (region, var.GetName())
            pdf_name = 'pdf_all_%s_%s' % (region, var.GetName())
            category_pdf_list.append("%s=%s" % (category, pdf_name))
        ws.factory('SIMUL::model_%s(categories_%s, %s)' %
                   (var.GetName(), var.GetName(), ','.join(category_pdf_list)))

    # ##############################################################################
    # Set any uniffted nuisances constant
    # ##############################################################################
    if not fit_ss_fail:
        ws.var('tau_fail_charge_misid').setVal(0.0)
        ws.var('tau_fail_charge_misid').setConstant(True)
        for var in rft.iter_collection(ws.allVars()):
            if 'os_ss_ratio_fail_nuis' in var.GetName():
                print "Disabling fit of", var.GetName()
                var.setConstant(True)

    if not fit_ss_pass:
        ws.var('tau_charge_misid').setVal(0.0)
        ws.var('tau_charge_misid').setConstant(True)
        for var in rft.iter_collection(ws.allVars()):
            if 'os_ss_ratio_pass_nuis' in var.GetName():
                print "Disabling fit of", var.GetName()
                var.setConstant(True)

    # ##############################################################################
    # Explicitly set initial values constant
    # ##############################################################################
    for var in rft.iter_collection(ws.allVars()):
        if '_init' in var.GetName():
            print "Setting", var.GetName(), "constant"
            var.setConstant(True)


    # ##############################################################################
    # Create model PDF with nuisance constraints
    # ##############################################################################

    # Get all the constraints
    con_pdf = []
    for pdf in rft.iter_collection(ws.allPdfs()):
        if '_con' in pdf.GetName():
            if not fit_ss_fail and 'os_ss_ratio_fail' in pdf.GetName():
                continue
            if not fit_ss_pass and 'os_ss_ratio_pass' in pdf.GetName():
                continue
            print "Adding constraint PDF:", pdf.GetName()
            con_pdf.append(pdf.GetName())

    ws.factory("PROD::constraints(%s)" % ",".join(con_pdf))

if __name__ == "__main__":
    ws = ROOT.RooWorkspace("workspace")
    templates.build_fit_vars(ws)
    templates.build_templates(ws)
    build_model(ws, templates.get_initial_sizes())
    ws.Print("v")
    ws.pdf('n_wjets_os_fail_con').printCompactTree()
