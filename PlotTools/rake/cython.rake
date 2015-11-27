# Recipes to make cython wrappers and compile them
#
# Example:
#
# rake -f $fsa/PlotTools/rake/cython.rake "make_wrapper[$hdfs/2012-06-18-8TeV-VBF/Zjets_M50/1/higgs_ntuples_cfg-output_1000_0_iXW.root, mm/final/Ntuple, MuMuTree]"
# rake -f $fsa/PlotTools/rake/cython.rake MuMuTree.so

desc "Build a cython wrapper source file"
task :make_wrapper, [:file, :ntuple, :name] do |t, args|
  sh "make_cython_proxy.py #{args.file}  #{args.ntuple} #{args.name}"
end

desc "Compile a cython proxy wrapper"
rule ".so" => [proc { |targ| targ.sub('.so', '_setup.py') }] do |t|
  sh "echo #{t.source} "
  sh "python #{t.source} build_ext --inplace"
end
