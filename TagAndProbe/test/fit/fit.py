import ROOT
import sys
import itertools
import templates
import model
import FinalStateAnalysis.Utilities.RooFitTools as rft
import FinalStateAnalysis.Utilities.styling as styling
import math

ROOT.gROOT.SetBatch(True)

ws = ROOT.RooWorkspace("workspace")

fit_ss_fail = False
fit_ss_pass = False

templates.build_fit_vars(ws)
templates.build_templates(ws)
model.build_model(
    ws,
    templates.get_initial_sizes(
        fit_fail_ss = fit_ss_fail, fit_pass_ss = fit_ss_pass),
    fit_ss_fail, fit_ss_pass)

fit_vars = ws.set('fit_vars')
all_vars = ws.set('all_vars')
#nonfit_vars = all_vars.clone('nonfit_vars')
nonfit_vars = all_vars
nonfit_vars.remove(fit_vars)

ROOT.RooMsgService.instance().getStream(1).removeTopic(ROOT.RooFit.Plotting)

nlls = []

data_sets = {}
for var in itertools.chain(
    rft.iter_collection(fit_vars), rft.iter_collection(nonfit_vars)):
    for region in templates.regions:
        realdata = ws.data('data_%s_%s' % (region, var.GetName()))
        pseudodata = ws.data('pseudodata_%s_%s' % (region, var.GetName()))
        binned_pseudodata = realdata.Clone()
        binned_pseudodata.reset()
        binned_pseudodata.add(pseudodata)
        # Select data type
        data = binned_pseudodata
        #data = realdata
        data_sets[(var.GetName(), region)] = data

for var in rft.iter_collection(fit_vars):
    for region in templates.regions:
        if not fit_ss_fail and 'ss_fail' in region:
            continue
        if not fit_ss_pass and 'ss_pass' in region:
            continue
        pdf = ws.pdf('pdf_all_%s_%s' % (region, var.GetName()))
        data = data_sets[(var.GetName(), region)]
        options = ROOT.RooLinkedList()
        if True or not nlls:
            options.Add(ROOT.RooFit.ExternalConstraints(
                ROOT.RooArgSet(ws.pdf('constraints'))))
        options.Add(ROOT.RooFit.Extended(True))
        nll = pdf.createNLL(data, options)
        nlls.append(nll)

all_nll = ROOT.RooAddition("nll", "nll", ROOT.RooArgSet(*nlls))

minuit = ROOT.RooMinuit(all_nll)
minuit.setErrorLevel(1);
minuit.setNoWarn();
minuit.setPrintEvalErrors(0);
minuit.setPrintLevel(0);
minuit.setWarnLevel(3);
minuit.migrad();
minuit.hesse();
minuit.hesse();
result = minuit.save()
result.Print("v")

canvas = ROOT.TCanvas("asdf", "adsf", 800, 600)

stack = ['*_ztt_*', '*qcd*', '*wjets*',  '*_zjetsfakes_*', '*ttbar*',]
stack_names = ['Z#tau#tau', 'QCD', 'W+jets',  'Z+jets (fake)', 'tt+jets',]
color_names = [
    'ewk_yellow',
    'ewk_orange',
    'ewk_red',
    'ewk_purple',
    'green_blue',
    'blue'
]

colors = [styling.colors[x].code for x in color_names]

stack_args, legend_maker = rft.make_stack_arguments(
    *zip(stack, colors, stack_names))

for region in templates.regions:
    for type, var_collection in [('FITTED', fit_vars),
                                 ('CONTROL', nonfit_vars) ]:
        for var in rft.iter_collection(var_collection):
            if not fit_ss_fail and 'ss_fail' in region:
                type = 'CONTROL'

            frame = var.frame()
            model = ws.pdf('pdf_all_%s_%s' % (region, var.GetName()))
            #data = ws.data('data_%s_%s' % (region, var.GetName()))
            data = data_sets[(var.GetName(), region)]
            normalization = ws.arg('n_all_%s' % region).getVal()
            data.plotOn(frame)

            for stack_arg in stack_args:
                model.plotOn(
                    frame,
                    ROOT.RooFit.Normalization(normalization,
                                              ROOT.RooAbsReal.NumEvent),
                    *stack_arg
                )

            data.plotOn(frame)

            legend = ROOT.TLegend(0.65, 0.65, 0.86, 0.86, "", "brNDC")
            legend.SetFillStyle(0)

            legend_maker(frame, legend)

            frame.Draw()
            frame.SetMaximum(1.5*frame.GetMaximum())
            frame.GetYaxis().SetTitle("")
            title = "Fitted yields in %s region with tau ID = %s " % tuple(
                region.upper().split('_'))
            title += type
            frame.SetTitle(title)
            legend.Draw()
            canvas.SaveAs("final_fit_" + var.GetName() + "_" + region + "_result.pdf")
            canvas.SaveAs("final_fit_" + var.GetName() + "_" + region + "_result.png")
            canvas.SetLogy(True)
            canvas.SaveAs("final_fit_" + var.GetName() + "_" + region + "_result_log.pdf")
            canvas.SaveAs("final_fit_" + var.GetName() + "_" + region + "_result_log.png")
            canvas.SetLogy(False)

#for region in templates.regions:
    #for type, var_collection in [('FITTED', fit_vars),
                                 #('CONTROL', nonfit_vars) ]:
    ##for type, var_collection in [('FITTED', all_vars), ]:
        #for var in rft.iter_collection(var_collection):
            #counter += 1
            ##print region.upper()
            ##print region, var.GetTitle(), counter, len(templates.regions)*all_vars.getSize()-2
            #if not fit_ss_fail and 'ss_fail' in region:
                #continue
                #type = 'CONTROL'
            #categories = ws.cat("categories_%s" % var.GetName())
            #frame = var.frame()
            #model = ws.pdf('model_%s' % var.GetName())
            #data = ws.data('data_combo_%s' % var.GetName())
            #data.plotOn(
                #frame,
                #ROOT.RooFit.Cut("categories_%s==categories_%s::%s_%s" % (
                    #var.GetName(), var.GetName(),
                    #region, var.GetName()))
            #)

            #for stack_arg in stack_args:
                ##continue
                #model.plotOn(
                    #frame,
                    #ROOT.RooFit.Slice(categories,
                                      #"%s_%s" % (region, var.GetName())),
                    #ROOT.RooFit.ProjWData(
                        #ROOT.RooArgSet("%s_%s" % (region, var.GetName())), data),
                    #*stack_arg
                #)

            #data.plotOn(
                #frame,
                #ROOT.RooFit.Cut("categories_%s==categories_%s::%s_%s" % (
                    #var.GetName(), var.GetName(),
                    #region, var.GetName()))
            #)

            #legend = ROOT.TLegend(0.65, 0.65, 0.86, 0.86, "", "brNDC")
            #legend.SetFillStyle(0)

            #legend_maker(frame, legend)

            #frame.Draw()
            #frame.SetMaximum(1.5*frame.GetMaximum())
            #frame.GetYaxis().SetTitle("")
            #title = "Fitted yields in %s region with tau ID = %s " % tuple(
                #region.upper().split('_'))
            #title += type
            #frame.SetTitle(title)
            #legend.Draw()
            #canvas.SaveAs("final_fit_" + var.GetName() + "_" + region + "_result.pdf")
            #canvas.SetLogy(True)
            #canvas.SaveAs("final_fit_" + var.GetName() + "_" + region + "_result_log.pdf")
            #canvas.SetLogy(False)



# Get truth
pass_os =  templates.get_th1('zjets', 'sigPassOS/realTau', 'AbsTauEta').Integral()
fail_os =  templates.get_th1('zjets', 'sigFailOS/realTau', 'AbsTauEta').Integral()
pass_ss =  templates.get_th1('zjets', 'sigPassSS/realTau', 'AbsTauEta').Integral()

mc_eff = (pass_os/(pass_os + fail_os))
mc_eff_err = math.sqrt(pass_os*(1 - mc_eff))/(pass_os + fail_os)
print "MC eff:", "%0.4f +/- %0.4f" % (mc_eff , mc_eff_err)
print "Measured eff:", "%0.4f" % ws.var('tau_id_eff').getVal(), "+/-", "%0.4f" % ws.var('tau_id_eff').getError()
print "MC charge:", "%0.4f" % (pass_ss/(pass_os + pass_ss))
print "Measured charge:", "%0.4f" % ws.var('tau_charge_misid').getVal(), "+/-", "%0.4f" % ws.var('tau_charge_misid').getError()

ws.var('tau_id_eff').Print()
ws.var('tau_charge_misid').Print()

# Stupid way
pass_ss_data =  templates.get_th1('data', 'sigPassSS', 'AbsTauEta').Integral()
pass_ss_fit_qcd = ws.arg('n_qcd_ss_pass').getVal()
pass_ss_fit_wjets = ws.arg('n_wjets_ss_pass').getVal()
#pass_ss_fit_zll = ws.arg('n_zll_ss_pass').getVal()
pass_ss_fit_zjetsfakes = ws.arg('n_zjetsfakes_ss_pass').getVal()
#total_bkg = pass_ss_fit_qcd + pass_ss_fit_wjets + pass_ss_fit_zll + pass_ss_fit_zjetsfakes
total_bkg = pass_ss_fit_qcd + pass_ss_fit_wjets + pass_ss_fit_zjetsfakes

print "SS pass data:", pass_ss_data
print "SS pass qcd:", pass_ss_fit_qcd
print "SS pass wjets:", pass_ss_fit_wjets
#print "SS pass zll:", pass_ss_fit_zll
print "SS pass zjetsfakes:", pass_ss_fit_zjetsfakes
print "SS pass bkg:", total_bkg
pass_ss_ztt = pass_ss_data - total_bkg
print "SS pass taus:", pass_ss_ztt

pass_os_ztt = ws.arg('n_ztt_os_pass').getVal()
print "OS pass taus:", pass_os_ztt
print "Charge mis-ID:", pass_ss_ztt/(pass_os_ztt + pass_ss_ztt)
