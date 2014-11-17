#!/usr/bin/env python
# Tai Sakuma <sakuma@fnal.gov>
import ROOT
import sys
import math
import json
import re
from optparse import OptionParser

ROOT.gROOT.SetBatch(1)

##____________________________________________________________________________||
parser = OptionParser()
parser.add_option('-i', '--inputPath', default = './corrMet.root', action = 'store', type = 'string')
(options, args) = parser.parse_args(sys.argv)
inputPath = options.inputPath

##____________________________________________________________________________||
def main():
    
    printHeader()
    if getNEvents(inputPath):
        count(inputPath)

##____________________________________________________________________________||
def printHeader():
    print '%6s'  % 'run',
    print '%10s' % 'lumi',
    print '%9s'  % 'event',
    print '%35s' % 'module',
    print '%15s' % 'pt',
    print '%10s' % 'eta',
    print '%10s' % 'phi',
    print

##____________________________________________________________________________||
def count(inputPath):

    files = [inputPath]

    events = Events(files)

    handlePatMETs = Handle("std::vector<pat::MET>") 
    handlePFMETs = Handle("std::vector<reco::PFMET>") 
    handleLeafCand = Handle("std::vector<reco::LeafCandidate>")

    handlePatJets = Handle("std::vector<pat::Jet>")
    handlePFJets = Handle("std::vector<reco::PFJet>")

    METCollections = (
        ("pfMet",                   "", "RECO", handlePFMETs   ),
        ("patPfMet",                "", "TUPLE", handlePatMETs   ),
        #("patPFMetForMEtUncertaintyTOM", "", "TUPLE", handlePatMETs   ),
       #("patPFMetTOM",                "", "TUPLE", handlePatMETs   ),
        #("patPfMetT0rt",            "", "TUPLE", handlePatMETs   ),
        #("patPfMetT0rtT1",          "", "TUPLE", handlePatMETs   ),
        #("patPfMetT0pc",            "", "TUPLE", handlePatMETs   ),
        #("patPfMetT0pcT1",          "", "TUPLE", handlePatMETs   ),
        ("patPfMetT1",              "", "TUPLE", handlePatMETs   ),
        ("systematicsMET", "metType1", "TUPLE", handleLeafCand),
        ("systematicsMET", "metsJESUp", "TUPLE", handleLeafCand),
        ("systematicsMET", "metsFullJESUp", "TUPLE", handleLeafCand),
        ("systematicsMET", "metsUESUp", "TUPLE", handleLeafCand),
        ("systematicsMET", "metsFullUESUp", "TUPLE", handleLeafCand),
        ("systematicsMET", "metsJESDown", "TUPLE", handleLeafCand),
        ("systematicsMET", "metsFullJESDown", "TUPLE", handleLeafCand),
        ("systematicsMET", "metsUESDown", "TUPLE", handleLeafCand),
        ("systematicsMET", "metsFullUESDown", "TUPLE", handleLeafCand),
#        #("patPfMetT0rtTxy",         "", "TUPLE", handlePatMETs   ),
#        #("patPfMetT0rtT1Txy",       "", "TUPLE", handlePatMETs   ),
#        #("patPfMetT0pcTxy",         "", "TUPLE", handlePatMETs   ),
#        #("patPfMetT0pcT1Txy",       "", "TUPLE", handlePatMETs   ),
#        #("patPfMetT1xy",            "", "TUPLE", handlePatMETs   ),
#        ("patType1CorrectedPFMetTOM",  "", "TUPLE", handlePatMETs   ),
#        ("patType1CorrectedPFMetElectronEnDown"     ,  "", "TUPLE", handlePatMETs ),
#        ("patType1CorrectedPFMetElectronEnUp"       ,  "", "TUPLE", handlePatMETs ),
#        ("patType1CorrectedPFMetJetEnDown"          ,  "", "TUPLE", handlePatMETs ),
#        ("patType1CorrectedPFMetJetEnUp"            ,  "", "TUPLE", handlePatMETs ),
#        ("patType1CorrectedPFMetJetResDown"         ,  "", "TUPLE", handlePatMETs ),
#        ("patType1CorrectedPFMetJetResUp"           ,  "", "TUPLE", handlePatMETs ),
#        ("patType1CorrectedPFMetMuonEnDown"         ,  "", "TUPLE", handlePatMETs ),
#        ("patType1CorrectedPFMetMuonEnUp"           ,  "", "TUPLE", handlePatMETs ),
#        ("patType1CorrectedPFMetTauEnDown"          ,  "", "TUPLE", handlePatMETs ),
#        ("patType1CorrectedPFMetTauEnUp"            ,  "", "TUPLE", handlePatMETs ),
#        ("patType1CorrectedPFMetUnclusteredEnDown"  ,  "", "TUPLE", handlePatMETs ),
#        ("patType1CorrectedPFMetUnclusteredEnUp"    ,  "", "TUPLE", handlePatMETs ),
        )

    JetCollections = (
#        ("selectedPatJets",                "", "TUPLE", handlePatJets),
#        ("selectedPatJetsAK5chsPF",        "", "TUPLE", handlePatJets),
##        ("smearedPatJets",         "", "TUPLE", handlePatJets),
#        ("selectedPatJetsForMETtype1p2CorrTOM", "", "TUPLE", handlePatJets),
        ("ak5PFJets",              "", "RECO" , handlePFJets),
#        ("patJetsForMETSyst",              "", "TUPLE" , handlePatJets),
        ("patJetsMET",              "", "TUPLE" , handlePatJets),
        ("patJets",              "", "TUPLE" , handlePatJets),
#        ("selectedPatJetsForMETtype1p2CorrTOMAS",              "", "TUPLE" , handlePatJets),
        #("selectedPatJetsForMETtype1p2Corr",              "", "TUPLE" , handlePatJets),
        #("patJetsMETTOMnotOverlappingWithLeptonsForMEtUncertaintyTOM", "", "TUPLE", handlePatJets),
#        ("patJetsNotOverlappingWithLeptonsForMEtUncertaintyTOM", "", "TUPLE", handlePatJets),
#        ("selectedPatJetsAK5chsPF",        "", "TUPLE", handleJets),
#        ("smearedPatJetsAK5chsPF",         "", "TUPLE", handleJets),
#        ("shiftedPatJetsAK5chsPFenUpForRawMEt", "", "TUPLE", handleJets),
#        ("shiftedPatJetsAK5chsPFenUpForCorrMEt", "", "TUPLE", handleJets),

    )


    for event in events:

        run = event.eventAuxiliary().run()
        lumi = event.eventAuxiliary().luminosityBlock()
        eventId = event.eventAuxiliary().event()

        for METCollection in METCollections:
            handle = METCollection[3]

            event.getByLabel(METCollection[0:3], handle)
            met = handle.product().front()
            #if (eventId==3196817 or eventId==3196833 or eventId==3196840):
            if METCollection[0]=="patPfMetT1": T1_official=met.pt()
            if METCollection[0]=="patType1CorrectedPFMetTOM": T1_tom=met.pt()
             
            print '%6d'    % run,
            print '%10d'   % lumi,
            print '%9d'    % eventId,
            print '%35s'   % METCollection[0],
            print '%10.8f' % met.pt(),
            print '%10.3f' % met.eta(),
            print '%10.2f' % met.phi(),
            #print '%10.2f' % (met.phi()/math.pi*180.0),
            print
#        print("(off - tom) / avg(off,tom) = %0.4f"%(2 * (T1_official - T1_tom) / (T1_official + T1_tom)) )
#        print

        for JetCollection in JetCollections:

            handle = JetCollection[3]
            event.getByLabel(JetCollection[0:3], handle)
            #if (eventId==3196817 or eventId==3196833 or eventId==3196840):
            for i in range (handle.product().size()):
             jet = handle.product().at(i)
             if jet.pt() > 20:
 
              print '%6d'    % run,
              print '%10d'   % lumi,
              print '%9d'    % eventId,
              print '%35s'   % JetCollection[0],
              print '%10.8f'  % jet.pt(),
              print '%10.3f'  % jet.eta(),
              print '%10.2f'  % jet.phi(),
              print
        #if (eventId==3196817 or eventId==3196833 or eventId==3196840): print 
        print

##____________________________________________________________________________||
def getNEvents(inputPath):
    file = ROOT.TFile.Open(inputPath)
    events = file.Get('Events')
    return events.GetEntries()

##____________________________________________________________________________||
def loadLibraries():
    argv_org = list(sys.argv)
    sys.argv = [e for e in sys.argv if e != '-h']
    ROOT.gSystem.Load("libFWCoreFWLite")
    ROOT.AutoLibraryLoader.enable()
    ROOT.gSystem.Load("libDataFormatsFWLite")
    ROOT.gSystem.Load("libDataFormatsPatCandidates")
    sys.argv = argv_org

##____________________________________________________________________________||
loadLibraries()
from DataFormats.FWLite import Events, Handle

##____________________________________________________________________________||
if __name__ == '__main__':
    main()
