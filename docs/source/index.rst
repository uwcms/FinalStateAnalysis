.. Final State Analysis Framework documentation master file, created by
   sphinx-quickstart on Sun Dec  4 09:34:54 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The Final State Analysis Framework
==================================

Philosophy
----------

The final state analysis package is built around the data format PATFinalState.
This abstract which encapsulates all of the interesting information needed by
the analyst.   Another way of imagining the PATFinalState is that it represents
a single row in an ntuple.  The advantage of the single object is that is both
lightweight and that it holds references to all of the interesting information
in the event.  Thus you can compose complex observables using only a single
object, enabling many tasks to use the string cut parser.  This allows new cuts
to be implemented quickly, and without writing any C++ code.

Contents:

.. toctree::
   :maxdepth: 2

   intro
   install
   pat_tuple
   tools
   version_control


Building this documentation
---------------------------

This documentation is contained in the FinalStateAnalysis/docs/source folder.
It's built using Sphinx.  The doc files are formatted as 
`Restructured Text <http://docutils.sourceforge.net/rst.html>`_.   To build
the documentation, run ``make html`` in FinalStateAnalysis/docs, and open 
``FinalStateAnalysis/docs/build/html/index.html`` in your web browser.
