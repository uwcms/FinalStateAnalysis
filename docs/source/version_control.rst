Version Control
===============

The Final State Analysis package is tracked using the 
`Link Git <http://git-scm.com//>`_
version control system.   Git is different than CVS in that it's
distributed - each repository is local and can stand by itself.  Git makes
it easy to pass changes to other repositories.  This means you can make commits
offline, and without worrying about messing up the central version control
system.

Links
-----

   * `Link Git For Scientists <http://smash.psych.nyu.edu/pages/GitTutorial/>`_
   * `The "central" repo <https://github.com/ekfriis/FinalStateAnalysis>`_

Downloading Code
----------------

To get the code, you can clone from the master repository::

  git clone git@github.com:ekfriis/FinalStateAnalysis.git

Setting up your own online repo
-------------------------------

Go to github.com and set up an account.  Then "fork" the master repository.
Now you have your own version at::

  https://github.com/YOURNAME/FinalStateAnalysis

now get a local copy of your remote version::

  git clone git@github.com:YOURNAME/FinalStateAnalysis.git

You can now edit the code, and commit it as often as you like (see below).  You
can't ever mess anyone else up with conflicts like in CVS so do it often. When
you want to share it, "push" it to your github account::

  git push origin master

Now you can request that this gets "pulled" into the master repository by going
to your github.com site and clicking "Pull Request".

Committing Code
---------------

To commit a file, first add it to the "index" of changes to be commited::

  git add file1 [file2]

Once you're ready to commit, run::

  git commit -m "my commit message"
