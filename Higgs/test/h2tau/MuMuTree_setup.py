
# Tools to compile cython proxy class
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(ext_modules=[Extension(
    "MuMuTree",                 # name of extension
    ["MuMuTree.pyx"], #  our Cython source
    include_dirs=['/cvmfs/cms.hep.wisc.edu/osg/app/cmssoft/cms/slc5_amd64_gcc462/cms/cmssw/CMSSW_5_2_5/external/slc5_amd64_gcc462/bin/../../../../../../lcg/root/5.32.00-cms6/include'],
    library_dirs=['/cvmfs/cms.hep.wisc.edu/osg/app/cmssoft/cms/slc5_amd64_gcc462/cms/cmssw/CMSSW_5_2_5/external/slc5_amd64_gcc462/bin/../../../../../../lcg/root/5.32.00-cms6/lib'],
    libraries=['Tree', 'Core', 'TreePlayer'],
    language="c++")],  # causes Cython to create C++ source
    cmdclass={'build_ext': build_ext})
