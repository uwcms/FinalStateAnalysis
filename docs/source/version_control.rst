Version Control
===============

The Final State Analysis package is tracked using the 
`Link Git <http://http://git-scm.com//>`_
version control system.   Git is different than CVS in that it's
distributed - each repository is local and can stand by itself.  Git makes
it easy to pass changes to other repositories.  This means you can make commits
offline, and without worrying about messing up the central version control
system.

Getting Git
-----------------

Git is installed on the UW cluster.  

Downloading Code
----------------

To get the code, you clone from an existing repository::

  git clone git@github.com:ekfriis/FinalStateAnalysis.git

Committing Code
---------------

To commit a file, first add it to the "index" of changes to be commited::

  git add file1 [file2]

Once you're ready to commit, run::

  git commit -m "my commit message"
