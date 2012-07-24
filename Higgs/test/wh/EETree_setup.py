
# Tools to compile cython proxy class
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(ext_modules=[Extension(
    "EETree",                 # name of extension
    ["EETree.pyx"], #  our Cython source
    include_dirs=['/cvmfs/cms.hep.wisc.edu/osg/app/cmssoft/cms/slc5_amd64_gcc434/lcg/root/5.27.06b-cms23/include'],
    library_dirs=['/cvmfs/cms.hep.wisc.edu/osg/app/cmssoft/cms/slc5_amd64_gcc434/lcg/root/5.27.06b-cms23/lib'],
    libraries=['Tree', 'Core', 'TreePlayer'],
    language="c++")],  # causes Cython to create C++ source
    cmdclass={'build_ext': build_ext})
