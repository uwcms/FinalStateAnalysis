Installation
============

Current CMSSW version: 4_2_8

Steps:

Checkout the repository::

  cd CMSSW_XXX/src
  git clone https://ekfriis@github.com/ekfriis/FinalStateAnalysis.git

Checkout the needed CMSSW tags::

  cd FinalStateAnalysis/recipe/
  # You need to have CVS access
  kinit me@CERN.CH
  # Make sure your CMSSW environment is set up
  cmsenv
  # Checkout needed packages and apply patches
  ./recipe.sh

Install the custom python virtualenv and extra packages::

  ./install_python.sh

This might take a while - the script will download and compile the Numpy
library.

You should be able to check the packages installed in the new python virtualenv
by setting up the environment::

  source environment.sh

and using the "yolk" python tool to query the installed packages::

  yolk -l

It should look something like this::

  PyYAML          - 3.10         - active 
  Python          - 2.6.4        - active development (/cvmfs/cms.cern.ch/slc5_amd64_gcc434/external/python/2.6.4-cms14/lib/python2.6/lib-dynload)
  Rivet           - 1.4.0        - active development (/cvmfs/cms.cern.ch/slc5_amd64_gcc434/external/rivet/1.4.0-cms/lib/python2.6/site-packages)
  distribute      - 0.6.24       - active 
  elementtree     - 1.2.6-20050316 - active development (/cvmfs/cms.cern.ch/slc5_amd64_gcc434/external/elementtree/1.2.6-cms15/share/lib/python2.6/site-packages)
  ipython         - 0.12         - active 
  matplotlib      - 1.0.1        - active 
  numpy           - 1.6.1        - active 
  pip             - 1.0.2        - active 
  pyMinuit2       - 0.0.1        - active development (/cvmfs/cms.cern.ch/slc5_amd64_gcc434/external/pyminuit2/0.0.1-cms22/lib/python2.6/site-packages)
  python-ldap     - 2.3.5        - active development (/cvmfs/cms.cern.ch/slc5_amd64_gcc434/external/python-ldap/2.3.5-cms13/lib/python2.6/site-packages)
  scipy           - 0.8.0        - active development (/cvmfs/cms.cern.ch/slc5_amd64_gcc434/external/py2-scipy/0.8.0-cms2/lib/python2.6/site-packages)
  setuptools      - 0.6c11       - active 
  termcolor       - 1.1.0        - active 
  uncertainties   - 1.8          - active 
  wsgiref         - 0.1.2        - active development (/cvmfs/cms.cern.ch/slc5_amd64_gcc434/external/python/2.6.4-cms14/lib/python2.6)
  yolk            - 0.4.3        - active 
