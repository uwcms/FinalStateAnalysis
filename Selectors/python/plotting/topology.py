import FWCore.ParameterSet.Config as cms

ss = cms.PSet(
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(1.5),
    nbins = cms.untracked.int32(2),
    name = cms.untracked.string("${name}_SS"),
    description = cms.untracked.string("${nicename} is SS"),
    plotquantity = cms.untracked.string("likeSigned(${index1}, ${index2})"),
)

pairMass = cms.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(200),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("${name}_Mass"),
    description = cms.untracked.string("${nicename} Mass"),
    plotquantity = cms.untracked.string("subcand(${index1}, ${index2}).get.mass"),
)

pairDPhi = cms.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(3.14),
    nbins = cms.untracked.int32(100),
    name = cms.untracked.string("${name}_DPhi"),
    description = cms.untracked.string("${nicename} #Delta#phi"),
    plotquantity = cms.untracked.string("abs(dPhi(${index1}, ${index2}))"),
)

phiTopology = cms.PSet(
    name = cms.untracked.string("${name}_DPhiTopo"),
    description = cms.untracked.string("${nicename} #Delta#phi topology"),
    xAxis = cms.untracked.PSet(
        min = cms.untracked.double(0),
        max = cms.untracked.double(3.14),
        nbins = cms.untracked.int32(100),
        plotquantity = cms.untracked.string(
            "abs(deltaPhi(daughterByPt(0).phi, daughterByPt(1).phi))"),
    ),
    yAxis = cms.untracked.PSet(
        min = cms.untracked.double(0),
        max = cms.untracked.double(3.14),
        nbins = cms.untracked.int32(100),
        plotquantity = cms.untracked.string(
            "abs(deltaPhi(daughterByPt(1).phi, daughterByPt(2).phi))"),
    ),
)

lowestTwoAreOS = cms.PSet(
    name = cms.untracked.string("${name}_LowestTwoSS"),
    description = cms.untracked.string("${nicename} Lowest p_{T} are SS"),
    min = cms.untracked.double(-0.5),
    max = cms.untracked.double(1.5),
    nbins = cms.untracked.int32(2),
    plotquantity = cms.untracked.string(
        "abs(daughterByPt(1).charge+daughterByPt(2).charge)/2"),
)

dPhiToMet = cms.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(3.14),
    nbins = cms.untracked.int32(100),
    name = cms.untracked.string("${name}_DPhiToMEt"),
    description = cms.untracked.string("${nicename} #Delta#phi to MET"),
    plotquantity = cms.untracked.string("deltaPhiToMEt(${index})"),
)

mtMET = cms.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(200),
    nbins = cms.untracked.int32(100),
    name = cms.untracked.string("${name}_MtToMET"),
    description = cms.untracked.string("${nicename} M_{T} with MET"),
    plotquantity = cms.untracked.string("mtMET(${index})"),
)

ht = cms.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(300),
    nbins = cms.untracked.int32(100),
    name = cms.untracked.string("${name}_Ht"),
    description = cms.untracked.string("${nicename} H_{T}"),
    plotquantity = cms.untracked.string("${getter}ht()"),
)

jetht = cms.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(300),
    nbins = cms.untracked.int32(100),
    name = cms.untracked.string("${name}_JetHt"),
    description = cms.untracked.string("${nicename} Jet H_{T}"),
    plotquantity = cms.untracked.string('subcand("#,#,#", "extJets", "pt > 10 & userFloat(\'idLoose\') > 0.5").get.ht'),
)

