# Parameters to be used in production of ZZ ntuples
# Only parameters seen here are used. make_ntuples_cfg.py loads these first
# and then loads any modifications to these parameters from a custom param file
# passed via paramFile=/path/to/param/file.py

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import PSet
from collections import OrderedDict

zzEvVars = PSet()
zzObjVars = PSet()
zzDiObjVars = PSet()
eleVars = PSet()
muVars = PSet()

fsr = 'dretFSR'
brSuffix = fsr.replace("dret", "DREt")
for fsrVar in ['pt', 'eta', 'phi']:
    varCap = fsrVar[0].upper()+fsrVar[1:]
    setattr(zzObjVars, "object%s%s"%(brSuffix, varCap), 
            cms.string(('? daughterHasUserCand({object_idx}, "%sCand") ? ' +
                        'daughterUserCand({object_idx}, "%sCand").%s() : -999.')%(fsr, fsr, fsrVar)))
        
    setattr(zzDiObjVars, "object1_object2_%s%s"%(varCap, brSuffix), 
            cms.string(('diObjectP4WithUserCands({object1_idx}, {object2_idx}, "%sCand").%s')%(fsr, fsrVar))
            )

    setattr(zzEvVars, '%s%s'%(varCap, brSuffix),
            cms.string('p4WithUserCands("%sCand").%s'%(fsr, varCap)))

setattr(eleVars, "objectRelPFIsoRhoR03",
        cms.string('({object}.pfIsolationVariables().sumChargedHadronPt' +
                   '+max(0.0,{object}.pfIsolationVariables().sumNeutralHadronEt' +
                   '+{object}.pfIsolationVariables().sumPhotonEt' +
                   '-{object}.userFloat("rho_fastjet")*{object}.userFloat("EffectiveArea")))' +
                   '/{object}.pt()')
        ),

setattr(muVars, "objectRelPFIsoDBR03",
        cms.string('({object}.pfIsolationR03().sumChargedParticlePt' +
                   '+max({object}.pfIsolationR03().sumPhotonEt' +
                   '+{object}.pfIsolationR03().sumNeutralHadronEt' +
                   '-0.5*{object}.pfIsolationR03().sumPUPt,0.0))' +
                   '/{object}.pt()')
        )

zzObjVars.objectHZZIsoFSR = cms.string('? {object}.hasUserFloat("HZZ4lIsoVal") ? {object}.userFloat("HZZ4lIsoVal") : 999.')

setattr(zzDiObjVars, "object1_object2_Mass%s"%(brSuffix), 
            cms.string(('diObjectP4WithUserCands({object1_idx}, {object2_idx}, "%sCand").M')%(fsr))
            )

setattr(zzEvVars, 'Mass%s'%(brSuffix),
        cms.string('p4WithUserCands("%sCand").M'%(fsr)))

eleVars.objectDREt = cms.string(('? daughterHasUserCand({object_idx}, "%sCand") ? ' +
                                 'daughterAsElectron({object_idx}).userFloat("%sCandDREt") : ' +
                                 '-999.')%(fsr, fsr))

muVars.objectDREt = cms.string(('? daughterHasUserCand({object_idx}, "%sCand") ? ' +
                                'daughterAsMuon({object_idx}).userFloat("%sCandDREt") : ' +
                                '-999.')%(fsr, fsr))


eleVars.objectHZZLooseID = cms.string('{object}.userFloat("HZZ4lIDPass")')
eleVars.objectHZZTightID = cms.string('{object}.userFloat("HZZ4lIDPassTight")')
eleVars.objectHZZIsoPass = cms.string('{object}.userFloat("HZZ4lIsoPass")')
muVars.objectHZZLooseID = cms.string('{object}.userFloat("HZZ4lIDPass")')
muVars.objectHZZTightID = cms.string('{object}.userFloat("HZZ4lIDPassTight")')
muVars.objectHZZIsoPass = cms.string('{object}.userFloat("HZZ4lIsoPass")')

zzEvVars.nJets   = cms.string('evt.jets.size')

parameters = {
    # selections on all objects whether they're included in final states or not, done immediately after necessary variables are embedded
    'preselection' : OrderedDict(
        [
            # vertex cuts
            #('v', '!isFake && ndof > 4 && abs(z) <= 24 && position.Rho <= 2'),

            # Veto electrons that are very close to muons
            ('e', {
                    'm' : {
                        'deltaR' : 0.05,
                        'selection' : 'userFloat("HZZ4lIDPassTight") > 0.5',
                        },
                    },
             ),
            # Remove jets that are near tight ID'd, isolated leptons
            # A separate module cleans jets near FSR photons
            ('j', {
                    'selection' : 'pt > 30 && eta < 4.7 && eta > -4.7 && userFloat("idLoose") > 0.5', # ' && userFloat("puID") > 0.5 '
                    'e' : {
                        'deltaR' : 0.4,
                        'selection' : 'userFloat("HZZ4lIDPassTight") > 0.5 && userFloat("HZZ4lIsoPass") > 0.5',
                        },
                    'm' : {
                        'deltaR' : 0.4,
                        'selection' : 'userFloat("HZZ4lIDPassTight") > 0.5 && userFloat("HZZ4lIsoPass") > 0.5',
                        },
                    }
             )
            ]),
            
    # selections to include object in final state (should be looser than analysis selections)
    'finalSelection' : OrderedDict(
        [
            ('e', 'abs(superCluster().eta) < 3.0 && pt > 6'),
            ('m', 'pt > 4 && (isGlobalMuon || isTrackerMuon)'),
            ]
        ),
    
    # Don't automaticaly cross clean among FS objects
    'crossCleaning' : '',

    # additional variables for ntuple
    'eventVariables' : PSet(
        zzEvVars,
        HZZCategory = '? hasUserFloat("HZZCategory") ? userFloat("HZZCategory") : -1.',
        D_bkg_kin = ('? hasUserFloat("p0plus_VAJHU") ? '
                     'userFloat("p0plus_VAJHU") / (userFloat("p0plus_VAJHU") + '
                     'userFloat("bkg_VAMCFM")) : '
                     '-1.'),
        D_bkg = ('? hasUserFloat("p0plus_VAJHU") ? '
                 'userFloat("p0plus_VAJHU") * userFloat("p0plus_m4l") / '
                 '(userFloat("p0plus_VAJHU") * userFloat("p0plus_m4l") + '
                 'userFloat("bkg_VAMCFM") * userFloat("bkg_m4l")) : '
                 '-1.'),
        D_gg = ('? hasUserFloat("Dgg10_VAMCFM") ? '
                'userFloat("Dgg10_VAMCFM") : '
                '-1.'),
        D_g4 = ('? hasUserFloat("p0plus_VAJHU") ? '
                'userFloat("p0plus_VAJHU") / (userFloat("p0plus_VAJHU") + '
                'userFloat("p0minus_VAJHU")) : '
                '-1.'),
        Djet_VAJHU = ('? evt.jets.size >= 2 && hasUserFloat("pvbf_VAJHU") ? '
                      'userFloat("pvbf_VAJHU") / (userFloat("pvbf_VAJHU") + '
                      'userFloat("phjj_VAJHU")) : '
                      '-1.'),
        muVeto = 'vetoMuons(0.05, \'userFloat(\\\"HZZ4lIDPass\\\") > 0.5\').size()',
        muVetoIso = 'vetoMuons(0.05, \'userFloat(\\\"HZZ4lIDPass\\\") > 0.5 && userFloat(\\\"HZZ4lIsoPass\\\") > 0.5\').size()',
        muVetoTight = 'vetoMuons(0.05, \'userFloat(\\\"HZZ4lIDPassTight\\\") > 0.5\').size()',
        muVetoTightIso = 'vetoMuons(0.05, \'userFloat(\\\"HZZ4lIDPassTight\\\") > 0.5 && userFloat(\\\"HZZ4lIsoPass\\\") > 0.5\').size()',
        eVeto = 'vetoElectrons(0.05, \'userFloat(\\\"HZZ4lIDPass\\\") > 0.5\').size()',
        eVetoIso = 'vetoElectrons(0.05, \'userFloat(\\\"HZZ4lIDPass\\\") > 0.5 && userFloat(\\\"HZZ4lIsoPass\\\") > 0.5\').size()',
        eVetoTight = 'vetoElectrons(0.05, \'userFloat(\\\"HZZ4lIDPassTight\\\") > 0.5\').size()',
        eVetoTightIso = 'vetoElectrons(0.05, \'userFloat(\\\"HZZ4lIDPassTight\\\") > 0.5 && userFloat(\\\"HZZ4lIsoPass\\\") > 0.5\').size()',
        ),
    # candidates of form: objectVarName = 'string expression for selection'
    'candidateVariables' : zzObjVars,
    'electronVariables' : eleVars,
    'muonVariables' : muVars,
    'tauVariables' : PSet(),
    'photonVariables' : PSet(),
    'jetVariables' : PSet(),
    # dicandidates of form: object1_object2_VarName = 'string expression for candidate'
    'dicandidateVariables' : zzDiObjVars,
}
