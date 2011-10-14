import ROOT
import os
import FinalStateAnalysis.TagAndProbe.datadefs as datadefs
import FinalStateAnalysis.Utilities.WeightedTFile as WeightedTFile
import FinalStateAnalysis.Utilities.AnalysisPlotter as AnalysisPlotter

ROOT.gROOT.SetBatch(True)
ROOT.gROOT.SetStyle("Plain")

samples = {}

def get_file(sample):
    return os.path.join('data', sample + '.root')

# Build our weighted objects
for sample_name, sample_longnames in datadefs.data_name_map.iteritems():
    print ">>", sample_name
    mydict = {}
    samples[sample_name] = mydict
    if isinstance(sample_longnames, basestring):
        sample_longnames = [sample_longnames]

    subsamples = {}
    mydict['subsamples'] = subsamples
    for sample_longname in sample_longnames:
        print sample_longname

        detail_dict = datadefs.datadefs[sample_longname]
        filename = get_file(sample_longname)
        # Define arguments used to build weighted tfile - default - no weighting.
        weightfile_args = { 'weight' : 1.0, 'verbose' : True }
        # For MC, we weight.
        if 'x_sec' in detail_dict:
            weightfile_args = {
                'target_lumi' : 1320,
                'xsec' : detail_dict['x_sec'],
                'skim_eff' : detail_dict['skim'],
                'event_count' : 'ohyeah/eventCount',
                'verbose' : True
            }

        wfile = WeightedTFile.WeightedTFile(filename, 'READ',
                                            **weightfile_args)
        # Make the plotter wrapper
        subsamples[sample_longname] = \
                AnalysisPlotter.AnalysisSample(wfile, sample_longname)

    mydict['sample'] =  AnalysisPlotter.AnalysisMultiSample(
        sample_name, *mydict['subsamples'].values())


print samples

canvas = ROOT.TCanvas("basdf", "aasdf", 800, 600)

plotter = AnalysisPlotter.AnalysisPlotter(
    *[sample['sample'] for sample in samples.values()])

for region in ['sigPassOS', 'sigPassSS', 'sigFailOS', 'sigFailSS',
               'qcdPassOS', 'qcdPassSS', 'qcdFailOS', 'qcdFailSS',
               'wjetsPassOS', 'wjetsPassSS', 'wjetsFailOS', 'wjetsFailSS']:
    for var in ['PZeta',  'Mvis', 'TauPt', 'MT1', 'TauDecayMode', 'cutFlow']:
        rebin = 5
        if 'cutFlow' in var or 'DecayMode' in var:
            rebin = 1
        canvas.Clear()

        def get_path(region, var):
            return os.path.join('ohyeah', region, var)

        stack =  plotter.build_stack('asdf', get_path(region, var),
                                    exclude=['data', 'vh',], rebin=rebin, show_overflows=True)

        data = plotter.get_histogram('data', get_path(region, var), rebin=rebin, show_overflows=True)

        legend = plotter.build_legend(get_path(region, var), drawopt='lf')

        stack.Draw()
        stack.GetXaxis().SetTitle(stack.GetTitle())
        stack.SetTitle(stack.GetTitle() + ' 1.32 fb^{-1}')
        stack.SetMaximum(1.1*max(stack.GetMaximum(), data.GetMaximum()))

        data.Draw('same,' + data.GetOption())
        legend.Draw()

        ROOT.gPad.SetLogy(False)
        canvas.Update()
        canvas.SaveAs(os.path.join('control_plots',
                                   '_'.join([var, region, ".pdf"])))
        canvas.SaveAs(os.path.join('control_plots',
                                   '_'.join([var, region, ".png"])))
        ROOT.gPad.SetLogy(True)
        canvas.Update()
        canvas.SaveAs(os.path.join('control_plots',
                                   '_'.join([var, region, "log", ".pdf"])))
        canvas.SaveAs(os.path.join('control_plots',
                                   '_'.join([var, region, "log", ".png"])))
