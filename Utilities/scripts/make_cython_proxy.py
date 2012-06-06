#!/usr/bin/env python
'''

Generate a Cython .pyx TTree wrapper

Currently only simple, single types (I, F) are supported.

Author: Evan K. Friis, UW Madison

'''

import argparse
import cStringIO
import ROOT
import subprocess

_pyx_template = '''

# Load relevant ROOT C++ headers
cdef extern from "TObject.h":
    cdef cppclass TObject:
        pass

cdef extern from "TBranch.h":
    cdef cppclass TBranch:
        int GetEntry(long, int)
        void SetAddress(void*)

cdef extern from "TTree.h":
    cdef cppclass TTree:
        TTree()
        int GetEntry(long, int)
        long LoadTree(long)
        long GetEntries()
        TBranch* GetBranch(char*)

cdef extern from "TFile.h":
    cdef cppclass TFile:
        TFile(char*, char*, char*, int)
        TObject* Get(char*)

# Used for filtering with a string
cdef extern from "TTreeFormula.h":
    cdef cppclass TTreeFormula:
        TTreeFormula(char*, char*, TTree*)
        double EvalInstance(int, char**)

from cpython cimport PyCObject_AsVoidPtr

cdef class {TreeName}:
    # Pointers to tree and current entry
    cdef TTree* tree
    cdef long ientry

    # Branches and address for all
{branchblock}

    def __cinit__(self, ttree):
        # Constructor from a ROOT.TTree
        from ROOT import AsCObject
        self.tree = <TTree*>PyCObject_AsVoidPtr(AsCObject(ttree))
        self.ientry = 0
        # Now set all the branch address
{setbranchesblock}

    # Iterating over the tree
    def __iter__(self):
        self.ientry = 0
        while self.ientry < self.tree.GetEntries():
            yield self
            self.ientry += 1

    # Iterate over rows which pass the filter
    def where(self, filter):
        cdef TTreeFormula* formula = new TTreeFormula(
            "cyiter", filter, self.tree)
        self.ientry = 0
        while self.ientry < self.tree.GetEntries():
            self.tree.LoadTree(self.ientry)
            if formula.EvalInstance(0, NULL):
                yield self
            self.ientry += 1
        del formula

    # Getting/setting the Tree entry number
    property entry:
        def __get__(self):
            return self.ientry
        def __set__(self, int i):
            self.ientry = i

    # Access to the current branch values
{getbranchesblock}

'''

_setup_template = '''
# Tools to compile cython proxy class
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(ext_modules=[Extension(
    "{classname}",                 # name of extension
    ["{classname}.pyx"], #  our Cython source
    include_dirs=['{incdir}'],
    library_dirs=['{libdir}'],
    libraries=['Tree', 'Core', 'TreePlayer'],
    language="c++")],  # causes Cython to create C++ source
    cmdclass={{'build_ext': build_ext}})
'''

def get_branches(tree):
    ''' Get the list of branches in a tree

    Returns a generator of tuples with format:

        [ (branchname, type), ... ]

    Where type is 'F' for float, 'I' for int, etc.

    '''
    type_map = {
        'F' : 'float',
        'I' : 'int',
        'D' : 'double'
    }

    for branch in tree.GetListOfBranches():
        name = branch.GetName()
        type = branch.GetTitle()
        # Clean out the leaflist syntax
        type = type.replace(name, '')
        type = type.replace('/', '')
        if type not in type_map:
            raise TypeError(
                "I don't understand branch type: %s" % type)
        yield name, type_map[type]

def make_pyx(name, tree):
    ''' Generate the content of a pyx file for this Tree '''
    branchblock = cStringIO.StringIO()
    setbranchesblock = cStringIO.StringIO()
    getbranchesblock = cStringIO.StringIO()

    for branch_name, branch_type in get_branches(tree):
        branchblock.write(
'''
    cdef TBranch* {branchname}_branch
    cdef {branchtype} {branchname}_value
'''.format(branchname=branch_name, branchtype=branch_type)
        )
        setbranchesblock.write(
'''
        self.{branchname}_branch = self.tree.GetBranch("{branchname}")
        self.{branchname}_branch.SetAddress(<void*>&self.{branchname}_value)
'''.format(branchname=branch_name, branchtype=branch_type)
        )
        getbranchesblock.write(
'''
    property {branchname}:
        def __get__(self):
            self.{branchname}_branch.GetEntry(self.ientry, 0)
            return self.{branchname}_value
'''.format(branchname=branch_name, branchtype=branch_type)
        )
    return _pyx_template.format(
        TreeName = name,
        branchblock = branchblock.getvalue(),
        setbranchesblock = setbranchesblock.getvalue(),
        getbranchesblock = getbranchesblock.getvalue()
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('template_file',
                        help='File path to .root file with template TTree')
    parser.add_argument('tree_path', help='Path in .root file to TTree')
    parser.add_argument('ClassName', help='Name of cython proxy class')

    args = parser.parse_args()

    file = ROOT.TFile(args.template_file, 'READ')
    tree = file.Get(args.tree_path)

    with open('%s.pyx' % args.ClassName, 'w') as pyx_file:
        pyx_file.write(make_pyx(args.ClassName, tree))

    # Figure out the root include and lib paths
    incdir = subprocess.Popen(
        ['root-config', '--incdir'],
        stdout=subprocess.PIPE).communicate()[0].strip()
    libdir = subprocess.Popen(
        ['root-config', '--libdir'],
        stdout=subprocess.PIPE).communicate()[0].strip()

    with open('%s_setup.py' % args.ClassName, 'w') as setup_file:
        setup_file.write(_setup_template.format(
            incdir=incdir, libdir=libdir, classname = args.ClassName))

