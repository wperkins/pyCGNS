#  -------------------------------------------------------------------------
#  pyCGNS - Python package for CFD General Notation System -
#  See license.txt file in the root directory of this Python module source  
#  -------------------------------------------------------------------------
#
MAJORVERSION=4
MINORVERSION=5
REVISION=0
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

rootfiles=['__init__.py','errors.py','version.py','config.py','test.py']
compfiles=['midlevel.py','wrap.py']

pfx='### pyCGNS: '

# if you change this name, also change lines tagged with 'USER CONFIG'
userconfigfile='setup_userConfig.py'

class ConfigException(Exception):
  pass

# --------------------------------------------------------------------
def prodtag():
  from time import gmtime, strftime
  proddate=strftime("%Y-%m-%d %H:%M:%S", gmtime())
  try:
    prodhost=os.uname()
  except AttributeError:
    prodhost='win32'
  return (proddate,prodhost)
  
# --------------------------------------------------------------------
def check_local_config():
  print setuputils.check_command(['pyside-uic'])
  print setuputils.check_command(['pyside-rcc'])
  print setuputils.check_command(['cython'])

# --------------------------------------------------------------------
def check_command(args):
  try:
    r=subprocess.check_output(args,stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError:
    return False
  except OSError:
    return False
  return True

# --------------------------------------------------------------------
def unique_but_keep_order(lst):
  if (len(lst)<2): return lst
  r=[lst[0]]
  for p in lst[1:]:
    if (p not in r): r.append(p)
  return r
    
# --------------------------------------------------------------------
def search(incs,libs,tag='pyCGNS',
           deps=['Cython','HDF5','MLL','numpy','vtk','CHLone',
                 'PySide','SQLAlchemy']):
  state=1
  for com in sys.argv:
    if com in ['help','clean']: state=0
  bxtarget='./build/lib'
  bptarget='./build/lib/CGNS'  
  if (not os.path.exists(bxtarget)):
    os.makedirs(bxtarget)
    pt=distutils.util.get_platform()
    vv="%d.%d"%(sys.version_info[0],sys.version_info[1])
    tg="%s/./build/lib.%s-%s/CGNS"%(os.getcwd(),pt,vv)
    lg="%s/./build/lib/CGNS"%(os.getcwd())
    os.makedirs(tg)
#    os.symlink(tg,lg)
  oldsyspath=sys.path
  sys.path =[os.path.abspath(os.path.normpath('./lib'))]
  cfgdict={}
  import pyCGNSconfig_default as C_D
  sys.path=oldsyspath
  for ck in dir(C_D):
    if (ck[0]!='_'): cfgdict[ck]=C_D.__dict__[ck]
  pg=prodtag()
  cfgdict['PFX']=pfx
  cfgdict['DATE']=pg[0]
  cfgdict['PLATFORM']="%s %s %s"%(pg[1][0],pg[1][1],pg[1][-1])
  updateConfig('..',bptarget,cfgdict)
  sys.path=[bptarget]+sys.path

  # here we go, check each dep and add incs/libs/others to config
  try:
    import pyCGNSconfig as C

    print incs, libs
    # -----------------------------------------------------------------------
    if ('Cython' in deps):
      try:
        from Cython.Distutils import build_ext
        C.HAS_CYTHON=True
      except:
        C.HAS_CYTHON=False

    # -----------------------------------------------------------------------
    if ('HDF5' in deps):
      incs=incs+C.HDF5_PATH_INCLUDES+C.INCLUDE_DIRS
      libs=libs+C.HDF5_PATH_LIBRARIES+C.LIBRARY_DIRS
      tp=find_HDF5(incs,libs,C.HDF5_LINK_LIBRARIES)
      if (tp is None):
        print pfx+'ERROR: %s setup cannot find HDF5!'%tag
        sys.exit(1)
      (C.HDF5_VERSION,
       C.HDF5_PATH_INCLUDES,
       C.HDF5_PATH_LIBRARIES,
       C.HDF5_LINK_LIBRARIES,
       C.HDF5_EXTRA_ARGS)=tp
      print pfx+'using HDF5 %s for %s'%(C.HDF5_VERSION,tag)
      print pfx+'using HDF5 headers from %s'%(C.HDF5_PATH_INCLUDES[0])
      print pfx+'using HDF5 libs from %s'%(C.HDF5_PATH_LIBRARIES[0])
      C.HAS_HDF5=True

    # -----------------------------------------------------------------------
    if ('MLL' in deps):
      incs=incs+C.MLL_PATH_INCLUDES
      libs=libs+C.MLL_PATH_LIBRARIES
      tp=find_MLL(incs,libs,C.MLL_LINK_LIBRARIES,C.MLL_EXTRA_ARGS)
      if (tp is None):
        print pfx+'ERROR: %s setup cannot find cgns.org library (MLL)!'%tag
        C.HAS_MLL=False
      else:
       (C.MLL_VERSION,
        C.MLL_PATH_INCLUDES,
        C.MLL_PATH_LIBRARIES,
        C.MLL_LINK_LIBRARIES,
        C.MLL_EXTRA_ARGS)=tp
       print pfx+'using MLL %s for %s'%(C.MLL_VERSION,tag)
       print pfx+'using MLL headers from %s'%(C.MLL_PATH_INCLUDES[0])
       print pfx+'using MLL libs from %s'%(C.MLL_PATH_LIBRARIES[0])
       C.HAS_MLL=True
        
    # -----------------------------------------------------------------------
    if ('CHLone' in deps):
      incs=incs+C.CHLONE_PATH_INCLUDES
      libs=libs+C.CHLONE_PATH_LIBRARIES
      tp=find_CHLone(incs,libs,C.CHLONE_LINK_LIBRARIES)
      if (tp is None):
        print pfx+'ERROR: %s setup cannot find CHLone!'%tag
        sys.exit(1)
      (C.CHLONE_VERSION,
       C.CHLONE_PATH_INCLUDES,
       C.CHLONE_PATH_LIBRARIES,
       C.CHLONE_LINK_LIBRARIES,
       C.CHLONE_EXTRA_ARGS)=tp
      print pfx+'using CHLone %s for %s'%(C.CHLONE_VERSION,tag)
      print pfx+'using CHLone headers from %s'%(C.CHLONE_PATH_INCLUDES[0])
      print pfx+'using CHLone libs from %s'%(C.CHLONE_PATH_LIBRARIES[0])
      C.HAS_CHLONE=True
        
    # -----------------------------------------------------------------------
    if ('numpy' in deps):
      tp=find_numpy(C.NUMPY_PATH_INCLUDES,
                    C.NUMPY_PATH_LIBRARIES,
                    C.NUMPY_LINK_LIBRARIES)
      if (tp is None):
        print pfx+'ERROR: %s setup cannot find Numpy!'%tag
        sys.exit(1)
      (C.NUMPY_VERSION,
       C.NUMPY_PATH_INCLUDES,
       C.NUMPY_PATH_LIBRARIES,
       C.NUMPY_LINK_LIBRARIES,
       C.NUMPY_EXTRA_ARGS)=tp
      print pfx+'using Numpy API version %s for %s'%(C.NUMPY_VERSION,tag)
      print pfx+'using Numpy headers from %s'%(C.NUMPY_PATH_INCLUDES[0])
      C.HAS_NUMPY=True

    # -----------------------------------------------------------------------

  except ImportError:
    print pfx+'ERROR: %s setup cannot find pyCGNSconfig.py file!'%tag
    sys.exit(1)
  C.MLL_PATH_INCLUDES=list(set(C.MLL_PATH_INCLUDES))
  C.MLL_PATH_LIBRARIES=list(set(C.MLL_PATH_LIBRARIES))
  C.HDF5_PATH_INCLUDES=list(set(C.HDF5_PATH_INCLUDES))
  C.HDF5_PATH_LIBRARIES=list(set(C.HDF5_PATH_LIBRARIES))
  C.CHLONE_PATH_INCLUDES=list(set(C.CHLONE_PATH_INCLUDES))
  C.CHLONE_PATH_LIBRARIES=list(set(C.CHLONE_PATH_LIBRARIES))
  C.NUMPY_PATH_INCLUDES=list(set(C.NUMPY_PATH_INCLUDES))
  C.NUMPY_PATH_LIBRARIES=list(set(C.NUMPY_PATH_LIBRARIES))
  updateConfig('..',bptarget,C.__dict__,cfgdict)
  return (C, state)

# --------------------------------------------------------------------
def installConfigFiles():
  lptarget='.'
  bptarget='./build/lib/CGNS'  
  for ff in rootfiles:
    shutil.copy("%s/lib/%s"%(lptarget,ff),"%s/%s"%(bptarget,ff))
  for ff in compfiles:
    shutil.copy("%s/lib/compatibility/%s"%(lptarget,ff),"%s/%s"%(bptarget,ff))

# --------------------------------------------------------------------
def updateVersionInFile(filename):
  f=open('./lib/revision.tmp')
  r=int(f.readlines()[0][:-1])
  REVISION=r
  f=open(filename,'r')
  l=f.readlines()
  f.close()
  vver='@@UPDATEVERSION@@'
  vrel='@@UPDATERELEASE@@'
  vrev='@@UPDATEREVISION@@'
  r=[]
  for ll in l:
    rl=ll
    if (ll[-len(vver)-1:-1]==vver): 
      rl='__version__=%s # %s\n'%(MAJORVERSION,vver)
    if (ll[-len(vrel)-1:-1]==vrel): 
      rl='__release__=%s # %s\n'%(MINORVERSION,vrel)
    if (ll[-len(vrev)-1:-1]==vrev):
      ACTUALREV=REVISION
      rl='__revision__=%s # %s\n'%(ACTUALREV,vrev)
    r+=[rl]
  f=open(filename,'w+')
  f.writelines(r)
  f.close()

# --------------------------------------------------------------------
# Clean target redefinition - force clean everything
relist=['^.*~$','^core\.*$','^pyCGNS\.log\..*$',
        '^#.*#$','^.*\.aux$','^.*\.pyc$','^.*\.bak$','^.*\.l2h',
        '^Output.*$']
reclean=[]

for restring in relist:
  reclean.append(re.compile(restring))

def wselect(args,dirname,names):
  for n in names:
    for rev in reclean:
      if (rev.match(n)):
        # print "%s/%s"%(dirname,n)
        os.remove("%s/%s"%(dirname,n))
        break

class clean(_clean):
  def walkAndClean(self):
    os.path.walk("..",wselect,[])
  def run(self):
    import glob
    rdirs=glob.glob("./build/*")
    for d in rdirs: remove_tree(d)
    if os.path.exists("./build"):     os.remove("./build")
    if os.path.exists("./Doc/_HTML"): remove_tree("./Doc/_HTML")
    if os.path.exists("./Doc/_PS"):   remove_tree("./Doc/_PS")
    if os.path.exists("./Doc/_PDF"):  remove_tree("./Doc/_PDF")
    self.walkAndClean()

# --------------------------------------------------------------------
def confValueAsStr(v):
  if (type(v)==type((1,))): return str(v)
  if (type(v)==type([])):   return str(v)
  if (v in [True,False]):   return str(v)
  else:                     return '"%s"'%str(v)

# --------------------------------------------------------------------
def updateConfig(pfile,gfile,config_default,config_previous=None):
  if (config_previous):
    from pyCGNSconfig_default import file_pattern as fpat
    cfg=config_default
    for ck in config_previous:
      if (not cfg.has_key(ck)): cfg[ck]=config_previous[ck]
    f=open("%s/pyCGNSconfig.py"%(gfile),'w+')
    f.writelines(fpat%cfg)
    f.close()
    return
  elif (not os.path.exists("%s/pyCGNSconfig.py"%(gfile))):
    print "### pyCGNS: create new pyCGNSconfig.py file"
    newconf=1
  else:
    f1=os.stat("%s/pyCGNSconfig.py"%(gfile))
    if (os.path.exists("%s/%s"%(pfile,userconfigfile))):
      f2=os.stat("%s/%s"%(pfile,userconfigfile))
    else:
      f2=os.stat("./%s"%userconfigfile)
    if (f1.st_mtime < f2.st_mtime):
      newconf=1
      print "### pyCGNS: use modified %s file"%userconfigfile
    else:
      newconf=0
      print "### pyCGNS: use existing %s file"%userconfigfile
  if newconf:
    sys.path=['..']+['.']+sys.path
    import setup_userConfig as UCFG # USER CONFIG
    for ck in dir(UCFG):
      if (ck[0]!='_'): config_default[ck]=UCFG.__dict__[ck]
    if (not os.path.exists('%s'%gfile)):
      os.makedirs('%s'%gfile)
    f=open("%s/pyCGNSconfig.py"%(gfile),'w+')
    f.writelines(config_default['file_pattern']%config_default)
    f.close()

# --------------------------------------------------------------------
def frompath_HDF5():
  try:
   h5p=subprocess.check_output(["which","h5dump"])
  except:
    try:
      h5p=subprocess.check_output(["whence","h5dump"])
    except:
      h5p=None
  if (h5p is not None):
    h5root='/'.join(h5p.split('/')[:-2])
  else:
    h5root='/usr/local'
  return h5root

# --------------------------------------------------------------------
def frompath_MLL():
  try:
   mllp=subprocess.check_output(["which","cgnscheck"],stderr=subprocess.STDOUT)
  except:
    try:
      mllp=subprocess.check_output(["whence","cgnscheck"],stderr=subprocess.STDOUT)
    except:
      mllp=None
  if (mllp is not None):
    mllroot='/'.join(mllp.split('/')[:-2])
  else:
    mllroot='/usr/local'
  return mllroot

# --------------------------------------------------------------------
def find_HDF5(pincs,plibs,libs):
  notfound=1
  extraargs=[]
  vers=''
  h5root=frompath_HDF5()
  pincs+=[h5root,'%s/include'%h5root]
  plibs+=[h5root,'%s/lib64'%h5root]
  plibs+=[h5root,'%s/lib'%h5root]
  pincs=unique_but_keep_order(pincs)
  plibs=unique_but_keep_order(plibs)
  for pth in plibs:
    if (    (os.path.exists(pth+'/libhdf5.a'))
         or (os.path.exists(pth+'/libhdf5.so'))
         or (os.path.exists(pth+'/libhdf5.sl'))):
      notfound=0
      plibs=[pth]
      break
  if notfound:
    print pfx+"ERROR: libhdf5 not found, please check paths:"
    for ppl in plibs:
      print pfx,ppl
  notfound=1
  for pth in pincs:
    if (os.path.exists(pth+'/hdf5.h')): notfound=0
  if notfound:
    print pfx,"ERROR: hdf5.h not found, please check paths"
    for ppi in pincs:
      print pfx,ppi
    return None

  ifh='HDF5 library version: unknown'
  notfound=1
  for pth in pincs:
    if (os.path.exists(pth+'/H5public.h')):
      fh=open(pth+'/H5public.h','r')
      fl=fh.readlines()
      fh.close()
      found=0
      for ifh in fl:
        if (ifh[:21] == "#define H5_VERS_INFO "):
          vers=ifh.split('"')[1].split()[-1]
          found=1
      if found:
        pincs=[pth]
        notfound=0
        break
  if notfound:
      print pfx,"ERROR: cannot find hdf5 version, please check paths"
      for ppi in pincs:
        print pfx,pincs
      return None

  return (vers,pincs,plibs,libs,extraargs)

# --------------------------------------------------------------------
def find_MLL(pincs,plibs,libs,extraargs):
  notfound=1
  vers=''
  cgnsversion='3200'
  mllroot=frompath_MLL()
  pincs+=[mllroot,'%s/include'%mllroot]
  plibs+=[mllroot,'%s/lib'%mllroot]
  libs=['cgns','hdf5']+libs
  pincs=unique_but_keep_order(pincs)
  plibs=unique_but_keep_order(plibs)
  extraargs=[]#'-DCG_BUILD_SCOPE']
  for pth in pincs:
    if (os.path.exists(pth+'/cgnslib.h')):
      notfound=0
      f=open(pth+'/cgnslib.h','r')
      l=f.readlines()
      f.close()
      for ll in l:
        if (ll[:20]=="#define CGNS_VERSION"):
          cgnsversion=ll.split()[2]
          if (cgnsversion<'3200'):
            print pfx,"ERROR: version should be v3.2 for MLL"
            return None
      break
  if notfound:
    print pfx+"ERROR: cgnslib.h not found, please check paths"
    for ppi in pincs:
      print pfx,ppi
    return None

  notfound=1
  for pth in plibs:
    if (    (os.path.exists(pth+'/libcgns.a'))
         or (os.path.exists(pth+'/libcgns.so'))
         or (os.path.exists(pth+'/libcgns.sl'))):
      cgnslib='cgns'
      notfound=0
      break
  if notfound:
    print pfx,"ERROR: libcgns not found, please check paths:"
    for ppl in plibs:
      print pfx,ppl
    return None

  notfound=1
  for pth in pincs:
    if (os.path.exists(pth+'/adfh/ADFH.h')):
      extraargs+=['-D__ADF_IN_SOURCES__']
      notfound=0
      break
    if (os.path.exists(pth+'/ADFH.h')):
      notfound=0
      break

  if notfound:
    print pfx,"Warning: ADFH.h not found, using pyCGNS own headers"
    extraargs+=['-U__ADF_IN_SOURCES__']

  libs=list(set(libs))
  return (cgnsversion,pincs,plibs,libs,extraargs)

# --------------------------------------------------------------------
def find_CHLone(pincs,plibs,libs):
  extraargs=[]
  vers=''
  notfound=1
  libs=['CHLone']
  pincs=unique_but_keep_order(pincs)
  plibs=unique_but_keep_order(plibs)
  for pth in plibs:
    if (    (os.path.exists(pth+'/libCHLone.a'))
         or (os.path.exists(pth+'/libCHLone.so'))
         or (os.path.exists(pth+'/libCHLone.sl'))):
      notfound=0
      plibs=[pth]
      break
  if notfound:
    print pfx+"ERROR: libCHlone not found, please check paths:"
    for ppl in plibs:
      print pfx,ppl
    return None

  notfound=1      
  for pth in pincs:
    if (os.path.exists(pth+'/CHLone/CHLone.h')):
      fh=open(pth+'/CHLone/config.h','r')
      fl=fh.readlines()
      fh.close()
      found=0
      vma=0
      vmi=0
      for ifh in fl:
        if (ifh[:21] == "#define CHLONE_MAJOR "):
          vma=ifh.split()[-1]
        if (ifh[:21] == "#define CHLONE_MINOR "):          
          vmi=ifh.split()[-1]
          found=1
      if found:
        vers="%s.%s"%(vma,vmi)
        pincs=[pth]
        notfound=0
        break
  if notfound:
    print pfx,"ERROR: CHLone/CHLone.h not found, please check paths"
    for ppi in pincs:
      print pfx,ppi
    return None

  return (vers,pincs,plibs,libs,extraargs)

# --------------------------------------------------------------------
def find_numpy(pincs,plibs,libs):
  import numpy
  vers=''
  extraargs=[]
  pdir=os.path.normpath(sys.prefix)
  xdir=os.path.normpath(sys.exec_prefix)
  pincs+=['%s/lib/python%s/site-packages/numpy/core/include'\
         %(xdir,sys.version[:3])]
  pincs+=['%s/lib/python%s/site-packages/numpy/core/include'\
         %(pdir,sys.version[:3])]
  pincs+=[numpy.get_include()]
  notfound=1      
  for pth in pincs:
    if (os.path.exists(pth+'/numpy/ndarrayobject.h')):
      fh=open(pth+'/numpy/ndarrayobject.h','r')
      fl=fh.readlines()
      fh.close()
      found=0
      for ifh in fl:
        if (ifh[:20] == "#define NPY_VERSION "):
          vers=ifh.split()[-1]
          found=1
      if found:
        pincs=[pth]
        notfound=0
        break
    if (os.path.exists(pth+'/numpy/_numpyconfig.h')):
      fh=open(pth+'/numpy/_numpyconfig.h','r')
      fl=fh.readlines()
      fh.close()
      found=0
      for ifh in fl:
        if (ifh[:24] == "#define NPY_ABI_VERSION "):
          vers=ifh.split()[-1]
          found=1
      if found:
        pincs=[pth]
        notfound=0
        break
  if notfound:
    print pfx,"ERROR: numpy headers not found, please check your paths"
    print pfx,pincs
    return None
  
  return (vers,pincs,plibs,libs,extraargs)

# --------------------------------------------------------------------
def touch(filename):
  now=time.time()
  os.utime(filename,(now,now))

# --- last line

