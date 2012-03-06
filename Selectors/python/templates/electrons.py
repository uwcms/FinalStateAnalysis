'''

Ntuple branch template sets for electron objects.

Each string is transformed into an expression on a FinalStateEvent object.

{object} should be replaced by an expression which evaluates to a pat::Electron
i.e. daughter(1) or somesuch.

Author: Evan K. Friis

'''

import FWCore.ParameterSet.Config as cms
from FinalStateAnalysis.Utilities.cfgtools import PSet

# ID and isolation
id = PSet(
    objectWWID = '{object}.userFloat("WWID")',
    objectMITID = '{object}.userFloat("MITID")',
    # Use cms.string so we get the parentheses formatting bonus
    objectRelPFIsoDB = cms.string(
        "({object}.chargedHadronIso"
        "+max({object}.photonIso()"
        "+{object}.neutralHadronIso()"
        "-0.5*{object}.userIso(0),0.0))"
        "/{object}.pt()"
    ),
    objectRelIso = cms.string("({object}.dr03TkSumPt()"
               "+max({object}.dr03EcalRecHitSumEt()-1.0,0.0)"
               "+{object}.dr03HcalTowerSumEt())/{object}.pt()"),
    objectChargeIdTight = '{object}.isGsfCtfScPixChargeConsistent',
    objectChargeIdMed = '{object}.isGsfScPixChargeConsistent',
    objectChargeIdLoose = '{object}.isGsfCtfChargeConsistent',

)

tracking = PSet(
    objectHasConversion = '{object}.userFloat("hasConversion")',
    objectMissingHits = cms.string(
        '? {object}.gsfTrack.isNonnull? '
        '{object}.gsfTrack.trackerExpectedHitsInner.numberOfHits() : 10'),
)
