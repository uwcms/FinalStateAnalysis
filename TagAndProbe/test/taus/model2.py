import ROOT
from collections import defaultdict
import FinalStateAnalysis.Utilities.RooFitTools as rft
import templates

def ws_importer(ws):
    # Work around the limitation reserved word limitation affecting
    # RooWorkspace::import
    method = getattr(ws, 'import')
    return method

def build_model(workspace, init_vals):
    ws = workspace
    importer = ws_importer(ws)

    ws.factory("qcd_os_ss_ratio_pass_meas[1.11]")
    ws.factory("wjets_os_ss_ratio_pass_meas[2.65]")
    ws.factory("zjetsfakes_os_ss_ratio_pass_meas[2.85]") # in MC
    ws.factory("ttbar_os_ss_ratio_pass_meas[4.65]") # in MC

    ws.factory("qcd_os_ss_ratio_pass_nuis[1.0, 0.0, 5.0]")
    ws.factory("wjets_os_ss_ratio_pass_nuis[1.0, 0.0, 5.0]")
    ws.factory("zjetsfakes_os_ss_ratio_pass_nuis[1.0, 0.0, 5.0]")
    ws.factory("ttbar_os_ss_ratio_pass_nuis[1.0, 0.0, 5.0]")

    ws.factory("expr::qcd_os_ss_ratio_pass("
               "'@0*@1', {qcd_os_ss_ratio_pass_meas, qcd_os_ss_ratio_pass_nuis})")

    ws.factory("expr::wjets_os_ss_ratio_pass("
               "'@0*@1', {wjets_os_ss_ratio_pass_meas, wjets_os_ss_ratio_pass_nuis})")

    ws.factory("expr::zjetsfakes_os_ss_ratio_pass("
               "'@0*@1', {zjetsfakes_os_ss_ratio_pass_meas, zjetsfakes_os_ss_ratio_pass_nuis})")

    ws.factory("expr::ttbar_os_ss_ratio_pass("
               "'@0*@1', {ttbar_os_ss_ratio_pass_meas, ttbar_os_ss_ratio_pass_nuis})")

    ws.factory("RooGaussian::qcd_os_ss_ratio_pass_con(qcd_os_ss_ratio_pass_nuis,"
               "1.0, 0.06)")
    ws.factory("RooGaussian::wjets_os_ss_ratio_pass_con(wjets_os_ss_ratio_pass_nuis,"
               "1.0, 0.03)")
    ws.factory("RooGaussian::zjetsfakes_os_ss_ratio_pass_con(zjetsfakes_os_ss_ratio_pass_nuis,"
               "1.0, 0.05)")
    ws.factory("RooGaussian::ttbar_os_ss_ratio_pass_con(ttbar_os_ss_ratio_pass_nuis,"
               "1.0, 0.14)")

    # ##############################################################################
    # The quantities of interest
    # ##############################################################################

    ws.factory("tau_id_eff[0.70, 0.0, 1.0]")
    ws.factory("tau_charge_misid[0.01, 0.0, 1.0]")

    # Total ZTT events in all samples
    ws.factory("prod::n_ztt_total(n_ztt_total_scale[1.0, 0, 50], n_ztt_total_init[%f])" %
               (init_vals['n_ztt_all_pass'] + init_vals['n_ztt_os_fail']) )

    ws.factory('expr::n_ztt_os_fail("@0*(1-@1)", {n_ztt_total, tau_id_eff})')

    ws.factory('expr::n_ztt_os_pass("@0*@1*(1-@2)",'
               '{n_ztt_total, tau_id_eff, tau_charge_misid})')

    ws.factory('expr::n_ztt_ss_pass("@0*@1*@2",'
               '{n_ztt_total, tau_id_eff, tau_charge_misid})')

    # ##############################################################################
    # QCD yields in all regions
    # ##############################################################################

    ws.factory('prod::n_qcd_all_pass(n_qcd_all_pass_scale[1.0, 0, 50],'
               'n_qcd_all_pass_init[%f])' % init_vals['n_qcd_all_pass'])

    ws.factory('expr::n_qcd_ss_pass('
              "'@0/(1 + @1)', {n_qcd_all_pass, qcd_os_ss_ratio_pass})")
    ws.factory('expr::n_qcd_os_pass('
              "'@0 - @1', {n_qcd_all_pass, n_qcd_ss_pass})")

    ws.factory('prod::n_qcd_os_fail(n_qcd_os_fail_scale[1.0, 0, 50],'
               'n_qcd_os_fail_init[%f])' % init_vals['n_qcd_os_fail'])

    # ##############################################################################
    # W yields in all regions
    # ##############################################################################

    ws.factory('prod::n_wjets_all_pass(n_wjets_all_pass_scale[1.0, 0, 50],'
               'n_wjets_all_pass_init[%f])' % init_vals['n_wjets_all_pass'])

    ws.factory('prod::n_wjets_os_fail(n_wjets_os_fail_scale[1.0, 0, 50],'
               'n_wjets_os_fail_init[%f])' % init_vals['n_wjets_os_fail'])

    ws.factory('expr::n_wjets_ss_pass('
              "'@0/(1 + @1)', {n_wjets_all_pass, wjets_os_ss_ratio_pass})")
    ws.factory('expr::n_wjets_os_pass('
              "'@0 - @1', {n_wjets_all_pass, n_wjets_ss_pass})")

    ### Constrain using Wjets sideband
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

    ws.factory('RooGaussian::n_wjets_all_pass_con(n_wjets_all_pass_scale, 1., 0.05)')
    ws.factory('RooGaussian::n_wjets_os_fail_con(n_wjets_os_fail_scale, 1., 0.05)')

    # ##############################################################################
    # Ztt fakes yields in all regions
    # ##############################################################################

    ws.factory('prod::n_zjetsfakes_all_pass(n_zjetsfakes_all_pass_scale[1.0, 0, 50],'
               'n_zjetsfakes_pass_init[%f])' % init_vals['n_zjetsfakes_all_pass'])

    ws.factory('prod::n_zjetsfakes_os_fail(n_zjetsfakes_os_fail_scale[1.0, 0, 50],'
               'n_zjetsfakes_fail_init[%f])' % init_vals['n_zjetsfakes_os_fail'])

    ws.factory('expr::n_zjetsfakes_ss_pass('
              "'@0/(1 + @1)', {n_zjetsfakes_all_pass, zjetsfakes_os_ss_ratio_pass})")
    ws.factory('expr::n_zjetsfakes_os_pass('
              "'@0 - @1', {n_zjetsfakes_all_pass, n_zjetsfakes_ss_pass})")

    # Constraint
    ws.factory('RooGaussian::n_zjetsfakes_all_pass_con(n_zjetsfakes_all_pass_scale, 1., 0.05)')
    ws.factory('RooGaussian::n_zjetsfakes_os_fail_con(n_zjetsfakes_os_fail_scale, 1., 0.05)')

    # ##############################################################################
    # ttbar yields
    # ##############################################################################

    ws.factory('prod::n_ttbar_all_pass(n_ttbar_all_pass_scale[1.0, 0, 50],'
               'n_ttbar_all_pass_init[%f])' % init_vals['n_ttbar_all_pass'])

    ws.factory('prod::n_ttbar_os_fail(n_ttbar_os_fail_scale[1.0, 0, 50],'
               'n_ttbar_os_fail_init[%f])' % init_vals['n_ttbar_os_fail'])

    ws.factory('expr::n_ttbar_ss_pass('
              "'@0/(1 + @1)', {n_ttbar_all_pass, ttbar_os_ss_ratio_pass})")
    ws.factory('expr::n_ttbar_os_pass('
              "'@0 - @1', {n_ttbar_all_pass, n_ttbar_ss_pass})")

    # Constraint
    #ws.factory('RooGaussian::n_ttbar_all_pass_con(n_ttbar_all_pass_scale, 1, 0.086)')
    #ws.factory('RooGaussian::n_ttbar_os_fail_con(n_ttbar_os_fail_scale, 1, 0.086)')
    ws.factory('RooGaussian::n_ttbar_all_pass_con(n_ttbar_all_pass_scale, 1, 0.1)')
    ws.factory('RooGaussian::n_ttbar_os_fail_con(n_ttbar_os_fail_scale, 1, 0.1)')

    # ##############################################################################
    # Total yield in each region
    # ##############################################################################
    #
    for region in templates.regions:
        if 'ss_fail' in region:
            continue
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
            if 'ss_fail' in region:
                continue
            pdf_product_list = []
            # SUM::name(f1*pdf1,f2*pdf2,f3*pdf3)
            for sample in ['ztt', 'qcd', 'wjets', 'ttbar', 'zjetsfakes']:
                yield_var_name = 'n_%s_%s' % (sample, region)
                pdf_name = 'pdf_%s_%s_%s' % (sample, region, var.GetName())
                pdf_product_list.append("%s*%s" % (yield_var_name, pdf_name))
            # Build the PDF
            pdf_name = 'pdf_all_%s_%s' % (region, var.GetName())
            ws.factory("SUM::%s(%s)" % (pdf_name, ",".join(pdf_product_list)))

    # ##############################################################################
    # Make poisson constraint of SS pass region
    # ##############################################################################
    #ws.factory('RooPoisson::ss_pass_obs_con(n_all_ss_pass, n_data_ss_pass_obs[%f])' % init_vals['n_data_ss_pass'])

    #ws.var('tau_charge_misid').setConstant(True)

    # Get all the constraints
    con_pdf = []
    for pdf in rft.iter_collection(ws.allPdfs()):
        if '_con' in pdf.GetName():
            print "Adding constraint PDF:", pdf.GetName()
            con_pdf.append(pdf.GetName())

    ws.factory("PROD::constraints(%s)" % ",".join(con_pdf))


if __name__ == "__main__":
    ws = ROOT.RooWorkspace("workspace")
    templates.build_fit_vars(ws)
    templates.build_templates(ws)
    build_model(ws, templates.get_initial_sizes())
    ws.Print("v")
    ws.allFunctions().Print()
    ws.function("n_all_ss_pass").Print("v")
    ws.pdf('n_wjets_os_fail_con').printCompactTree()
    ws.pdf('ss_pass_obs_con').printCompactTree()
    print ws.pdf('n_wjets_os_fail_con').getNorm(ROOT.RooArgSet(ws.var('n_wjets_os_fail_scale')))
    print ws.pdf('n_wjets_os_fail_con').getVal()
