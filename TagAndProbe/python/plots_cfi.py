import FWCore.ParameterSet.Config as cms

muon_pt_histo = cms.untracked.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(100),
    nbins = cms.untracked.int32(100),
    name = cms.untracked.string("MuonPt"),
    description = cms.untracked.string("Muon p_{T}"),
    plotquantity = cms.untracked.string("daughter1.pt"),
)

muon_eta_histo = cms.untracked.PSet(
    min = cms.untracked.double(-2.5),
    max = cms.untracked.double(2.5),
    nbins = cms.untracked.int32(100),
    name = cms.untracked.string("MuonEta"),
    description = cms.untracked.string("Muon #eta"),
    plotquantity = cms.untracked.string("daughter1.eta"),
)

muon_iso_histo = cms.untracked.PSet(
    min = cms.untracked.double(0.0),
    max = cms.untracked.double(0.3),
    nbins = cms.untracked.int32(120),
    name = cms.untracked.string("MuonIso"),
    description = cms.untracked.string("Muon rel. isolation"),
    plotquantity = cms.untracked.string('daughter1.userFloat("pfLooseIsoPt04")/daughter1.pt'),
)

muon_charge_histo = cms.untracked.PSet(
    min = cms.untracked.double(-1.5),
    max = cms.untracked.double(1.5),
    nbins = cms.untracked.int32(3),
    name = cms.untracked.string("MuonCharge"),
    description = cms.untracked.string("Muon charge"),
    plotquantity = cms.untracked.string('daughter1.charge'),
)


muon_kin_histos = cms.VPSet(
    muon_pt_histo,
    muon_eta_histo,
    muon_iso_histo,
    muon_charge_histo,
)

tau_pt_histo = cms.untracked.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(100),
    nbins = cms.untracked.int32(100),
    name = cms.untracked.string("TauPt"),
    description = cms.untracked.string("Tau p_{T}"),
    plotquantity = cms.untracked.string('daughter2.userCand("jet_nom").pt'),
)

tau_dm_histo = cms.untracked.PSet(
    min = cms.untracked.double(-2.5),
    max = cms.untracked.double(20.5),
    nbins = cms.untracked.int32(23),
    name = cms.untracked.string("TauDecayMode"),
    description = cms.untracked.string("Tau Decay Mode"),
    plotquantity = cms.untracked.string('daughter2.decayMode()'),
)

tau_eta_histo = cms.untracked.PSet(
    min = cms.untracked.double(-2.5),
    max = cms.untracked.double(2.5),
    nbins = cms.untracked.int32(100),
    name = cms.untracked.string("TauEta"),
    description = cms.untracked.string("Tau #eta"),
    plotquantity = cms.untracked.string('daughter2.userCand("jet_nom").eta'),
)

tau_abseta_histo = cms.untracked.PSet(
    min = cms.untracked.double(0.0),
    max = cms.untracked.double(2.5),
    nbins = cms.untracked.int32(100),
    name = cms.untracked.string("AbsTauEta"),
    description = cms.untracked.string("Tau |#eta|"),
    plotquantity = cms.untracked.string('abs(daughter2.userCand("jet_nom").eta)'),
)


tau_kin_histos = cms.VPSet(
    tau_pt_histo,
    tau_dm_histo,
    tau_eta_histo,
    tau_abseta_histo,
)

pzeta_histo = cms.untracked.PSet(
    min = cms.untracked.double(-100),
    max = cms.untracked.double(30),
    nbins = cms.untracked.int32(130),
    name = cms.untracked.string("PZeta"),
    description = cms.untracked.string("P_{#zeta} - 1.5 P_{#zeta}^{vis}"),
    plotquantity = cms.untracked.string(
        'pZetas("nom", "jet_nom", "nom").first '
        '-1.5*pZetas("nom", "jet_nom", "nom").second'),
)

mvis_histo = cms.untracked.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(200),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("Mvis"),
    description = cms.untracked.string("Visible Mass"),
    plotquantity = cms.untracked.string(
        'visP4("nom", "jet_nom").mass'),
)

ptvis_histo = cms.untracked.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(200),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("PTvis"),
    description = cms.untracked.string("Visible #mu-#tau p_{T}"),
    plotquantity = cms.untracked.string(
        'visP4("nom", "jet_nom").pt'),
)

mt_histo = cms.untracked.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(200),
    nbins = cms.untracked.int32(400),
    name = cms.untracked.string("MT"),
    description = cms.untracked.string("#mu-#tau-MET M_{T}"),
    plotquantity = cms.untracked.string(
        'totalP4("nom", "jet_nom", "nom").mt'),
)

mt1_histo = mt_histo.clone(
    name = cms.untracked.string("MT1"),
    description = cms.untracked.string("#mu-MET M_{T}"),
    plotquantity = cms.untracked.string(
        'mt1MEt("nom", "nom")'
    )
)

mt2_histo = mt_histo.clone(
    name = cms.untracked.string("MT2"),
    description = cms.untracked.string("#tau-MET M_{T}"),
    plotquantity = cms.untracked.string(
        'mt2MEt("jet_nom", "nom")'
    )
)


vis_met_angle_histo = cms.untracked.PSet(
    min = cms.untracked.double(-3.14),
    max = cms.untracked.double(3.14),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("DPhiVisMEt"),
    description = cms.untracked.string("Visible #Delta #phi #mu-#tau to MET"),
    plotquantity = cms.untracked.string(
        'abs(deltaPhi(visP4("nom", "jet_nom").phi, met().userCand("nom").phi))'),
)

vis_dphi_histo = cms.untracked.PSet(
    min = cms.untracked.double(-3.14),
    max = cms.untracked.double(3.14),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("DPhi12Vis"),
    description = cms.untracked.string("#Delta #phi #mu-#tau"),
    plotquantity = cms.untracked.string(
        'abs(deltaPhi12("nom", "jet_nom"))'),
)

met_histo = cms.untracked.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(200),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("MET"),
    description = cms.untracked.string("MEt"),
    plotquantity = cms.untracked.string(
        'met().userCand("nom").et'),
)

topo_histos = cms.VPSet(
    pzeta_histo,
    mvis_histo,
    mt_histo,
    mt1_histo,
    mt2_histo,
    ptvis_histo,
    vis_met_angle_histo,
    met_histo,
    vis_dphi_histo,
)

dcasig2d_histo = cms.untracked.PSet(
            min = cms.untracked.double(-2),
            max = cms.untracked.double(20),
            nbins = cms.untracked.int32(200),
            name = cms.untracked.string("DCASig2D"),
            description = cms.untracked.string("DCA Significance (2D)"),
            plotquantity = cms.untracked.string('userFloat("dcaSig2D")'),
        )

dcasig3d_histo = cms.untracked.PSet(
            min = cms.untracked.double(-2),
            max = cms.untracked.double(20),
            nbins = cms.untracked.int32(200),
            name = cms.untracked.string("DCASig3D"),
            description = cms.untracked.string("DCA Significance (3D)"),
            plotquantity = cms.untracked.string('userFloat("dcaSig3D")'),
        )

logdcasig2d_histo = cms.untracked.PSet(
            min = cms.untracked.double(0),
            max = cms.untracked.double(5),
            nbins = cms.untracked.int32(200),
            name = cms.untracked.string("LogDCASig2D"),
            description = cms.untracked.string("Log DCA Significance (2D)"),
            plotquantity = cms.untracked.string('log(userFloat("dcaSig2D"))'),
        )

logdcasig3d_histo = cms.untracked.PSet(
    min = cms.untracked.double(0),
    max = cms.untracked.double(5),
    nbins = cms.untracked.int32(200),
    name = cms.untracked.string("LogDCASig3D"),
    description = cms.untracked.string("Log DCA Significance (3D)"),
    plotquantity = cms.untracked.string('log(userFloat("dcaSig3D"))'),
)

inner_dca_histos = cms.VPSet(
    dcasig2d_histo,
    dcasig3d_histo,
    logdcasig2d_histo,
    logdcasig3d_histo,
)

tau_pt_v_muon_pt = cms.untracked.PSet(
    name = cms.untracked.string("TauPtVsMuonPt"),
    description = cms.untracked.string("Tau p_{T} vs. Muon p_{T}"),
    xAxis = tau_pt_histo,
    yAxis = muon_pt_histo,
)

vis_pt_v_met_pt = cms.untracked.PSet(
    name = cms.untracked.string("VisPtVsMEt"),
    description = cms.untracked.string("Vis p_{T} vs. MEt p_{T}"),
    xAxis = ptvis_histo,
    yAxis = met_histo,
)

vis_dphi_v_met_pt = cms.untracked.PSet(
    name = cms.untracked.string("VisDPhiVsMEt"),
    description = cms.untracked.string("Vis #Delta#phi vs. MEt p_{T}"),
    xAxis = vis_dphi_histo,
    yAxis = met_histo,
)

vis_dphi_v_mt_pt = cms.untracked.PSet(
    name = cms.untracked.string("VisDPhiVsMT"),
    description = cms.untracked.string("Vis #Delta#phi vs. MT"),
    xAxis = vis_dphi_histo,
    yAxis = mt_histo,
)

mt1_v_mt2 = cms.untracked.PSet(
    name = cms.untracked.string("MT1VsMT2"),
    description = cms.untracked.string("#mu-MET Mt vs. #tau-MET Mt"),
    xAxis = mt1_histo,
    yAxis = mt2_histo,
)

tau_pt_v_logdcasig2d = cms.untracked.PSet(
    name = cms.untracked.string("TauPtVsLogDCASig2D"),
    description = cms.untracked.string("Tau p_{T} vs. LogDCA (2D)"),
    xAxis = tau_pt_histo,
    yAxis = logdcasig2d_histo
)

tau_abseta_v_logdcasig2d = cms.untracked.PSet(
    name = cms.untracked.string("TauAbsEtaVsLogDCASig2D"),
    description = cms.untracked.string("Tau |#eta| vs. LogDCA (2D)"),
    xAxis = tau_abseta_histo,
    yAxis = logdcasig2d_histo
)

pzeta_v_logdcasig2d = cms.untracked.PSet(
    name = cms.untracked.string("PZetaVsLogDCASig2D"),
    description = cms.untracked.string("P_{#zeta} vs. LogDCA (2D)"),
    xAxis = pzeta_histo,
    yAxis = logdcasig2d_histo
)

tau_abseta_v_pzeta = cms.untracked.PSet(
    name = cms.untracked.string("TauAbsEtaVsPZeta"),
    description = cms.untracked.string("Tau |#eta| vs. P_{#zeta}"),
    xAxis = tau_abseta_histo,
    yAxis = pzeta_histo
)

pzeta_vis_v_pzeta = cms.untracked.PSet(
    name = cms.untracked.string("PZetaVisVsPZeta"),
    description = cms.untracked.string("P_{#zeta}^{vis} vs. P_{#zeta}"),
    xAxis = cms.untracked.PSet(
        min = cms.untracked.double(-100),
        max = cms.untracked.double(100),
        nbins = cms.untracked.int32(200),
        plotquantity = cms.untracked.string(
            'pZetas("nom", "jet_nom", "nom").first'),
    ),
    yAxis = cms.untracked.PSet(
        min = cms.untracked.double(-100),
        max = cms.untracked.double(100),
        nbins = cms.untracked.int32(200),
        plotquantity = cms.untracked.string(
            'pZetas("nom", "jet_nom", "nom").second'),
    ),
)


correlation_histos = cms.VPSet(
    tau_pt_v_muon_pt,
    tau_pt_v_logdcasig2d,
    tau_abseta_v_logdcasig2d,
    pzeta_v_logdcasig2d,
    tau_abseta_v_pzeta,
    #pzeta_vis_v_pzeta,
    #vis_pt_v_met_pt,
    #vis_dphi_v_met_pt,
    #vis_dphi_v_mt_pt,
    #mt1_v_mt2,
)

all_histos = cms.VPSet()
all_histos.extend(muon_kin_histos)
all_histos.extend(tau_kin_histos)
all_histos.extend(topo_histos)
all_histos.extend(inner_dca_histos)
all_histos.extend(correlation_histos)

    #cms.PSet(
        #min = cms.untracked.double(0),
        #max = cms.untracked.double(20),
        #nbins = cms.untracked.int32(200),
        #name = cms.untracked.string("DCASig12D"),
        #description = cms.untracked.string("Muon DCA Significance to PV (2D)"),
        #plotquantity = cms.untracked.string('userFloat("dcaSig12D")'),
    #),
    #cms.PSet(
        #min = cms.untracked.double(-2),
        #max = cms.untracked.double(20),
        #nbins = cms.untracked.int32(200),
        #name = cms.untracked.string("DCASig13D"),
        #description = cms.untracked.string("Muon DCA Significance to PV (3D)"),
        #plotquantity = cms.untracked.string('userFloat("dcaSig13D")'),
    #),
    #cms.PSet(
        #min = cms.untracked.double(-2),
        #max = cms.untracked.double(20),
        #nbins = cms.untracked.int32(200),
        #name = cms.untracked.string("DCASig22D"),
        #description = cms.untracked.string("Tau DCA Significance to PV (2D)"),
        #plotquantity = cms.untracked.string('userFloat("dcaSig22D")'),
    #),
    #cms.PSet(
        #min = cms.untracked.double(-2),
        #max = cms.untracked.double(20),
        #nbins = cms.untracked.int32(200),
        #name = cms.untracked.string("DCASig23D"),
        #description = cms.untracked.string("Tau DCA Significance to PV (3D)"),
        #plotquantity = cms.untracked.string('userFloat("dcaSig23D")'),
    #),
