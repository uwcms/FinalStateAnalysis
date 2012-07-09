# Special recipes for combining the 7 TEV and 8TEV results.
#
directory 'combo_results'

file 'combo_results/vhtt_2lt_yields.tex' => ['tex_yields_table.py', 'vhtt_lep_cards_7TeV/shapes.json', 'vhtt_lep_cards_8TeV/shapes.json'] do |t|
  sh "mkdir -p combo_results"
  sh "./tex_yields_table.py vhtt_lep_cards_7TeV/shapes.json vhtt_lep_cards_8TeV/shapes.json > #{t.name}"
end
