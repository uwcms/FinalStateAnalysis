# Collection of all common recipes

metarake = ENV['fsa'] + '/PlotTools/rake/meta.rake'
import metarake

cythonrake = ENV['fsa'] + '/PlotTools/rake/cython.rake'
import cythonrake

analysisrake = ENV['fsa'] + '/PlotTools/rake/analysis.rake'
import analysisrake
