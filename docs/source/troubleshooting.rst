Troubleshooting
===============

A summary of frequently encountered errors and there solutions.

*Step ZERO*

If something doesn't work, try running ``cmsenv``, and ``source FinalStateAnalysis/environment.sh`` and then try again.

General CMSSW problems
----------------------

ERROR: Unable to find release area
''''''''''''''''''''''''''''''''''

You have the wrong SCRAM_ARCH set.  You need to do::

   export SCRAM_ARCH=slc5_amd64_gcc434

for CMSSW_4_X_Y and::

   export SCRAM_ARCH=slc5_amd64_gcc462

for CMSSW_5_X_Y.  Note these will change for future CMSSW versions!


Getting the code (git problems)
-------------------------------

These are generally problems that happen when you are trying to checkout
or update the code (``git pull origin master``).

fatal: Not a git repository
'''''''''''''''''''''''''''

This error occurs when you try to ``git pull`` outside of the FinalStateAnalysis
directory (which is the "root" of the git repository).  Solution is to run the 
command in that directory.

error: Your local changes to the following files would be overwritten by merge
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

This means that you have files changed in your working area that are also 
changed in the code update you are trying to pull.   You can see locally modified
files by running ``git status``.

You have two options:

- Commit your changes ``git add [the files]``, ``git commit -m "my commit message"``, and then pull again.
- Reset (lose/throw away/discard) your changes (danger!) ``git checkout -- [files]``
- "Stash" your changes (advanced) ``git stash``

Permission denied (publickey).
''''''''''''''''''''''''''''''

You need to create a github.com account, and generate a SSH key pair.  
Instructions to do this are at `Generating SSH keys`_:

.. _Generating SSH keys: https://help.github.com/articles/generating-ssh-keys

Runtime Errors
--------------

First, always make sure that you did::

   source environment.sh

in the FinalStateAnalysis directory to setup your environment.


ImportError: No module named ...
''''''''''''''''''''''''''''''''

Generally this means that you have either not setup your environment, or not 
compiled the area.  (``scram b -j 6`` in the ``src/`` directory)


ImportError: No module named rootpy
'''''''''''''''''''''''''''''''''''

This is a special case, generally only needed for plotting - ``rootpy`` is an 
external package that needs to be downloaded and installed::

   cd $CMSSW_BASE/src/FinalStateAnalysis/recipe/external/src
   git clone git@github.com:ekfriis/rootpy.git
   cd $CMSSW_BASE/src/FinalStateAnalysis/recipe
   ./install_python.sh

