Version Control
===============

The Final State Analysis package is tracked using the 
`Link Mercurial <http://mercurial.selenic.com/>`_
version control system.   Mercurial is different than CVS in that it's
distributed - each repository is local and can stand by itself.  Mercurial makes
it easy to pass changes to other repositories.  This means you can make commits
offline, and without worrying about messing up the central version control
system.

Getting Mercurial
-----------------

Mercurial is installed on the UW cluster.  To make it available, add this to
your bashrc:

``alias hg=/afs/hep.wisc.edu/cms/sw/python/2.7/bin/hg``


Updating Code
-------------

To get the updated code, you "pull" from the central repository.  Just run ``hg pull`` in your repository.

Committing Code
---------------

To commit a file, just run

``hg commit [file] -m "[commit message]"``

You can all also commit a directory - this is recursive.
