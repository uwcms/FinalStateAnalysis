#!/usr/bin/env python
'''

Generate a Cython .pyx TTree proxy and its associated
setup.py build file.

Currently only simple, single types (I, F) are supported.

usage::
    make_cython_proxy.py [-h] template_file.root tree_path ClassName

This will generate ClassName.pyx and ClassName_setup.py based
on the tree found at [tree_path] in [template_file.root]

The proxy is built by running::
    python ClassName_setup.py build_ext --inplace
this will create a ClassName.so which can be imported in a regular
python session.  The wrapper is instantiated by passing it a ROOT.TTree.

Author: Evan K. Friis, UW Madison

'''

import argparse
import cStringIO
import ROOT
import subprocess

from FinalStateAnalysis.PlotTools.MegaPath import resolve_file

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
        TTree* GetTree()
        int GetTreeNumber()
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
        void UpdateFormulaLeaves()
        void SetTree(TTree*)

from cpython cimport PyCObject_AsVoidPtr
import warnings
def my_warning_format(message, category, filename, lineno, line=""):
    return "%s:%s\\n" % (category.__name__, message)
warnings.formatwarning = my_warning_format

cdef class {TreeName}:
    # Pointers to tree (may be a chain), current active tree, and current entry
    # localentry is the entry in the current tree of the chain
    cdef TTree* tree
    cdef TTree* currentTree
    cdef int currentTreeNumber
    cdef long ientry
    cdef long localentry
    # Keep track of missing branches we have complained about.
    cdef public set complained

    # Branches and address for all
{branchblock}

    def __cinit__(self, ttree):
        #print "cinit"
        # Constructor from a ROOT.TTree
        from ROOT import AsCObject
        self.tree = <TTree*>PyCObject_AsVoidPtr(AsCObject(ttree))
        self.ientry = 0
        self.currentTreeNumber = -1
        #print self.tree.GetEntries()
        #self.load_entry(0)
        self.complained = set([])

    cdef load_entry(self, long i):
        #print "load", i
        # Load the correct tree and setup the branches
        self.localentry = self.tree.LoadTree(i)
        #print "local", self.localentry
        new_tree = self.tree.GetTree()
        #print "tree", <long>(new_tree)
        treenum = self.tree.GetTreeNumber()
        #print "num", treenum
        if treenum != self.currentTreeNumber or new_tree != self.currentTree:
            #print "New tree!"
            self.currentTree = new_tree
            self.currentTreeNumber = treenum
            self.setup_branches(new_tree)

    cdef setup_branches(self, TTree* the_tree):
        #print "setup"
{setbranchesblock}

    # Iterating over the tree
    def __iter__(self):
        self.ientry = 0
        while self.ientry < self.tree.GetEntries():
            self.load_entry(self.ientry)
            yield self
            self.ientry += 1

    # Iterate over rows which pass the filter
    def where(self, filter):
        print "where"
        cdef TTreeFormula* formula = new TTreeFormula(
            "cyiter", filter, self.tree)
        self.ientry = 0
        cdef TTree* currentTree = self.tree.GetTree()
        while self.ientry < self.tree.GetEntries():
            self.tree.LoadTree(self.ientry)
            if currentTree != self.tree.GetTree():
                currentTree = self.tree.GetTree()
                formula.SetTree(currentTree)
                formula.UpdateFormulaLeaves()
            if formula.EvalInstance(0, NULL):
                yield self
            self.ientry += 1
        del formula

    # Getting/setting the Tree entry number
    property entry:
        def __get__(self):
            return self.ientry
        def __set__(self, int i):
            print i
            self.ientry = i
            self.load_entry(i)

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
    language="c++", 
    #extra_compile_args=['-std=c++11'])],  # causes Cython to create C++ source
    extra_compile_args=['-std=c++11', '-fno-var-tracking-assignments'])],  # causes Cython to create C++ source
    cmdclass={{'build_ext': build_ext}})
'''


def get_branches(tree):
    ''' Get the list of branches in a tree

    Returns a generator of tuples with format:

        [ (branchname, type), ... ]

    Where type is 'F' for float, 'I' for int, etc.

    '''
    type_map = {
        'F': 'float',
        'I': 'int',
        'D': 'double',
        'i': 'long',
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

    # Declare data members & methods for each branch.
    for branch_name, branch_type in get_branches(tree):
        # We need both a pointer to the TBranch, and
        # an owned C++ type (int, float, etc) that the TBranch
        # will point too.
        branchblock.write(
'''
    cdef TBranch* {branchname}_branch
    cdef {branchtype} {branchname}_value
'''.format(branchname=branch_name, branchtype=branch_type)
        )

        # Initialize the branch members.  The branch pointer
        # is loaded from the tree, and the branch address
        # is set to the owned value object.
        setbranchesblock.write(
'''
        #print "making {branchname}"
        self.{branchname}_branch = the_tree.GetBranch("{branchname}")
        #if not self.{branchname}_branch and "{branchname}" not in self.complained:
        if not self.{branchname}_branch and "{branchname}":
            warnings.warn( "{TreeName}: Expected branch {branchname} does not exist!" \
               " It will crash if you try and use it!",Warning)
            #self.complained.add("{branchname}")
        else:
            self.{branchname}_branch.SetAddress(<void*>&self.{branchname}_value)
'''.format(branchname=branch_name, branchtype=branch_type, TreeName=name)
        )
        # Define a property for each branch.
        # When the attribute is gotten, it will call
        # GetEntry on the branch to load the information
        # into the value, and then return the value.
        # Note that the entry number is available/set via
        # the class member ientry.
        getbranchesblock.write(
'''
    property {branchname}:
        def __get__(self):
            self.{branchname}_branch.GetEntry(self.localentry, 0)
            return self.{branchname}_value
'''.format(branchname=branch_name, branchtype=branch_type)
        )
    return _pyx_template.format(
        TreeName=name,
        branchblock=branchblock.getvalue(),
        setbranchesblock=setbranchesblock.getvalue(),
        getbranchesblock=getbranchesblock.getvalue()
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('template_file',
                        help='File path to .root file with template TTree')
    parser.add_argument('tree_path', help='Path in .root file to TTree')
    parser.add_argument('ClassName', help='Name of cython proxy class')

    args = parser.parse_args()

    file = ROOT.TFile(resolve_file(args.template_file), 'READ')
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
            incdir=incdir, libdir=libdir, classname=args.ClassName))
