# meta.rake
#
# Finds lists of datafiles (starting from a directory)
# and computes meta data: # of events, effective/real int. lumi

namespace :meta do
  # How to generate the inputs
  desc "Query lists of ntuple .root files"
  task :getinputs, [:jobid, :source, :ntuple, :histo] do |t, args|
    # If MEGAPATH is enabled, use relative paths.
    opt_relative = ""
    if ENV.has_key?("MEGAPATH")
        opt_relative = "--relative"
    end
    discovercheck = ENV.fetch('discovercheck', "0")
    if discovercheck == "1" then
      sh "discover_ntuples.py #{args.jobid} #{args.source} inputs/#{args.jobid} --force --meta=#{args.ntuple} #{opt_relative}"
    elsif discovercheck == "never" then
      sh "discover_ntuples.py #{args.jobid} #{args.source} inputs/#{args.jobid} --meta=#{args.ntuple} --histo=#{args.histo} #{opt_relative} --no-check"
    else
      sh "discover_ntuples.py #{args.jobid} #{args.source} inputs/#{args.jobid} --meta=#{args.ntuple} --histo=#{args.histo} #{opt_relative}"
    end
  end

  def make_meta_tasks(sample, ntuple, sqrts ,histo)
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
        sh "extract_meta_info.py #{t.prerequisites} metaInfo  #{t.name}  --lumimask"
      else
        sh "extract_meta_info.py #{t.prerequisites} metaInfo  #{t.name} --histo #{histo}"
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
        #sh "lumiCalc2.py overview -i #{t.prerequisites} -o #{t.name}"
        print "lumiCalc2 this does not work yet --> move to brilcalc \n"
      end
      # Get the PU distribution
      file sample + '.pu.root' => sample + '.lumimask.json' do |t|
        pu_file = ''
        maxbin = 52
        nbins = 52
        # Minbias xsection
        minbias = 68000
        if sqrts == "13" then
          pu_file = ENV['pu2017JSON']
          maxbin = 100
          nbins = 100
          # Minbias xsection
          minbias = 69200 # suggested for 13TeV
        end
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
        #print "cannot run pileupCalc.py yet \n"  
        sh "pileupCalc.py -i #{t.prerequisites[0]} --inputLumiJSON #{pu_file} --calcMode true --minBiasXsec #{minbias} --maxPileupBin #{maxbin} --numPileupBins #{nbins} #{t .name} "
	sh "pileupCalc.py -i #{t.prerequisites[0]} --inputLumiJSON #{pu_file} --calcMode true --minBiasXsec #{minbias*1.05} --maxPileupBin #{maxbin} --numPileupBins #{nbins} #{sample+'.pu_up.root'} "
	sh "pileupCalc.py -i #{t.prerequisites[0]} --inputLumiJSON #{pu_file} --calcMode true --minBiasXsec #{minbias*0.95} --maxPileupBin #{maxbin} --numPileupBins #{nbins} #{sample+'.pu_down.root'} "
      end
      # Put the lumicalc result in a readable format.  Make it dependent
      # on the PU .root file as well, so it gets built.
      file sample + '.lumicalc.sum' => [sample + '.lumicalc.csv', sample + '.pu.root'] do |t|
        # sh "lumicalc_parser.py #{t.prerequisites[0]} > #{t.name}"
        print "does not make sense to run lumicalc_parser yet \n"  
      end
    else
      # In MC, we can get the effective lumi from xsec and #events.
      file sample + '.lumicalc.sum' => sample + '.meta.json' do |t|
        event=`cat #{t.prerequisites} | extract_json.py n_evts`
        weight=`cat #{t.prerequisites} | extract_json.py sumweights`
        print event.to_i, " " , weight.to_i, "\n"
        if event.to_i==weight.to_i then
          sh "get_mc_lumi.py --sqrts #{sqrts} #{sample} `cat #{t.prerequisites} | extract_json.py n_evts` > #{t.name}"
        end
        if event.to_i!=weight.to_i then
          sh "get_mc_lumi.py --sqrts #{sqrts} #{sample} #{weight.to_f} > #{t.name}"
        end
      end
    end
    # Return the final target
    return sample + '.lumicalc.sum'
  end

  task :getmeta, [:directory, :ntuple, :sqrt, :histo] do |t, args|
    puts "Computing meta information for #{args.sqrts} TeV in #{args.directory}"
    chdir(args.directory) do
      puts "hello"
      #get override meta tree values
      override_keyword   = 'OVERRIDE_META_TREE_'
      meta_override_keys = ENV.keys.select{|x| x.start_with?(override_keyword)}

      FileList["*.txt"].each do |txtfile|
        sample = txtfile.sub('.txt', '')
        #check if we have to override
        meta_ntuple = args.ntuple
        meta_histo = args.histo
        meta_override_keys.each do |key|
          if sample.start_with?(key.gsub(override_keyword,''))
            meta_ntuple = ENV[key]
          end
        end
        #make the task
        target = make_meta_tasks(sample, meta_ntuple, args.sqrt, meta_histo)
        task :computemeta => target
      end
      #puts Rake::Task['computemeta'].timestamp
      #puts Rake::Task['computemeta'].investigation
      Rake::Task['computemeta'].invoke
    end
  end
end
