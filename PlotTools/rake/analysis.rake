# Rule to map an analyzer + an MC input to a results .root file
# inputs/jobid/sample.txt => results/jobid/analyzer/sample.root
desc "Analyze a sample, producing a .root file"
#rule /^results\/.*\/.*\/.*.root$/ => [ 
rule ".root" => [ 
  # The analyzer .py file
  proc {|targ| targ.sub(%r{results/.*/(.*)/.*root}, "\\1.py")},
  # The sample file list .txt file
  proc {|targ| targ.sub(%r{results/(.*)/.*/(.*).root}, "inputs/\\1/\\2.txt")} ] do |t|
  # Make the output directory
  sh "mkdir -p `dirname #{t.name}`"
  sh "time mega #{t.prerequisites[0]} #{t.prerequisites[1]} #{t.name}"
end

task :analyze, [:jobid, :analyzer, :sample] do |t, args|
   Rake::Task["results/#{args.jobid}/#{args.analyzer}/#{args.sample}.root"].invoke
end

