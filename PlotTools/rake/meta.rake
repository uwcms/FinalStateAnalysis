# meta.rake
#
# Finds lists of datafiles (starting from a directory)
# and computes meta data: # of events, effective/real int. lumi

namespace :meta do
  # How to generate the inputs
  desc "Query lists of ntuple .root files"
  task :getinputs, [:jobid, :source, :ntuple] do |t, args|
    # If MEGAPATH is enabled, use relative paths.
    opt_relative = ""
    if ENV.has_key?("MEGAPATH")
        opt_relative = "--relative"
    end
    discovercheck = ENV.fetch('discovercheck', "0")
    if discovercheck == "1" then
      sh "discover_ntuples.py #{args.jobid} #{args.source} inputs/#{args.jobid} --force --meta=#{args.ntuple} #{opt_relative}"
    elsif discovercheck == "never" then
      sh "discover_ntuples.py #{args.jobid} #{args.source} inputs/#{args.jobid} --meta=#{args.ntuple} #{opt_relative} --no-check"
    else
      sh "discover_ntuples.py #{args.jobid} #{args.source} inputs/#{args.jobid} --meta=#{args.ntuple} #{opt_relative}"
    end
  end

  def make_meta_tasks(sample, ntuple, sqrts)
    # Getting meta information from ntpule
    file sample + '.meta.root' => sample + '.txt' do |t|
        farmout = ENV.fetch('farmout', "0")
        if farmout == "1"
            sh "mega-farmout $fsa/PlotTools/python/ExtractTree.py #{t.prerequisites} #{t.name} --tree #{ntuple} --verbose"
        else
            sh "mega $fsa/PlotTools/python/ExtractTree.py #{t.prerequisites} #{t.name} --tree #{ntuple}"
        end
    end

    file sample + '.meta.json' => sample + '.meta.root' do |t|
      if t.name.include? 'data'
        sh "extract_meta_info.py #{t.prerequisites} metaInfo #{t.name} --lumimask"
      else
        sh "extract_meta_info.py #{t.prerequisites} metaInfo #{t.name}"
      end
    end

    # For data, we need a computed lumi mask
    if sample.include? 'data'
      # Get lumi mask in plain format.
      file sample + '.lumimask.json' => sample + '.meta.json' do |t|
        sh "cat #{t.prerequisites} | dump_lumimask.py > #{t.name}"
      end
      # Run lumicalc on the mask
      file sample + '.lumicalc.csv' => sample + '.lumimask.json' do |t|
        #sh "pixelLumiCalc.py overview -i #{t.prerequisites} -o #{t.name}"
        sh "lumiCalc2.py overview -i #{t.prerequisites} -o #{t.name}"
      end
      # Get the PU distribution
      file sample + '.pu.root' => sample + '.lumimask.json' do |t|
        pu_file = ''
        maxbin = 50
        nbins = 500
        # Minbias xsection
        minbias = 68000
        if sqrts == "8" then
          pu_file = ENV['pu2012JSON']
          maxbin = 60
          nbins = 600
          minbias = 69400
        end
        if sqrts == "7" then
          pu_file = ENV["pu2011JSON"]
        end
        # Find the newest PU json file
        sh "pileupCalc.py -i #{t.prerequisites[0]} --inputLumiJSON #{pu_file} --calcMode true --minBiasXsec #{minbias} --maxPileupBin #{maxbin} --numPileupBins #{nbins} #{t.name}"
      end
      # Put the lumicalc result in a readable format.  Make it dependent
      # on the PU .root file as well, so it gets built.
      file sample + '.lumicalc.sum' => [sample + '.lumicalc.csv', sample + '.pu.root'] do |t|
        sh "lumicalc_parser.py #{t.prerequisites[0]} > #{t.name}"
      end
    else
      # In MC, we can get the effective lumi from xsec and #events.
      file sample + '.lumicalc.sum' => sample + '.meta.json' do |t|
        sh "get_mc_lumi.py --sqrts #{sqrts} #{sample} `cat #{t.prerequisites} | extract_json.py n_evts` > #{t.name}"
      end
    end
    # Return the final target
    return sample + '.lumicalc.sum'
  end

  task :getmeta, [:directory, :ntuple, :sqrts] do |t, args|
    puts "Computing meta information for #{args.sqrts} TeV in #{args.directory}"
    chdir(args.directory) do
      FileList["*.txt"].each do |txtfile|
        sample = txtfile.sub('.txt', '')
        target = make_meta_tasks(sample, args.ntuple, args.sqrts)
        task :computemeta => target
      end
      #puts Rake::Task['computemeta'].timestamp
      #puts Rake::Task['computemeta'].investigation
      Rake::Task['computemeta'].invoke
    end
  end
end
