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
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--files', nargs='+')
parser.add_argument('--variables', nargs='+')
parser.add_argument('--outputfile', required=True)
parser.add_argument('--tree', required=True, help='Path to tree')
parser.add_argument('--cut', required=True, help='branch name of id/iso WP')
parser.add_argument('--neighbors', type=int, help='numer of heighbors to use', default=100)

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



data_files  = filter(lambda x: 'data_' in x, args.files)
zz_file     = filter(lambda x: 'ZZ'    in x, args.files)[0]
wz_file     = filter(lambda x: 'WZ'    in x, args.files)[0]

output_file = args.outputfile
input_tree  = args.tree #'wjets/pt10/muonInfo'
selection   = args.cut #'h2taucuts'
out_tfile   = ROOT.TFile.Open(output_file, 'recreate')
cut_pass    = ROOT.TCut('%s==1' % selection)
cut_fail    = ROOT.TCut('%s==0' % selection)

log.info('Getting data Tree')
data_tree   = ROOT.TChain(input_tree)
data_lumi   = 0.
for i in data_files:
    data_lumi += get_lumi(i)
    data_tree.Add(i)
num_pass    = data_tree.GetEntries(cut_pass.GetTitle())
num_fail    = data_tree.GetEntries(cut_fail.GetTitle())
log.info("found %i input files for a total lumi: %f total passing events: %i. total failing events: %i" % (len(data_files), data_lumi, num_pass, num_fail) )


log.info('getting ZZ dataset...')
zz_tree    = ROOT.TFile.Open(zz_file).Get(input_tree)
zz_lumi    = get_lumi(zz_file)
zz_factor  = -(data_lumi / zz_lumi)
log.info('   Events are going to be scaled by %f' % zz_factor)

log.info('getting WZ dataset...')
wz_tree    = ROOT.TFile.Open(wz_file).Get(input_tree)
wz_lumi    = get_lumi(wz_file)
wz_factor  = -(data_lumi / wz_lumi)
log.info('   Events are going to be scaled by %f' % wz_factor)

out_tfile.cd()
training_vars   = args.variables+[args.cut,'weight']
training_NTuple = ROOT.TNtuple('training_ntuple', 'training_ntuple', ':'.join(training_vars) )

#Copy the data tree as it is
log.info('copying data events into training tree')
for row in data_tree:
    training_NTuple.Fill(
        array('f',
              [ getattr(row, var) for var in training_vars ]
          )
    )

#Copy WZ and ZZ Trees but scale each event by the proper lumi factor

#WZ
log.info('copying WZ events into training tree')
for row in wz_tree:
    to_fill = array('f',
                    [ getattr(row, var) for var in training_vars ]
                )
    #scale by lumi factor
    to_fill[-1] *= wz_factor

    training_NTuple.Fill(
        to_fill
    )

#ZZ
log.info('copying ZZ events into training tree')
for row in zz_tree:
    to_fill = array('f',
                    [ getattr(row, var) for var in training_vars ]
                )
    #scale by lumi factor
    to_fill[-1] *= zz_factor

    training_NTuple.Fill(
        to_fill
    )


num_pass    = training_NTuple.GetEntries(cut_pass.GetTitle())
num_fail    = training_NTuple.GetEntries(cut_fail.GetTitle())


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


#Reads back and produces control plots
hist_maps = {}
for var in args.variables:
    hist_maps[var] = {
        'estimate' : plotting.Hist(100, 0, 200),
        'estimate_all' : plotting.Hist(100, 0, 200),
        'pass'     : plotting.Hist([10,12,15,20,25,30,35,40,45,50,60,70,100,150,200]),
        'all'      : plotting.Hist([10,12,15,20,25,30,35,40,45,50,60,70,100,150,200]),
        }

log.info("making plots")
functor = FunctorFromMVA('kNN', target, *args.variables)

for row in training_NTuple:
    var_d  = dict([(v, getattr(row, v)) for v in args.variables])
    mva    = functor(**var_d)
    weight = row.weight
    cut    = bool( getattr(row, args.cut) )
    for var in args.variables:
        value = var_d[var]
        hist_maps[var]['estimate'].Fill(value, mva*weight)
        hist_maps[var]['all'].Fill(value, weight)
        hist_maps[var]['estimate_all'].Fill(value, weight)
        if cut:
            hist_maps[var]['pass'].Fill(value, weight)


canvas = plotting.Canvas(name='adsf', title='asdf')
canvas.SetLogy(True)
for var in args.variables:

    for key in hist_maps[var].iterkeys():
        hist_maps[var][key] = round_to_ints(hist_maps[var][key])

    eff = asrootpy( ROOT.TGraphAsymmErrors( hist_maps[var]['pass'], hist_maps[var]['all']) )
    eff.markerstyle = 20
    estimate = hist_maps[var]['estimate']
    estimate.Divide(hist_maps[var]['estimate_all'])
    estimate.linecolor = ROOT.kBlue 
    estimate.linewidth = 2
    estimate.fillstyle = 0
    estimate.drawstyle = 'hist'
    
    estimate.Draw()
    eff.Draw('P same')
    canvas.Update()
    canvas.SetLogy(True)
    canvas.SaveAs( output_file.replace('.root', '.%s.png' % var ) )
    
    for key, obj in hist_maps[var].iteritems():
        obj.SetName( '%s_%s' % (var, key) )
        obj.Write()

training_NTuple.Write()

out_tfile.Close()
