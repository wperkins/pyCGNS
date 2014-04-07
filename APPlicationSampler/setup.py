#  -------------------------------------------------------------------------
#  pyCGNS - Python package for CFD General Notation System -
#  See license.txt file in the root directory of this Python module source  
#  -------------------------------------------------------------------------
#
import os
from  distutils.core import setup, Extension
from  distutils.util import get_platform
from Cython.Distutils import build_ext

# --- pyCGNSconfig search
import sys
sys.path+=['../lib']
import setuputils
(pyCGNSconfig,installprocess)=setuputils.search('APP')
# ---
if (not os.path.exists("build")): os.system("ln -sf ../build build")
setuputils.installConfigFiles()

import numpy

incdirs=['%s/lib/python%s/site-packages/numpy/core/include'\
         %(os.path.normpath(sys.exec_prefix),sys.version[:3]),
         '.',
         'CGNS/APP/lib']
incdirs+=[numpy.get_include()]

slist=['cg_grep','cg_list','cg_link','cg_gather','cg_scatter',
       'cg_scan','cg_look']

extmods=[Extension("CGNS.APP.lib.arrayutils",
                  ["CGNS/APP/lib/arrayutils.pyx",
                   "CGNS/APP/lib/hashutils.c"],
                  include_dirs = incdirs,
                  extra_compile_args=[])]

cmdclassdict={'clean':setuputils.clean,'build_ext': build_ext}

# -------------------------------------------------------------------------
setup (
name         = pyCGNSconfig.NAME,
version      = pyCGNSconfig.VERSION,
description  = pyCGNSconfig.DESCRIPTION,
author       = pyCGNSconfig.AUTHOR,
author_email = pyCGNSconfig.EMAIL,
license      = pyCGNSconfig.LICENSE,
packages     = ['CGNS.APP',
                'CGNS.APP.lib',
                'CGNS.APP.tools',
                'CGNS.APP.examples',
                'CGNS.APP.misc'],
scripts      = [ 'CGNS/APP/tools/%s'%f for f in slist],
ext_modules  = extmods,
cmdclass     = cmdclassdict
)
# --- last line
