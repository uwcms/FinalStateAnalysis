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

# For  HLT_Mu17_Ele8_CaloIdL_v*
hltL1NonIsoHLTNonIsoMu17Ele8PixelMatchFilter = cms.PSet(
    name = cms.string("${name}_hltL1NonIsoHLTNonIsoMu17Ele8PixelMatchFilter"),
    description = cms.string(
        "$nicename trigger match "
        "hltL1NonIsoHLTNonIsoMu17Ele8PixelMatchFilter (HLT_Mu17_Ele8)"),
    cut = cms.string(
        r'matchToHLTFilter(${index}, "hltL1NonIsoHLTNonIsoMu17Ele8PixelMatchFilter")'
    ),
    plottable = cms.string(
        r'matchToHLTFilter(${index}, "hltL1NonIsoHLTNonIsoMu17Ele8PixelMatchFilter")'
    ),
    invert = cms.bool(False)
)

# For  HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_v*
hltMu17Ele8CaloIdTPixelMatchFilter = cms.PSet(
    name = cms.string("${name}_hltMu17Ele8CaloIdTPixelMatchFilter"),
    description = cms.string(
        "$nicename trigger match "
        "hltMu17Ele8CaloIdTPixelMatchFilter (HLT_Mu17_Ele8)"),
    cut = cms.string(
        r'matchToHLTFilter(${index}, "hltMu17Ele8CaloIdTPixelMatchFilter")'
    ),
    plottable = cms.string(
        r'matchToHLTFilter(${index}, "hltMu17Ele8CaloIdTPixelMatchFilter")'
    ),
    invert = cms.bool(False)
)

# For HLT_Mu8_Ele17_CaloIdL_v*
hltL1NonIsoHLTNonIsoMu8Ele17PixelMatchFilter = cms.PSet(
    name = cms.string("${name}_hltL1NonIsoHLTNonIsoMu8Ele17PixelMatchFilter"),
    description = cms.string(
        "$nicename trigger match "
        "hltL1NonIsoHLTNonIsoMu8Ele17PixelMatchFilter (HLT_Mu8_Ele17)"),
    cut = cms.string(
        r'matchToHLTFilter(${index}, "hltL1NonIsoHLTNonIsoMu8Ele17PixelMatchFilter")'
    ),
    plottable = cms.string(
        r'matchToHLTFilter(${index}, "hltL1NonIsoHLTNonIsoMu8Ele17PixelMatchFilter")'
    ),
    invert = cms.bool(False)
)

# For HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_v*
hltMu8Ele17CaloIdTCaloIsoVLPixelMatchFilter = cms.PSet(
    name = cms.string("${name}_hltMu8Ele17CaloIdTCaloIsoVLPixelMatchFilter"),
    description = cms.string(
        "$nicename trigger match "
        "hltMu8Ele17CaloIdTCaloIsoVLPixelMatchFilter (HLT_Mu8_Ele17)"),
    cut = cms.string(
        r'matchToHLTFilter(${index}, "hltMu8Ele17CaloIdTCaloIsoVLPixelMatchFilter")'
    ),
    plottable = cms.string(
        r'matchToHLTFilter(${index}, "hltMu8Ele17CaloIdTCaloIsoVLPixelMatchFilter")'
    ),
    invert = cms.bool(False)
)

all = [reliso]
