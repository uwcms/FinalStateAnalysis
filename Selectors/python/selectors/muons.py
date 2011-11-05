import FWCore.ParameterSet.Config as cms

id = cms.PSet(
    name = cms.string("${name}_MuID"),
    description = cms.string("$nicename Muon ID [${muID}]"),
    cut = cms.string("${getter}userInt('${muID}') > 0.5"),
    plottable = cms.string("${getter}userInt('${muID}')"),
    invert = cms.bool(False),
)

reliso = cms.PSet(
    name = cms.string("${name}_RelIsoDB"),
    description = cms.string("$nicename #Delta#Beta Rel. Iso [${threshold}]"),
    cut = cms.string(
        "(${getter}chargedHadronIso"
        "+max(${getter}photonIso()"
        "+${getter}neutralHadronIso()"
        "-0.5*${getter}userIso(0),0.0))"
        "/${getter}pt() < ${threshold}"
    ),
    plottable = cms.string(
        "(${getter}chargedHadronIso"
        "+max(${getter}photonIso()"
        "+${getter}neutralHadronIso()"
        "-0.5*${getter}userIso(0),0.0))"
        "/${getter}pt()"
    ),
    invert = cms.bool(False)
)

# Non-PFlow relative isolation
relSubDetIso = cms.PSet(
    name = cms.string("${name}_RelIsoSubDet"),
    description = cms.string("$nicename Sub. Det. Rel. Iso (#DeltaR < 0.3)"),
    cut = cms.string(
        "(${getter}trackIso()"
        "+${getter}ecalIso()"
        "+${getter}hcalIso())"
        "/${getter}pt() < ${threshold}"
    ),
    plottable = cms.string("(${getter}trackIso()"
        "+${getter}ecalIso()"
        "+${getter}hcalIso())"
        "/${getter}pt()"
    ),
    invert = cms.bool(False)
)

# Non-PFlow ECAL abs. isolation
ecalIso = cms.PSet(
    name = cms.string("${name}_ECALIso"),
    description = cms.string("$nicename ECAL Iso < ${threshold}"),
    cut = cms.string(
        "${getter}ecalIso() < ${threshold}"
    ),
    plottable = cms.string(
        "${getter}ecalIso()"
    ),
    invert = cms.bool(False)
)

# Non-PFlow HCAL abs. isolation
hcalIso = cms.PSet(
    name = cms.string("${name}_HCALIso"),
    description = cms.string("$nicename HCAL Iso < ${threshold}"),
    cut = cms.string(
        "${getter}hcalIso() < ${threshold}"
    ),
    plottable = cms.string(
        "${getter}hcalIso()"
    ),
    invert = cms.bool(False)
)

# Global muon
globalTrk = cms.PSet(
    name = cms.string("${name}_GlbTrk"),
    description = cms.string("$nicename has global track"),
    cut = cms.string("${getter}combinedMuon.isNonnull"),
    plottable = cms.string("${getter}combinedMuon.isNonnull"),
    invert = cms.bool(False)
)

# Global muon
pixelHits = cms.PSet(
    name = cms.string("${name}_NpixHits"),
    description = cms.string("$nicename number pixel hits"),
    cut = cms.string("? ${getter}combinedMuon.isNonnull ? "
                     "${getter}combinedMuon.hitPattern.numberOfValidPixelHits :"
                     "-1 > ${threshold}"),
    plottable = cms.string(
        "? ${getter}combinedMuon.isNonnull ? "
        "${getter}combinedMuon.hitPattern.numberOfValidPixelHits : -1"),
    invert = cms.bool(False)
)

# Normalized chi2 of global track
trkNormChi2 = cms.PSet(
    name = cms.string("${name}_GlbTrkNormChi2"),
    description = cms.string("$nicename normalized #chi^{2} < ${threshold}"),
    cut = cms.string(
        "? ${getter}combinedMuon.isNonnull ? "
        "${getter}combinedMuon.chi2/${getter}combinedMuon.ndof : 1e99"
        "< ${threshold}"),
    plottable = cms.string(
        "? ${getter}combinedMuon.isNonnull ? "
        "${getter}combinedMuon.chi2/${getter}combinedMuon.ndof : 1e99"
    ),
    invert = cms.bool(False)
)

# Cut on IP
d0 = cms.PSet(
    name = cms.string("${name}_MuonIP"),
    description = cms.string("$nicename 3D IP < ${threshold}"),
    cut = cms.string("${getter}dB('PV3D') < ${threshold}"),
    plottable = cms.string("${getter}dB('PV3D')"),
    invert = cms.bool(False)
)

################################################################################
### Trigger match selectors  ###################################################
################################################################################

# For HLT_Mu13_Mu8
hltSingleMu13L3Filtered13 = cms.PSet(
    name = cms.string("${name}_hltSingleMu13L3Filtered13"),
    description = cms.string("$nicename trigger match hltSingleMu13L3Filtered13"),
    cut = cms.string(
        'matchToHLTFilter(${index}, "hltSingleMu13L3Filtered13")'
    ),
    plottable = cms.string(
        'matchToHLTFilter(${index}, "hltSingleMu13L3Filtered13")'
    ),
    invert = cms.bool(False)
)

# For HLT_Mu13_Mu8
hltDiMuonL3p5PreFiltered8 = cms.PSet(
    name = cms.string("${name}_hltDiMuonL3p5PreFiltered8"),
    description = cms.string("$nicename trigger match hltDiMuonL3p5PreFiltered8"),
    cut = cms.string(
        'matchToHLTFilter(${index}, "hltDiMuonL3(p5|)PreFiltered8")'
    ),
    plottable = cms.string(
        'matchToHLTFilter(${index}, "hltDiMuonL3(p5|)PreFiltered8")'
    ),
    invert = cms.bool(False)
)

# For HLT_DoubleMu7
hltDiMuonL3PreFiltered7 = cms.PSet(
    name = cms.string("${name}_hltDiMuonL3PreFiltered7"),
    description = cms.string("$nicename trigger match hltDiMuonL3PreFiltered7"),
    cut = cms.string(
        'matchToHLTFilter(${index}, "hltDiMuonL3PreFiltered7")'
    ),
    plottable = cms.string(
        'matchToHLTFilter(${index}, "hltDiMuonL3PreFiltered7")'
    ),
    invert = cms.bool(False)
)

# For Mu30
hltSingleMu30L3Filtered30 = cms.PSet(
    name = cms.string("${name}_hltSingleMu30L3Filtered30"),
    description = cms.string("$nicename trigger match (hltSingleMu30L3Filtered30) HLT_Mu30"),
    cut = cms.string(
        r'matchToHLTFilter(${index}, "hltSingleMu30(L2Qual|)L3Filtered30")'
    ),
    plottable = cms.string(
        r'matchToHLTFilter(${index}, "hltSingleMu30(L2Qual|)L3Filtered30")'
    ),
    invert = cms.bool(False)
)

# For IsoMu24
# hltSingleMu(L2Qual|)IsoL3IsoFiltered24
hltSingleMuIsoL3IsoFiltered24 = cms.PSet(
    name = cms.string("${name}_hltSingleMuIsoL3IsoFiltered24"),
    description = cms.string("$nicename trigger match (hltSingleMuIsoL3IsoFiltered24) HLT_IsoMu24"),
    cut = cms.string(
        r'matchToHLTFilter(${index}, "hltSingleMu(L2Qual|)IsoL3IsoFiltered24")'
    ),
    plottable = cms.string(
        r'matchToHLTFilter(${index}, "hltSingleMu(L2Qual|)IsoL3IsoFiltered24")'
    ),
    invert = cms.bool(False)
)

# For Mu8_Ele17
hltL1Mu3EG5L3Filtered8 = cms.PSet(
    name = cms.string("${name}_hltL1Mu3EG5L3Filtered8"),
    description = cms.string("$nicename trigger match (hltL1Mu3EG5L3Filtered8 ) HLT_Mu8_Ele17"),
    cut = cms.string(
        r'matchToHLTFilter(${index}, "hltL1Mu3EG5L3Filtered8")'
    ),
    plottable = cms.string(
        r'matchToHLTFilter(${index}, "hltL1Mu3EG5L3Filtered8")'
    ),
    invert = cms.bool(False)
)

# For Mu17_Ele8
hltL1Mu3EG5L3Filtered17 = cms.PSet(
    name = cms.string("${name}_hltL1Mu3EG5L3Filtered17"),
    description = cms.string("$nicename trigger match (hltL1Mu3EG5L3Filtered17) HLT_Mu17_Ele8"),
    cut = cms.string(
        r'matchToHLTFilter(${index}, "hltL1Mu3EG5L3Filtered17")'
    ),
    plottable = cms.string(
        r'matchToHLTFilter(${index}, "hltL1Mu3EG5L3Filtered17")'
    ),
    invert = cms.bool(False)
)
