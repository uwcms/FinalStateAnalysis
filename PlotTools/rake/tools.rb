def get_lumi(sample, jobid)
  lumifiles = Dir.glob("inputs/#{jobid}/*.lumicalc.sum").select {|x| x.include? sample}
  lumifiles = lumifiles.map {|x| Float(File.read(x).strip())*0.001}
  totLumi   = 0
  lumifiles.each {|a| totLumi+=a }
  return totLumi
end

# How to generate the inputs
desc "check that total luminosity is the target one"
def check_luminosity(samples, period, jobid)
  #check that we have the expected lumi
  target_lumi = Float(ENV.fetch("TARGET_LUMI_#{period}", -1))
  tolerance   = Float(ENV.fetch('LUMI_TOLERANCE', 0.1))
  ingore_err  = Float(ENV.fetch('IGNORE_LUMI_ERRORS', 0))
  if target_lumi == -1 || ingore_err == 1
    return nil
  end
  samples.each do |sample|
    totLumi   = get_lumi(sample, jobid)
    diff_to_target = totLumi - target_lumi
    diff_to_target = diff_to_target.abs
    abs_tolerance  = tolerance*target_lumi
    if diff_to_target > abs_tolerance
      raise "For your future mental health the process was stopped! 
The total lumi I have for the sample #{sample} is #{totLumi} which does not 
match with the target one (#{target_lumi}) within the tolerance of #{tolerance}. 
If you want to skip this test set the environmental variable IGNORE_LUMI_ERRORS to 1"
    end
  end
end

