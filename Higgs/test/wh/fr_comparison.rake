# Rakefile to compare fake rates between DATA/MC and 7 and 8TeV

$dir7TeV = 'results/2012-07-04-7TeV-Higgs/fakerate_fits/'
$dir8TeV = 'results/2012-07-04-8TeV-Higgs/fakerate_fits/'

$plotdir = 'results/plots/fr_comp'
directory $plotdir

task :allplots => []

# Make task to 
def compare(output, a, b, name_a, name_b, args='')
  task output => [$plotdir, a, b] do |t|
    sh "compare_fits.py #{$plotdir}/#{output} #{a} #{b} --names '#{name_a}' '#{name_b}' #{args}"
  end
  task :allplots => output
end

# Muon fake rate 7 vs 8 TeV
compare(
  'm_wjets_pt10_pfidiso03_muonJetPt-7vs8.pdf',
  $dir7TeV + 'm_wjets_pt10_pfidiso03_muonJetPt-data_mm.root',
  $dir8TeV + 'm_wjets_pt10_pfidiso03_muonJetPt-data_mm.root',
  "7 TeV",
  "8 TeV",
  '--min 5e-3'
)

compare(
  'm_wjets_pt10_pfidiso01_muonJetPt-7vs8.pdf',
  $dir7TeV + 'm_wjets_pt10_pfidiso01_muonJetPt-data_mm.root',
  $dir8TeV + 'm_wjets_pt10_pfidiso01_muonJetPt-data_mm.root',
  "7 TeV",
  "8 TeV",
  '--min 5e-3'
)

# Muon fake rate MC vs. DATA
compare(
  'm_wjets_pt10_pfidiso03_muonJetPt-7TeV-MCvsDATA.pdf',
  $dir7TeV + 'm_wjets_pt10_pfidiso01_muonJetPt-data_mm.root',
  $dir7TeV + 'm_wjets_pt10_pfidiso01_muonJetPt-wjets.root',
  "2011 Data",
  "W+jets MC"
)

# Muon fake rate MC vs. DATA (8 TeV)
compare(
  'm_wjets_pt10_pfidiso03_muonJetPt-8TeV-MCvsDATA.pdf',
  $dir8TeV + 'm_wjets_pt10_pfidiso01_muonJetPt-data_mm.root',
  $dir8TeV + 'm_wjets_pt10_pfidiso01_muonJetPt-wjets.root',
  "2012 Data",
  "W+jets MC"
)

# Tau fake rate MVA in 7 and 8
compare(
  't_ztt_pt20_mvaloose_tauPt-7vs8.pdf',
  $dir7TeV + 't_ztt_pt20_mvaloose_tauPt-data_mm.root',
  $dir8TeV + 't_ztt_pt20_mvaloose_tauPt-data_mm.root',
  "7 TeV",
  "8 TeV"
)

# Tau fake rate HPS in 7 and 8
compare(
  't_ztt_pt20_hpsloose_tauPt-7vs8.pdf',
  $dir7TeV + 't_ztt_pt20_hpsloose_tauPt-data_mm.root',
  $dir8TeV + 't_ztt_pt20_hpsloose_tauPt-data_mm.root',
  "7 TeV",
  "8 TeV"
)

# Tau fake rate MVA vs MC
compare(
  't_ztt_pt20_mvaloose_tauPt-7TeV-MCvsData.pdf',
  $dir7TeV + 't_ztt_pt20_mvaloose_tauPt-data_mm.root',
  $dir7TeV + 't_ztt_pt20_mvaloose_tauPt-zjets.root',
  "2011 Data",
  "Z+jets MC"
)

# Tau fake rate MVA vs MC
compare(
  't_ztt_pt20_mvaloose_tauPt-8TeV-MCvsData.pdf',
  $dir8TeV + 't_ztt_pt20_mvaloose_tauPt-data_mm.root',
  $dir8TeV + 't_ztt_pt20_mvaloose_tauPt-zjets.root',
  "2012 Data",
  "Z+jets MC"
)

# Tau fake rate HPS vs MC
compare(
  't_ztt_pt20_hpsVsMVA_tauPt-7TeV.pdf',
  $dir7TeV + 't_ztt_pt20_hpsloose_tauPt-data_mm.root',
  $dir7TeV + 't_ztt_pt20_mvaloose_tauPt-data_mm.root',
  "2011 HPS",
  "2011 MVA"
)

# Tau fake rate HPS vs MC
compare(
  't_ztt_pt20_hpsVsMVA_tauPt-8TeV.pdf',
  $dir8TeV + 't_ztt_pt20_hpsloose_tauPt-data_mm.root',
  $dir8TeV + 't_ztt_pt20_mvaloose_tauPt-data_mm.root',
  "2012 HPS",
  "2012 MVA"
)
