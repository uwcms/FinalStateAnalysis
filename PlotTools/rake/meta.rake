# Rules for extracting meta information (#events, lumis) from ntuples

namespace :meta do

  # How to generate the inputs
  desc "Query lists of ntuple .root files"
  task :getinputs, [:jobid, :source] do |t, args|
    sh "discover_ntuples.sh #{args.jobid} #{args.source} inputs/#{args.jobid}"
  end

  def make_meta_tasks(sample)
    # Getting meta information from ntpule
    task sample + '.meta.json' => sample + '.txt' do |t|
      if t.name.include? 'data'
        sh "extract_meta_info.py #{t.prerequisites} /mutau/metaInfo #{t.name} --lumimask"
      else
        sh "extract_meta_info.py #{t.prerequisites} /mutau/metaInfo #{t.name}"
      end
    end

    # For data, we need a computed lumi mask 
    if sample.include? 'data' 
      # Get lumi mask in plain format.
      task sample + '.lumimask.json' => sample + '.meta.json' do |t|
        sh "cat #{t.prerequisites} | dump_lumimask.py > #{t.name}"
      end
      # Run lumicalc on the mask
      task sample + '.lumicalc.csv' => sample + '.lumimask.json' do |t|
        sh "pixelLumiCalc.py overview -i #{t.prerequisites} -o #{t.name}"
      end
      # Put the lumicalc result in a readable format
      task sample + '.lumicalc.sum' => sample + '.lumicalc.csv' do |t|
        sh "lumicalc_parser.py #{t.prerequisites} > #{t.name}"
      end
    else
      # In MC, we can get the effective lumi from xsec and #events.
      task sample + '.lumicalc.sum' => sample + '.meta.json' do |t|
        sh "get_mc_lumi.py #{sample} `cat #{t.prerequisites} | extract_json.py n_evts` > #{t.name}"
      end
    end
    # Return the final target
    return sample + '.lumicalc.sum'
  end

  task :getmeta, [:directory] do |t, args|
    puts "Computing meta information in #{args.directory}" 
    chdir(args.directory) do
      FileList["*.txt"].each do |txtfile|
        sample = txtfile.sub('.txt', '')
        target = make_meta_tasks(sample)
        multitask :computemeta => target
      end
      #puts Rake::Task['computemeta'].timestamp
      #puts Rake::Task['computemeta'].investigation
      Rake::Task['computemeta'].invoke
    end
  end
end
