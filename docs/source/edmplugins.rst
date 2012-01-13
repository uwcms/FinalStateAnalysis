List of EDM Plugins
===================

CandInfoPrinter
---------------

Prints (to stdout) information about each candidate in a collection.

Example configuration::

  process.printElectrons = cms.EDAnalyzer(
      "CandInfoPrinter",
      src = cms.InputTag("cleanPatElectrons"),
      pt = cms.string("pt"),
      eta = cms.string("eta"),
      superclusterEta = cms.string("superCluster.eta"),
      mva = cms.string("userFloat('MVA')"),
      mitID = cms.string("userFloat('MITID')"),
  )

