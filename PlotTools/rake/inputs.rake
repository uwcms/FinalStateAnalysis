# Recipes to discover lists of files

# How to generate the inputs
desc "Query lists of ntuple .root files"
task :getinputs, [:jobid, :source, :dir, :histo] do |t, args|
  print "Hello #{args.dir},  #{args.histo}" 
  sh "discover_ntuples.sh #{args.jobid} #{args.source} --meta=#{args.dir} --histo=#{args.histo} inputs/#{args.jobid}"
end
