#  -------------------------------------------------------------------------
#  pyCGNS - Python package for CFD General Notation System -
#  See license.txt file in the root directory of this Python module source  
#  -------------------------------------------------------------------------
#
from __future__ import unicode_literals
from __future__ import print_function
MAJORVERSION = 5
MINORVERSION = 0
REVISION = 0
# --------------------------------------------------------------------

import os
import sys
import shutil
import re
import time
import subprocess
import distutils.util

from distutils.dir_util import remove_tree
from distutils.core import setup
from distutils.util import get_platform
from distutils.command.clean import clean as _clean

rootfiles = ['__init__.py', 'errors.py', 'version.py', 'config.py', 'test.py']
compfiles = []

pfx = '# '

# if you change this name, also change lines tagged with 'USER CONFIG'
userconfigfile = 'setup_userConfig.py'


class ConfigException(Exception):
    pass


# --------------------------------------------------------------------
def prodtag():
    from time import gmtime, strftime
    proddate = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    try:
        prodhost = os.uname()
    except AttributeError:
        prodhost = 'win32'
    return (proddate, prodhost)


# http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
            w_exe_file = exe_file + '.exe'
            if is_exe(w_exe_file):
                return w_exe_file
            b_exe_file = exe_file + '.bat'
            if is_exe(b_exe_file):
                return b_exe_file

    return None


# --------------------------------------------------------------------
def unique_but_keep_order(lst):
    if len(lst) < 2:
        return lst
    r = [lst[0]]
    for p in lst[1:]:
        if p not in r:
            r.append(p)
    return r


# --------------------------------------------------------------------
def search(incs, libs, tag='pyCGNS',
           deps=['Cython', 'HDF5', 'numpy', 'vtk',
                 'qtpy', 'SQLAlchemy']):
    state = 1
    for com in sys.argv:
        if com in ['help', 'clean']: state = 0
    pt = distutils.util.get_platform()
    vv = "%d.%d" % (sys.version_info[0], sys.version_info[1])
    tg = "%s/./build/lib.%s-%s/CGNS" % (os.getcwd(), pt, vv)
    bptarget = tg
    if (not os.path.exists(bptarget)): os.makedirs(bptarget)
    oldsyspath = sys.path
    sys.path = [os.path.abspath(os.path.normpath('./lib'))]
    cfgdict = {}
    import pyCGNSconfig_default as C_D
    sys.path = oldsyspath
    for ck in dir(C_D):
        if ck[0] != '_':
            cfgdict[ck] = C_D.__dict__[ck]
    pg = prodtag()
    cfgdict['PFX'] = pfx
    cfgdict['DATE'] = pg[0]
    cfgdict['PLATFORM'] = "%s %s %s" % (pg[1][0], pg[1][1], pg[1][-1])
    updateConfig('..', bptarget, cfgdict)
    sys.path = [bptarget] + sys.path

    # here we go, check each dep and add incs/libs/others to config
    try:
        import pyCGNSconfig as C

        # -----------------------------------------------------------------------
        if ('Cython' in deps):
            try:
                if (which('cython') is not None):
                    C.COM_CYTHON = 'cython'
                else:
                    raise Exception
                C.COM_UIC = 'true'
                C.COM_RCC = 'true'
                if (which('pyuic') is not None):  C.COM_UIC = 'pyuic'
                if (which('pyrcc') is not None):  C.COM_RCC = 'pyrcc'
                if (which('pyuic5') is not None): C.COM_UIC = 'pyuic5'
                if (which('pyrcc5') is not None): C.COM_RCC = 'pyrcc5'
                import Cython
                C.HAS_CYTHON = True
                print(pfx + 'using Cython v%s' % Cython.__version__)
                C.HAS_CYTHON_2PLUS = False
                C.CYTHON_VERSION = Cython.__version__
                try:
                    if (float(Cython.__version__[:3]) > 0.1):
                        C.HAS_CYTHON_2PLUS = True
                    else:
                        print(pfx + '***** SKIP Cython version cannot build CGNS')
                except:
                    print(pfx + '***** SKIP Cython version cannot build CGNS')
            except:
                C.HAS_CYTHON = False
                print(pfx + '***** FATAL: Cython not found')

        # -----------------------------------------------------------------------
        if ('PyQt4' in deps):
            try:
                import PyQt4
                import PyQt4.QtCore
                import PyQt4.QtGui
                from PyQt4.Qt import PYQT_VERSION_STR
                from PyQt4.QtCore import QT_VERSION_STR

                C.HAS_PYQT4 = True
                print(pfx + 'using PyQt4 v%s (Qt v%s)' % (PYQT_VERSION_STR, QT_VERSION_STR))
                C.PYQT_VERSION = PYQT_VERSION_STR
                C.QT_VERSION = QT_VERSION_STR
            except:
                C.HAS_PYQT4 = False
                print(pfx + '***** SKIP NAV: PyQt4 not found')
        # -----------------------------------------------------------------------
        if ('qtpy' in deps):
            try:
                import qtpy
                import qtpy.QtCore
                import qtpy.QtGui
                import qtpy.QtWidgets

                C.HAS_QTPY = True
                print(pfx + 'using qtpy v%s (Qt v%s)' % (qtpy.__version__, qtpy.QtCore.__version__))
                C.PYQT_VERSION = str(qtpy.__version__)
                C.QT_VERSION = str(qtpy.QtCore.__version__)
            except:
                C.HAS_QTPY = False
                print(pfx + '***** SKIP NAV: qtpy not found')
        # -----------------------------------------------------------------------
        if ('vtk' in deps):
            try:
                import vtk
                v = vtk.vtkVersion()
                C.HAS_VTK = True
                print(pfx + 'using vtk (python module) v%s' % v.GetVTKVersion())
                C.VTK_VERSION = v.GetVTKVersion()
            except:
                C.HAS_VTK = False
                print(pfx + '***** SKIP NAV/VTK: no vtk python module')

        # -----------------------------------------------------------------------
        if ('numpy' in deps):
            incs = incs + C.NUMPY_PATH_INCLUDES
            libs = libs + C.NUMPY_PATH_LIBRARIES
            tp = find_numpy(incs, libs, C.NUMPY_LINK_LIBRARIES)
            if (tp is None):
                print(pfx + 'FATAL: setup cannot find Numpy')
                sys.exit(1)
            (C.NUMPY_VERSION,
             C.NUMPY_VERSION_API,
             C.NUMPY_PATH_INCLUDES,
             C.NUMPY_PATH_LIBRARIES,
             C.NUMPY_LINK_LIBRARIES,
             C.NUMPY_EXTRA_ARGS) = tp
            print(pfx + 'using Numpy version %s' % (C.NUMPY_VERSION,))
            print(pfx + 'using Numpy API version %s' % (C.NUMPY_VERSION_API,))
            print(pfx + 'using Numpy headers from %s' % (C.NUMPY_PATH_INCLUDES[0]))
            C.HAS_NUMPY = True
            incs = incs + C.NUMPY_PATH_INCLUDES
            libs = libs + C.NUMPY_PATH_LIBRARIES

        # -----------------------------------------------------------------------
        if ('HDF5' in deps):
            incs = incs + C.HDF5_PATH_INCLUDES + C.INCLUDE_DIRS
            libs = libs + C.HDF5_PATH_LIBRARIES + C.LIBRARY_DIRS
            tp = find_HDF5(incs, libs, C.HDF5_LINK_LIBRARIES)
            if (tp is None):
                print(pfx + '***** FATAL: setup cannot find HDF5!')
                sys.exit(1)
            (C.HDF5_VERSION,
             C.HDF5_PATH_INCLUDES,
             C.HDF5_PATH_LIBRARIES,
             C.HDF5_LINK_LIBRARIES,
             C.HDF5_EXTRA_ARGS,
             C.HDF5_HST,
             C.HDF5_H64,
             C.HDF5_HUP) = tp
            print(pfx + 'using HDF5 %s' % (C.HDF5_VERSION,))
            print(pfx + 'using HDF5 headers from %s' % (C.HDF5_PATH_INCLUDES[0]))
            print(pfx + 'using HDF5 libs from %s' % (C.HDF5_PATH_LIBRARIES[0]))
            C.HAS_HDF5 = True
            incs = incs + C.HDF5_PATH_INCLUDES + C.INCLUDE_DIRS
            libs = libs + C.HDF5_PATH_LIBRARIES + C.LIBRARY_DIRS

            # -----------------------------------------------------------------------

    except ImportError:
        print(pfx + '***** FATAL: setup cannot find pyCGNSconfig.py file!')
        sys.exit(1)
    C.HDF5_PATH_INCLUDES = list(set(C.HDF5_PATH_INCLUDES))
    C.HDF5_PATH_LIBRARIES = list(set(C.HDF5_PATH_LIBRARIES))
    C.NUMPY_PATH_INCLUDES = list(set(C.NUMPY_PATH_INCLUDES))
    C.NUMPY_PATH_LIBRARIES = list(set(C.NUMPY_PATH_LIBRARIES))

    incs = unique_but_keep_order(incs)
    libs = unique_but_keep_order(libs)

    C.INCLUDE_DIRS = incs
    C.LIBRARY_DIRS = libs

    C.PRODUCTION_DIR = bptarget

    updateConfig('..', bptarget, C.__dict__, cfgdict)

    return (C, state)


# --------------------------------------------------------------------
def installConfigFiles(bptarget):
    lptarget = '.'
    for ff in rootfiles:
        shutil.copy("%s/lib/%s" % (lptarget, ff), "%s/%s" % (bptarget, ff))
    for ff in compfiles:
        shutil.copy("%s/lib/compatibility/%s" % (lptarget, ff), "%s/%s" % (bptarget, ff))


# --------------------------------------------------------------------
def updateVersionInFile(filename, bptarget):
    f = open('%s/revision.tmp' % bptarget)
    r = int(f.readlines()[0][:-1])
    REVISION = r
    f = open(filename, 'r')
    l = f.readlines()
    f.close()
    vver = '@@UPDATEVERSION@@'
    vrel = '@@UPDATERELEASE@@'
    vrev = '@@UPDATEREVISION@@'
    r = []
    for ll in l:
        rl = ll
        if (ll[-len(vver) - 1:-1] == vver):
            rl = '__version__=%s # %s\n' % (MAJORVERSION, vver)
        if (ll[-len(vrel) - 1:-1] == vrel):
            rl = '__release__=%s # %s\n' % (MINORVERSION, vrel)
        if (ll[-len(vrev) - 1:-1] == vrev):
            ACTUALREV = REVISION
            rl = '__revision__=%s # %s\n' % (ACTUALREV, vrev)
        r += [rl]
    f = open(filename, 'w+')
    f.writelines(r)
    f.close()


# --------------------------------------------------------------------
# Clean target redefinition - force clean everything
relist = ['^.*~$', '^core\.*$', '^pyCGNS\.log\..*$',
          '^#.*#$', '^.*\.aux$', '^.*\.pyc$', '^.*\.bak$', '^.*\.l2h',
          '^Output.*$']
reclean = []

for restring in relist:
    reclean.append(re.compile(restring))


def wselect(args, dirname, names):
    for n in names:
        for rev in reclean:
            if (rev.match(n)):
                # print "%s/%s"%(dirname,n)
                os.remove("%s/%s" % (dirname, n))
                break


class clean(_clean):
    def run(self):
        import glob
        rdirs = glob.glob("./build/*")
        for d in rdirs: remove_tree(d)
        if os.path.exists("./build"):     remove_tree("./build")
        if os.path.exists("./Doc/_HTML"): remove_tree("./Doc/_HTML")
        if os.path.exists("./Doc/_PS"):   remove_tree("./Doc/_PS")
        if os.path.exists("./Doc/_PDF"):  remove_tree("./Doc/_PDF")


# --------------------------------------------------------------------
def confValueAsStr(v):
    if (type(v) == type((1,))): return str(v)
    if (type(v) == type([])):   return str(v)
    if (v in [True, False]):
        return str(v)
    else:
        return '"%s"' % str(v)


# --------------------------------------------------------------------
def updateConfig(pfile, gfile, config_default, config_previous=None):
    if (config_previous):
        from pyCGNSconfig_default import file_pattern as fpat
        cfg = config_default
        for ck in config_previous:
            if ck not in cfg:
                cfg[ck] = config_previous[ck]
        f = open("%s/pyCGNSconfig.py" % (gfile), 'w+')
        f.writelines(fpat % cfg)
        f.close()
        return
    elif (not os.path.exists("%s/pyCGNSconfig.py" % (gfile))):
        print("# create new pyCGNSconfig.py file")
        newconf = 1
    else:
        f1 = os.stat("%s/pyCGNSconfig.py" % (gfile))
        if (os.path.exists("%s/%s" % (pfile, userconfigfile))):
            f2 = os.stat("%s/%s" % (pfile, userconfigfile))
        else:
            f2 = os.stat("./%s" % userconfigfile)
        if (f1.st_mtime < f2.st_mtime):
            newconf = 1
            print(pfx + "using modified %s file" % userconfigfile)
        else:
            newconf = 0
            print(pfx + "using existing %s file" % userconfigfile)
    if newconf:
        sys.path = ['..'] + ['.'] + sys.path
        import setup_userConfig as UCFG  # USER CONFIG
        for ck in dir(UCFG):
            if (ck[0] != '_'): config_default[ck] = UCFG.__dict__[ck]
        if (not os.path.exists('%s' % gfile)):
            os.makedirs('%s' % gfile)
        f = open("%s/pyCGNSconfig.py" % (gfile), 'w+')
        f.writelines(config_default['file_pattern'] % config_default)
        f.close()


# --------------------------------------------------------------------
def frompath_HDF5():
    h5p = which("h5dump")
    if h5p is not None:
        h5root = '/'.join(h5p.split('/')[:-2])
    else:
        h5root = '/usr/local'
    return h5root


# --------------------------------------------------------------------
def find_HDF5(pincs, plibs, libs):
    notfound = 1
    extraargs = []
    vers = ''
    h5root = frompath_HDF5()
    pincs += [h5root, '%s/include' % h5root]
    plibs += [h5root, '%s/lib64' % h5root]
    plibs += [h5root, '%s/lib' % h5root]
    pincs = unique_but_keep_order(pincs)
    plibs = unique_but_keep_order(plibs)
    for pth in plibs:
        if ((os.path.exists(pth + '/libhdf5.a'))
            or (os.path.exists(pth + '/libhdf5.so'))
            or (os.path.exists(pth + '/libhdf5.sl'))):
            notfound = 0
            plibs = [pth]
            break
    if notfound:
        print(pfx + "***** FATAL: libhdf5 not found, please check paths:")
        for ppl in plibs:
            print(pfx, ppl)
    notfound = 1
    for pth in pincs:
        if (os.path.exists(pth + '/hdf5.h')): notfound = 0
    if notfound:
        print(pfx, "***** FATAL: hdf5.h not found, please check paths")
        for ppi in pincs:
            print(pfx, ppi)
        return None

    ifh = 'HDF5 library version: unknown'
    notfound = 1
    for pth in pincs:
        if (os.path.exists(pth + '/H5public.h')):
            fh = open(pth + '/H5public.h', 'r')
            fl = fh.readlines()
            fh.close()
            found = 0
            for ifh in fl:
                if (ifh[:21] == "#define H5_VERS_INFO "):
                    vers = ifh.split('"')[1].split()[-1]
                    found = 1
            if found:
                pincs = [pth]
                notfound = 0
                break
    if notfound:
        print(pfx, "***** FATAL: cannot find hdf5 version, please check paths")
        for ppi in pincs:
            print(pfx, pincs)
        return None

    h64 = 0
    hup = 1
    hst = 1
    if (os.path.exists(pth + '/H5pubconf.h')):
        hup = 1
        hst = 1
    if (os.path.exists(pth + '/h5pubconf.h')):
        hup = 0
        hst = 1
    if (os.path.exists(pth + '/H5pubconf-64.h')):
        h64 = 1
        hup = 1
    if (os.path.exists(pth + '/h5pubconf-64.h')):
        h64 = 1
        hup = 0
    print("HUP", hup)
    return (vers, pincs, plibs, libs, extraargs, hst, h64, hup)

# --------------------------------------------------------------------
def find_numpy(pincs, plibs, libs):
    try:
        import numpy
    except ImportError:
        print(pfx, "**** FATAL cannot import numpy")
        sys.exit(0)
    apivers = ''
    vers = numpy.version.version
    extraargs = []
    pdir = os.path.normpath(sys.prefix)
    xdir = os.path.normpath(sys.exec_prefix)
    pincs += ['%s/lib/python%s/site-packages/numpy/core/include' \
              % (xdir, sys.version[:3])]
    pincs += ['%s/lib/python%s/site-packages/numpy/core/include' \
              % (pdir, sys.version[:3])]
    pincs += [numpy.get_include()]
    notfound = 1
    pincs = unique_but_keep_order(pincs)
    plibs = unique_but_keep_order(plibs)
    for pth in pincs:
        if (os.path.exists(pth + '/numpy/ndarrayobject.h')):
            fh = open(pth + '/numpy/ndarrayobject.h', 'r')
            fl = fh.readlines()
            fh.close()
            found = 0
            for ifh in fl:
                if (ifh[:20] == "#define NPY_VERSION "):
                    apivers = ifh.split()[-1]
                    found = 1
            if found:
                pincs = [pth]
                notfound = 0
                break
        if (os.path.exists(pth + '/numpy/_numpyconfig.h')):
            fh = open(pth + '/numpy/_numpyconfig.h', 'r')
            fl = fh.readlines()
            fh.close()
            found = 0
            for ifh in fl:
                if (ifh[:24] == "#define NPY_ABI_VERSION "):
                    apivers = ifh.split()[-1]
                    found = 1
            if found:
                pincs = [pth]
                notfound = 0
                break
    if notfound:
        print(pfx, "***** FATAL: numpy headers not found, please check your paths")
        print(pfx, pincs)
        return None

    return (vers, apivers, pincs, plibs, libs, extraargs)


# --------------------------------------------------------------------
def touch(filename):
    now = time.time()
    os.utime(filename, (now, now))

# --- last line
