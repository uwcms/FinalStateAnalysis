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
  # Expose output filename to the analyzer
  ENV['megatarget'] = t.name
  farmout = ENV.fetch('farmout', "0")
  puts farmout
  if farmout == "1"
      sh "mega-farmout #{t.prerequisites[0]} #{t.prerequisites[1]} #{t.name} --verbose"
  else
      workers = ENV.fetch('megaworkers', 2)
      chain   = ENV.fetch('megachain'  , 10)
      sh "time mega #{t.prerequisites[0]} #{t.prerequisites[1]} #{t.name} --workers #{workers} --chain #{chain}"
  end
end

task :analyze, [:jobid, :analyzer, :sample] do |t, args|
   Rake::Task["results/#{args.jobid}/#{args.analyzer}/#{args.sample}.root"].invoke
end
