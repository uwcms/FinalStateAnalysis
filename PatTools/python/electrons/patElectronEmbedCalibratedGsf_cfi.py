'''

Embed links to calibrated Gsf Electrons into pat::Electrons

See: https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaElectronEnergyScale

'''

import FWCore.ParameterSet.Config as cms

patElectronEmbedCalibratedGsf = cms.EDProducer(
    "PATElectronEmbedCalibratedGsf",
    src = cms.InputTag('fixme'),
    calibSrc = cms.InputTag("calibratedGsfElectrons")
)

def validate_egamma_calib_config(process):
    ''' Sanity check the inputs to the electron calibration

    For allowed datasets see:

    https://twiki.cern.ch/twiki/bin/viewauth/CMS/EgammaElectronEnergyScale

    '''
    dataset = process.calibratedGsfElectrons.inputDataset.value()
    isMC = bool(process.calibratedGsfElectrons.isMC.value())

    data_datasets = set(['Prompt', 'ReReco', 'Jan16ReReco'])
    mc_datasets = set(['Summer11', 'Fall11'])

    if isMC:
        assert(dataset in mc_datasets)
    else:
        assert(dataset in data_datasets)

