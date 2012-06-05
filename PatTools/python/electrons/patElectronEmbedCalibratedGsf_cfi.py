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

    # If the sample is embedded, use the data calibrations
    isMC = isMC and not bool(process.calibratedGsfElectrons.isEmbedded.value())

    data_datasets = set(['Prompt', 'ReReco', 'Jan16ReReco'])
    mc_datasets = set(['Summer11', 'Fall11'])

    if isMC and (dataset not in mc_datasets):
        raise ValueError(
            "Dataset %s is not in the list of valid MC datasets: %s" %
            (dataset, repr(mc_datasets)))
    elif not isMC and (dataset not in data_datasets):
        raise ValueError(
            "Dataset %s is not in the list of valid data datasets: %s" %
            (dataset, repr(data_datasets)))

