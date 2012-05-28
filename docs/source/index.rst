.. Final State Analysis Framework documentation master file, created by
   sphinx-quickstart on Sun Dec  4 09:34:54 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

==================================
The Final State Analysis Framework
==================================


About this documentation
------------------------

An online version of this documentation is available at
http://readthedocs.org/docs/final-state-analysis/en/latest/.  This manual uses
the Sphinx_ documentation engine.  The source can be found in ``docs/source``
directory.  You can re-build the documentation by installing sphinx and then
running ``make html`` in the ``docs`` directory.

.. _Sphinx: http://sphinx.pocoo.org/


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

Contents
========

.. toctree::
   :maxdepth: 1

   intro
   readme
   install
   pat_tuple
   pat_tuple_generation
   tools
   edmplugins
   version_control

