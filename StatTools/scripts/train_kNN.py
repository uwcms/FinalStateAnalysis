#! /bin/env python

from RecoLuminosity.LumiDB import argparse
import ROOT
import rootpy.plotting as plotting
import sys
import os
from FinalStateAnalysis.MetaData.data_views import extract_sample, read_lumi
from FinalStateAnalysis.StatTools.RooFunctorFromWS import FunctorFromMVA
import logging
from array import array
from rootpy.utils import asrootpy
from progressbar import ETA, ProgressBar, FormatLabel, Bar
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--files', nargs='+')
parser.add_argument('--variables', nargs='+')
parser.add_argument('--outputfile', required=True)
parser.add_argument('--tree', required=True, help='Path to tree')
parser.add_argument('--cut', required=True, help='branch name of id/iso WP')
parser.add_argument('--neighbors', type=int, help='numer of heighbors to use', default=100)
parser.add_argument('--makePlots', type=int, help='skip the plotting step to be faster', default=1)
parser.add_argument('--forceLumi', type=float, help='force the data lumi value, helpful when running on MC only', default=0)
parser.add_argument('--splitter', type=str, help='function to split the sample, based on the entry number', default='')


args = parser.parse_args()

log = logging.getLogger("train_kNN")
log.info("train_kNN:")

jobid = os.environ['jobid']
def get_lumi(filename):
    sample_name = extract_sample(filename)
    lumi        = read_lumi( 
        os.path.join(
            'inputs',
            jobid,
            sample_name+".lumicalc.sum"
        ) 
    )
    return lumi

def round_to_ints(histo):
    new = histo.Clone()
    new.Reset()
    for bin in range(histo.GetNbinsX()+1):
        nentries = ROOT.TMath.Nint(histo.GetBinContent(bin)) \
                   if histo.GetBinContent(bin) >= 0 else 0
        centerx  = histo.GetXaxis().GetBinCenter(bin)
        for _ in range(nentries):
            new.Fill(centerx)
    return new



data_files = filter(lambda x: 'data_' in x, args.files)
mc_files   = filter(lambda x: x not in data_files, args.files)
#zz_file     = filter(lambda x: 'ZZ'    in x, args.files)[0]
#wz_file     = filter(lambda x: 'WZ'    in x, args.files)[0]

output_file = args.outputfile
input_tree  = args.tree #'wjets/pt10/muonInfo'
selection   = args.cut #'h2taucuts'
out_tfile   = ROOT.TFile.Open(output_file, 'recreate')
cut_pass    = ROOT.TCut('%s==1' % selection)
cut_fail    = ROOT.TCut('%s==0' % selection)
splitter    = eval('lambda x: '+args.splitter) if args.splitter else None

######################################
## Getting luminosities
######################################

data_tree = None
data_lumi   = 0.
mc_multiplicative = -1
if data_files:
    log.info('Getting data Tree')
    data_tree   = ROOT.TChain(input_tree)
    data_lumi   = 0.
    for i in data_files:
        data_lumi += get_lumi(i)
        data_tree.Add(i)
    num_pass    = data_tree.GetEntries(cut_pass.GetTitle())
    num_fail    = data_tree.GetEntries(cut_fail.GetTitle())
    log.info("found %i input files for a total lumi: %f total passing events: %i. total failing events: %i" % (len(data_files), data_lumi, num_pass, num_fail) )

if args.forceLumi:
    data_lumi = args.forceLumi
    log.info("forcing total lumi to %f", data_lumi )
    mc_multiplicative = 1

mc_trees = []
for mc_file in mc_files:
    sample_name = extract_sample(mc_file)
    log.info('getting %s dataset...' % sample_name)
    mc_tree   = ROOT.TFile.Open(mc_file).Get(input_tree)
    mc_lumi   = get_lumi(mc_file)
    mc_factor = mc_multiplicative*(data_lumi / mc_lumi) \
                if data_lumi <> -1 else 1.
    log.info('   Events are going to be scaled by %f' % mc_factor)
    mc_trees.append( (sample_name, mc_tree, mc_factor) )


out_tfile.cd()

######################################
## Loading training Tree
######################################

training_vars   = args.variables+[args.cut,'weight']
training_NTuple = ROOT.TNtuple('training_ntuple', 'training_ntuple', ':'.join(training_vars) )

#Copy the data tree as it is
if data_tree:
    log.info('copying data events into training tree')
    for i, row in enumerate(data_tree):
        if splitter and not splitter(i):
            #If there is a splitter and it returns False, skip the event
            continue
        training_NTuple.Fill(
            array('f',
                  [ getattr(row, var) for var in training_vars ]
              )
        )

#Copy MC Trees but scale each event by the proper lumi factor
for sample_name, mc_tree, mc_factor in mc_trees:
    log.info('copying %s events into training tree' % sample_name)
    for i, row in enumerate(mc_tree):
        if splitter and not splitter(i):
            #If there is a splitter and it returns False, skip the event
            continue
        to_fill = array('f',
                        [ getattr(row, var) for var in training_vars ]
                    )
        #scale by lumi factor
        to_fill[-1] *= mc_factor
        training_NTuple.Fill(to_fill)

num_tot  = training_NTuple.GetEntries()
num_pass = training_NTuple.GetEntries(cut_pass.GetTitle())
num_fail = training_NTuple.GetEntries(cut_fail.GetTitle())
log.info("# Events: %i, # Passing the cut: %i, # Failing: %i" % (num_tot, num_pass, num_fail))

############################################################################
## MVA Settings, training, move of the xml file
############################################################################

#Start TMVA and create factory
TMVA_tools = ROOT.TMVA.Tools.Instance()
log.info("creating TMVA factory")
factory    = ROOT.TMVA.Factory(
    "TMVAClassification", 
    out_tfile, 
    "!V:!Silent:Color:DrawProgressBar:Transformations=I" ) #"!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D"

#Add variables (maybe move to args)
for var in args.variables:
    log.info('adding %s as variable', var)
    factory.AddVariable( var   , 'F' )
    #factory->AddVariable( "m2JetPt", 'F' );

factory.SetWeightExpression( "weight" )

factory.SetInputTrees(training_NTuple, cut_pass, cut_fail)
factory.PrepareTrainingAndTestTree( ROOT.TCut(''), ROOT.TCut(''),
                                    "nTrain_Signal=%i:nTrain_Background=%i:SplitMode=Random:NormMode=None:!V" % (num_pass, num_fail) );
factory.BookMethod( 
    ROOT.TMVA.Types.kKNN, "KNN", 
    "H:nkNN=%i:ScaleFrac=0.8:SigmaFact=1.0:Kernel=Gaus:UseKernel=F:UseWeight=T" % args.neighbors)

log.info("Training kNN!...")
factory.TrainAllMethods()
log.info("Training Done!")


xml_name = os.path.join(os.getcwd(),"weights/TMVAClassification_KNN.weights.xml")
target   = os.path.join(os.getcwd(),output_file.replace('.root','.weights.xml'))
cmd      = 'mv %s %s' % (xml_name, target)
log.info(cmd)
os.system( cmd )

#############################################
##  Reads back and produces control plots
#############################################

hist_maps = {}
for var in args.variables:
    if 'pt' in var.lower():
        hist_maps[var] = {
            'estimate'     : plotting.Hist([10,12,15,20,25,30,35,40,45,50,60,70,100,150,200]), #plotting.Hist(100, 0, 200),
            'estimate_all' : plotting.Hist([10,12,15,20,25,30,35,40,45,50,60,70,100,150,200]), #plotting.Hist(100, 0, 200),
            'pass'     : plotting.Hist([10,12,15,20,25,30,35,40,45,50,60,70,100,150,200]),
            'all'      : plotting.Hist([10,12,15,20,25,30,35,40,45,50,60,70,100,150,200]),
        }
    elif 'jets' in var.lower() or 'njet' in var.lower():
        hist_maps[var] = {
            'estimate'     : plotting.Hist(12, 0, 12),
            'estimate_all' : plotting.Hist(12, 0, 12),
            'pass'         : plotting.Hist(12, 0, 12),
            'all'          : plotting.Hist(12, 0, 12),
        }
    else:
        hist_maps[var] = {
            'estimate'     : plotting.Hist(100, 0, 200),
            'estimate_all' : plotting.Hist(100, 0, 200),
            'pass'         : plotting.Hist(100, 0, 200),
            'all'          : plotting.Hist(100, 0, 200),
        }

if args.makePlots:
    log.info("making plots")
    functor = FunctorFromMVA('kNN', target, *args.variables)

    progress= ProgressBar(
        widgets = [
            ETA(),
            Bar('>')],
        maxval = training_NTuple.GetEntries() ).start()


    for i, row in enumerate(training_NTuple):
        progress.update(i+1)
        var_d  = dict([(v, getattr(row, v)) for v in args.variables])
        mva    = functor(**var_d)
        weight = row.weight
        cut    = bool( getattr(row, args.cut) )
        if weight > 0:
            print cut, mva, weight
            #assert(int(cut) == mva)
        else:
            print cut, mva, weight
        for var in args.variables:
            value = var_d[var]
            if weight > 0: #fill only data-like events
                hist_maps[var]['estimate'].Fill(value, weight*mva)
                hist_maps[var]['estimate_all'].Fill(value, weight)
            hist_maps[var]['all'].Fill(value, weight)
            if cut:
                hist_maps[var]['pass'].Fill(value, weight)


    canvas = plotting.Canvas(name='adsf', title='asdf')
    canvas.SetLogy(True)
    for var in args.variables:

        for key in ['pass', 'all']: #hist_maps[var].iterkeys():
            hist_maps[var][key] = round_to_ints(hist_maps[var][key])

        eff = asrootpy( ROOT.TGraphAsymmErrors( hist_maps[var]['pass'], hist_maps[var]['all']) )
        eff.markerstyle = 20
        eff.SetName('efficiency_%s' % var)
        estimate = hist_maps[var]['estimate'].Clone() #avoid getting divided
        estimate.Divide(hist_maps[var]['estimate_all'])
        estimate.SetName('estimate_%s' % var)
        estimate.linecolor = ROOT.kBlue 
        estimate.linewidth = 2
        estimate.fillstyle = 0
        estimate.drawstyle = 'hist'
        
        estimate.Draw()
        eff.Draw('P same')
        canvas.Update()
        canvas.SetLogy(True)
        canvas.SaveAs( output_file.replace('.root', '.%s.png' % var ) )
        
        eff.Write()
        estimate.Write()
        for key, obj in hist_maps[var].iteritems():
            obj.SetName( '%s_%s' % (var, key) )
            obj.Write()

training_NTuple.Write()

out_tfile.Close()
