'''

Fit (using the T&P method) various muon efficiencies


'''

import FWCore.ParameterSet.Config as cms

import FinalStateAnalysis.Utilities.TauVarParsing as TauVarParsing
options = TauVarParsing.TauVarParsing(
    skipEvents=0, # For debugging
)

process = cms.Process("TagProbe")
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.fitter = cms.EDAnalyzer(
    "TagProbeFitTreeAnalyzer",
    # IO parameters:
    InputFileNames = cms.vstring(options.inputFiles),
    InputDirectoryName = cms.string("mm/final"),
    InputTreeName = cms.string("Ntuple"),
    OutputFileName = cms.string(options.outputFile),
    #numbrer of CPUs to use for fitting
    NumCPU = cms.uint32(4),
    # specifies wether to save the RooWorkspace containing the data for each bin and
    # the pdf object with the initial and final state snapshots
    SaveWorkspace = cms.bool(True),
    floatShapeParameters = cms.bool(True),
    fixVars = cms.vstring("mean"),

    # defines all the real variables of the probes available in the input tree and intended for use in the efficiencies
    Variables = cms.PSet(
        Leg1Leg2_Mass = cms.vstring("Tag-Probe Mass", "60.0", "120.0", "GeV/c^{2}"),
        Muon2Pt = cms.vstring("Probe p_{T}", "0", "1000", "GeV/c"),
        #Muon2Eta = cms.vstring("Probe #eta", "-2.5", "2.5", ""),
        #Muon2AbsEta = cms.vstring("Probe |#eta|", "0", "2.5", ""),
    ),

    # defines all the discrete variables of the probes available in the input tree and intended for use in the efficiency calculations
    Categories = cms.PSet(
        #Muon2GenPdgId = cms.vstring("MC true", "dummy[pass=15,fail=-1]"),
        DoubleMu7_HLT = cms.vstring("DoubleMu7 passed", 'dummy[pass=1, fail=0]'),
    ),

    Cuts = cms.PSet(
        #relIso15 = cms.vstring("Rel Isol < 0.3", "Muon2_MuRelIso", "0.3"),
        #relIso10 = cms.vstring("Rel Isol < 0.1", "Muon2_MuRelIso", "0.10"),
    ),

    # defines all the PDFs that will be available for the efficiency calculations; uses RooFit's "factory" syntax;
    # each pdf needs to define "signal", "backgroundPass", "backgroundFail" pdfs, "efficiency[0.9,0,1]" and "signalFractionInPassing[0.9]" are used for initial values
    PDFs = cms.PSet(
        gaussPlusLinear = cms.vstring(
            "Gaussian::signal(mass, mean[91.2, 89.0, 93.0], sigma[2.3, 0.5, 10.0])",
            "RooExponential::backgroundPass(mass, cPass[0,-10,10])",
            "RooExponential::backgroundFail(mass, cFail[0,-10,10])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        gaussPlusExpo = cms.vstring(
            "Voigtian::signal(mass, mean[90,80,100], width[2.495], sigma[3,1,20])",
            "Exponential::backgroundPass(mass, lp[0,-5,5])",
            "Exponential::backgroundFail(mass, lf[0,-5,5])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
        cbPlusExpo = cms.vstring(
            "CBShape::signal(mass, mean[90,80,100], sigma[2.5, 0.5, 10], alpha[1, -10, 10], n[3, 0, 10])",
            "Exponential::backgroundPass(mass, lp[0,-5,5])",
            "Exponential::backgroundFail(mass, lf[0,-5,5])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        ),
    ),

    # defines a set of efficiency calculations, what PDF to use for fitting and how to bin the data;
    # there will be a separate output directory for each calculation that includes a simultaneous fit, side band subtraction and counting.
    Efficiencies = cms.PSet(
        first_try = cms.PSet(
            EfficiencyCategoryAndState = cms.vstring('DoubleMu7_HLT',"pass"),
            UnbinnedVariables = cms.vstring("Leg1Leg2_Mass"),
            BinnedVariables = cms.PSet(
                #Muon2GenPdgId = cms.vstring("pass"),
                Muon2Pt = cms.vint32([15, 20, 30, 40, 50, 60, 80, 120]),
            ),
            BinToPDFmap = cms.vstring('cbPlusExpo')
        )
    )
)

process.fit = cms.Path(process.fitter)
