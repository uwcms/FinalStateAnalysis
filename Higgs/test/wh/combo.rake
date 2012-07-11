# Special recipes for combining the 7 TEV and 8TEV results.

directory 'combo_results'

################################################################################
# Recipes to make data cards and tables (plots come for free)
#  targets:
#      cards
################################################################################

file  'vhtt_lep_cards_8TeV/shapes.json' => ['vhtt_lep_cards_8TeV/shapes.root'] do |t|
  sh "print_histogram_yields.py --json #{t.prerequisites} > #{t.name}"
end

file  'vhtt_lep_cards_7TeV/shapes.json' => ['vhtt_lep_cards_7TeV/shapes.root'] do |t|
  sh "print_histogram_yields.py --json #{t.prerequisites} > #{t.name}"
end

file 'combo_results/vhtt_2lt_yields.tex' => ['tex_yields_table.py', 'vhtt_lep_cards_7TeV/shapes.json', 'vhtt_lep_cards_8TeV/shapes.json'] do |t|
  sh "mkdir -p combo_results"
  sh "./tex_yields_table.py vhtt_lep_cards_7TeV/shapes.json vhtt_lep_cards_8TeV/shapes.json > #{t.name}"
end

$carddir = "vhtt_2lt_combo_cards"
directory $carddir

$source7 = "vhtt_lep_cards_7TeV"
$source8 = "vhtt_lep_cards_8TeV"

def make_combo_card(channel, mass)
  outcard = "#{$carddir}/#{channel}/#{mass}/vhtt_#{channel}.txt"
  # Combine 7 and 8 TeV
  card7 = "#{$source7}/#{channel}/#{mass}/vhtt_#{channel}.txt"
  card8 = "#{$source8}/#{channel}/#{mass}/vhtt_#{channel}.txt"
  file outcard => [card7, card8] do |t|
    sh "mkdir -p #{File.dirname(outcard)}"
    chdir($carddir) do
      sh "combineCards.py -S 7TeV=../#{card7} 8TeV=../#{card8} > #{channel}/#{mass}/vhtt_#{channel}.txt"
    end
  end
  return outcard
end

cardmasses = Array[120]
channels = Array["emt", "mmt", "eet", "2lt"]

task :cards => []

cardmasses.each do |mass|
  channels.each do |channel|
    task :cards => make_combo_card(channel, mass)
  end
end
