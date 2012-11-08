import FWCore.ParameterSet.Config as cms

effective_area_type_names = ['kEleTrkIso03', 
                             'kEleEcalIso03', 
                             'kEleHcalIso03', 
                             'kEleTrkIso04', 
                             'kEleEcalIso04', 
                             'kEleHcalIso04', 
                             'kEleChargedIso03', 
                             'kEleGammaIso03', 
                             'kEleNeutralHadronIso03', 
                             'kEleGammaAndNeutralHadronIso03',
                             'kEleChargedIso04', 
                             'kEleGammaIso04', 
                             'kEleNeutralHadronIso04', 
                             'kEleGammaAndNeutralHadronIso04',
                             'kEleGammaIsoDR0p0To0p1',
                             'kEleGammaIsoDR0p1To0p2',
                             'kEleGammaIsoDR0p2To0p3',
                             'kEleGammaIsoDR0p3To0p4',
                             'kEleGammaIsoDR0p4To0p5',
                             'kEleNeutralHadronIsoDR0p0To0p1',
                             'kEleNeutralHadronIsoDR0p1To0p2',
                             'kEleNeutralHadronIsoDR0p2To0p3',
                             'kEleNeutralHadronIsoDR0p3To0p4',
                             'kEleNeutralHadronIsoDR0p4To0p5'
                             ]
effective_area_types = \
dict([(name,number) for number,name in enumerate(effective_area_type_names)])

effective_area_target_names = ['kEleEANoCorr',
                               'kEleEAData2011',
                               'kEleEASummer11MC',
                               'kEleEAFall11MC',
                               'kEleEAData2012'
                               ]
effective_area_targets = \
dict([(name,number) for number,name in enumerate(effective_area_target_names)])

available_eas = cms.VPSet(
    cms.PSet(name      = cms.string('ea_comb_Data2012_iso04_kt6PFJ'),
             ea_type   = cms.int32(effective_area_types['kEleGammaAndNeutralHadronIso04']),
             ea_target = cms.int32(effective_area_targets['kEleEAData2012'])),
    cms.PSet(name      = cms.string('ea_comb_Fall11MC_iso04_kt6PFJ'),
             ea_type   = cms.int32(effective_area_types['kEleGammaAndNeutralHadronIso04']),
             ea_target = cms.int32(effective_area_targets['kEleEAFall11MC'])),
    cms.PSet(name      = cms.string('ea_comb_Summer11MC_iso04_kt6PFJ'),
             ea_type   = cms.int32(effective_area_types['kEleGammaAndNeutralHadronIso04']),
             ea_target = cms.int32(effective_area_targets['kEleEASummer11MC'])),
    cms.PSet(name      = cms.string('ea_comb_Data2011_iso04_kt6PFJ'),
             ea_type   = cms.int32(effective_area_types['kEleGammaAndNeutralHadronIso04']),
             ea_target = cms.int32(effective_area_targets['kEleEAData2011'])),
    cms.PSet(name      = cms.string('ea_comb_NoCorr_iso04_kt6PFJ'),
             ea_type   = cms.int32(effective_area_types['kEleGammaAndNeutralHadronIso04']),
             ea_target = cms.int32(effective_area_targets['kEleEANoCorr']))
    )


   
    



                            
