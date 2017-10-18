# Collection of all common recipes

fsa = ENV['CMSSW_BASE'] + '/src/FinalStateAnalysis'

metarake = fsa + '/PlotTools/rake/meta.rake'
import metarake

cythonrake = fsa + '/PlotTools/rake/cython.rake'
import cythonrake

analysisrake = fsa + '/PlotTools/rake/analysis.rake'
import analysisrake

# Cool debug patch from 
# http://martinfowler.com/articles/rake.html
class Task 
  def investigation
    result = "------------------------------\n"
    result << "Investigating #{name}\n" 
    result << "class: #{self.class}\n"
    result <<  "task needed: #{needed?}\n"
    result <<  "timestamp: #{timestamp}\n"
    result << "pre-requisites: \n"
    prereqs = @prerequisites.collect {|name| Task[name]}
    prereqs.sort! {|a,b| a.timestamp <=> b.timestamp}
    prereqs.each do |p|
      result << "--#{p.name} (#{p.timestamp})\n"
    end
    latest_prereq = @prerequisites.collect{|n| Task[n].timestamp}.max
    result <<  "latest-prerequisite time: #{latest_prereq}\n"
    result << "................................\n\n"
    return result
  end
end

