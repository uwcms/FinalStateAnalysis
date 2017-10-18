Rakefile Recipes
================

Various Rakefiles for routine tasks live here and can be imported by different
analyses.


Importing
---------

To import one of these into your analysis rakefile, add this to the top::

    metarake = ENV['fsa'] + '/PlotTools/rake/meta.rake'
    import metarake


meta.rake
---------

Recipes for computing meta information (#events, lumimasks) for different
samples.

To add it to your analysis rakefile, add this to the top::

    metarake = ENV['fsa'] + '/PlotTools/rake/meta.rake'
    import metarake

To compute the meta information, you can then run::

    rake meta:getmeta[path/to/ntuple_file_lists/]

inputs.rake
-----------

Tools for finding the available data.  To find the available root files
in a directory::

    rake "getinputs[JOBID, /path/to/job/data]"

Example if my output is in /scratch/efriis/data/2012-06-03-7TeV-Higgs::

    rake "getinputs[2012-06-03-7TeV-Higgs, /scratch/efriis/data]"
