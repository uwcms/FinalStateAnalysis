import FWCore.ParameterSet.Config as cms

id = cms.PSet(
    name = cms.string("${name}_ElecID"),
    description = cms.string("$nicename Electron ID [${eID}]"),
    cut = cms.string("${getter}userFloat('${eID}') > 0.5"),
    plottable = cms.string("${getter}userFloat('${eID}')"),
    invert = cms.bool(False),
)

reliso = cms.PSet(
    name = cms.string("${name}_RelIso"),
    description = cms.string("$nicename Rel. Iso [${threshold}]"),
    cut = cms.string("(${getter}dr03TkSumPt()"
                     "+max(${getter}dr03EcalRecHitSumEt()-1.0,0.0)"
                     "+${getter}dr03HcalTowerSumEt())/${getter}pt()"
                     "< ${threshold}"),
    plottable = cms.string("(${getter}dr03TkSumPt()"
                     "+max(${getter}dr03EcalRecHitSumEt()-1.0,0.0)"
                     "+${getter}dr03HcalTowerSumEt())/${getter}pt()"),
    invert = cms.bool(False)
)

# For HLT Mu17 Ele8.
HLT_Mu17_Ele8 = cms.PSet(
    name = cms.string("${name}_HLT_Mu17_Ele8"),
    description = cms.string("$nicename trigger match HLT_Mu17_Ele8"),
    cut = cms.string(
        'matchToHLTPath(${index}, "HLT_Mu17_Ele8_CaloId(T|L)(_CaloIsoVL|)_v\d+")'
    ),
    plottable = cms.string(
        'matchToHLTPath(${index}, "HLT_Mu17_Ele8_CaloId(T|L)(_CaloIsoVL|)_v\d+")'
    ),
    invert = cms.bool(False)
)

all = [reliso]
